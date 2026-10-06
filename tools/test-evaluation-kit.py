"""Dependency-free release checks: XLSX structure/caches, fixture and local links.

Native recalculation and mutation tests live in test-evaluation-kit.ps1.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from zipfile import ZipFile
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
fixture = json.loads((ROOT / "tools/fixtures/evaluation-kit.json").read_text(encoding="utf-8"))
book_html = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
figure = re.search(r'<figure[^>]*aria-labelledby="reranking-recall-worked-title".*?</figure>', book_html, re.S).group()
tiles = re.findall(r'class="recall-tile (relevant|other)">([A-T])<', figure)
assert len(tiles) == 40
assert [record for _, record in tiles[:20]] == fixture["before"]
assert [record for _, record in tiles[20:]] == fixture["after"]
assert {record for label, record in tiles if label == "relevant"} == set(fixture["relevant"])
assert len(fixture["probes"]) == 5
assert len(set(fixture["seeds"])) == 5

def cell(sheet, address):
    element = sheet.find(f"s:sheetData/s:row/s:c[@r='{address}']", NS)
    value = element.find("s:v", NS) if element is not None else None
    if value is None or value.text is None:
        return ""
    return value.text if element.get("t") == "str" else float(value.text)

for suffix in ["template", "worked-example"]:
    with ZipFile(ROOT / f"downloads/evaluation-{suffix}.xlsx") as archive:
        xml = {name: ET.fromstring(archive.read(name)) for name in archive.namelist() if name.endswith((".xml", ".rels"))}
        names = [s.get("name") for s in xml["xl/workbook.xml"].findall("s:sheets/s:sheet", NS)]
        assert names == ["Comparison", "Queries", "Records", "Runs"]
        assert not any("vbaProject" in name or "externalLink" in name for name in archive.namelist())
        for name, table in xml.items():
            if name.startswith("xl/tables/"):
                headers = [c.get("name") for c in table.findall("s:tableColumns/s:tableColumn", NS)]
                assert len(headers) == len(set(headers)), (name, "duplicate table headers")
                assert table.find("s:autoFilter", NS) is not None, (name, "missing filter")
        for i in range(1, 5):
            sheet = xml[f"xl/worksheets/sheet{i}.xml"]
            errors = sheet.findall("s:sheetData/s:row/s:c[@t='e']", NS)
            assert not errors, [(e.get("r"), e.findtext("s:v", namespaces=NS)) for e in errors]
            assert sheet.find("s:sheetViews/s:sheetView/s:pane", NS) is not None
        comparison = xml["xl/worksheets/sheet1.xml"]
        assert cell(comparison, "B4") == 10
        assert comparison.find("s:sheetData/s:row/s:c[@r='I55']/s:f", NS) is not None
        if suffix == "worked-example":
            expected = {"C6": "Ready", "D6": 10, "E6": 10, "F6": 2, "G6": 6, "H6": 10,
                        "I6": .2, "J6": .6, "K6": .4, "L6": 5, "M6": 1, "N6": 3, "O6": .2, "P6": .6, "Q6": .4}
            for address, value in expected.items():
                actual = cell(comparison, address)
                assert actual == value or (isinstance(value, (float, int)) and abs(actual-value) < 1e-9), (address, actual, value)
        else:
            for row in range(6, 11):
                assert cell(comparison, f"C{row}") == "Write relevance criteria"
                assert cell(comparison, f"I{row}") == ""
                assert cell(comparison, f"O{row}") == ""
            records = xml["xl/worksheets/sheet3.xml"]
            assert cell(records, "A6") == ""
            assert cell(comparison, "A11") == ""

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])

pages = {}
for name in ["evaluation-kit.html", "search-textbook.html", "teaching-notes.html"]:
    pages[name] = Links((ROOT / name).read_text(encoding="utf-8"))
    assert len(pages[name].ids) == len(set(pages[name].ids)), name
for name, page in pages.items():
    for href in page.hrefs:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / unquote(url.path)) if url.path else ROOT / name
        assert target.is_file(), (name, href, "missing file")
        if url.fragment and target.suffix == ".html":
            destination = pages.get(target.name) or Links(target.read_text(encoding="utf-8"))
            assert unquote(url.fragment) in destination.ids, (name, href, "missing anchor")
assert pages["search-textbook.html"].hrefs.count("evaluation-kit.html") == 3
assert "evaluation-kit.html" in pages["teaching-notes.html"].hrefs
print("PASS: both XLSX packages, cached results, 50-query capacity, blank template, Figure 14.1 fixture, tables, filters and local links.")
