# -*- coding: utf-8 -*-
"""Read-only structural audit for search-textbook.html.

The report is deliberately based on source offsets and regex-scoped element
ranges. It never parses and reserializes the book, so running it cannot alter
the HTML. By default it writes baseline.json; pass another output path as the
first argument when producing a later phase or final audit.
"""

from __future__ import annotations

import bisect
import collections
import hashlib
import html as html_module
import io
import json
import os
import re
import sys
from datetime import datetime, timezone


REPO = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(REPO, "search-textbook.html")
OUTPUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(REPO, "baseline.json")

with open(BOOK, "rb") as handle:
    source_bytes = handle.read()
source = source_bytes.decode("utf-8")


def text_of(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html_module.unescape(without_tags)).strip()


def masked_text(document: str) -> str:
    """Mask non-visible source while preserving every character offset."""
    masked = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        lambda match: " " * len(match.group(0)),
        document,
        flags=re.I | re.S,
    )
    return re.sub(r"<[^>]+>", lambda match: " " * len(match.group(0)), masked)


def text_pass_source(document: str) -> str:
    """Mask script/style blocks but retain markup, matching the plan's audit pass."""
    return re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        lambda match: " " * len(match.group(0)),
        document,
        flags=re.I | re.S,
    )


def attr(open_tag: str, name: str) -> str:
    match = re.search(r"\b%s=([\"'])(.*?)\1" % re.escape(name), open_tag, re.I | re.S)
    return html_module.unescape(match.group(2)) if match else ""


def element_range(document: str, open_start: int, tag_name: str) -> tuple[int, int]:
    """Return the range of an element, accounting for same-name nesting."""
    open_end = document.index(">", open_start) + 1
    depth = 1
    token_re = re.compile(r"<%s\b[^>]*>|</%s\s*>" % (tag_name, tag_name), re.I)
    for match in token_re.finditer(document, open_end):
        if match.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return open_start, match.end()
        else:
            depth += 1
    raise ValueError("unclosed <%s> at character %d" % (tag_name, open_start))


def ranges_for_opening(document: str, pattern: str, tag_name: str) -> list[tuple[int, int]]:
    return [element_range(document, match.start(), tag_name) for match in re.finditer(pattern, document, re.I | re.S)]


def in_ranges(position: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= position < end for start, end in ranges)


def top_level_sections(document: str, low: int, high: int) -> list[dict]:
    sections = []
    depth = 0
    start = None
    open_tag = ""
    token_re = re.compile(r"<section\b[^>]*>|</section\s*>", re.I)
    for match in token_re.finditer(document, low, high):
        if match.group(0).startswith("</"):
            depth -= 1
            if depth == 0 and start is not None:
                sections.append({"start": start, "end": match.end(), "open_tag": open_tag})
        else:
            if depth == 0:
                start = match.start()
                open_tag = match.group(0)
            depth += 1
    if depth:
        raise ValueError("unbalanced top-level <section> elements")
    return sections


def line_number(position: int) -> int:
    return source.count("\n", 0, position) + 1


text_pass = text_pass_source(source)
visible = masked_text(source)

article_start = source.index('<article id="article">')
footnotes_start = source.index('<section class="footnotes">')
article_end = footnotes_start
backmatter_start = source.index('<section class="part-divider backmatter-divider" id="backmatter">')

toc_ranges = []
for toc_id in ("toc-list", "mobile-toc-list"):
    match = re.search(r'<ol\b[^>]*\bid="%s"[^>]*>' % toc_id, source, re.I)
    if match:
        toc_ranges.append(element_range(source, match.start(), "ol"))
nav_ranges = ranges_for_opening(source, r'<nav\b[^>]*class="[^"]*\bchapter-nav\b[^"]*"[^>]*>', "nav")
chapter_head_ranges = ranges_for_opening(source, r'<header\b[^>]*class="[^"]*\bchapter-head\b[^"]*"[^>]*>', "header")

heading_re = re.compile(r'<h([23])\b([^>]*)>(.*?)</h\1\s*>', re.I | re.S)
headings = []
for match in heading_re.finditer(source):
    headings.append(
        {
            "level": int(match.group(1)),
            "id": attr(match.group(2), "id"),
            "text": text_of(match.group(3)).rstrip("#").strip(),
            "position": match.start(),
        }
    )
heading_positions = [heading["position"] for heading in headings]


def enclosing_headings(position: int) -> tuple[dict | None, dict | None]:
    index = bisect.bisect_right(heading_positions, position) - 1
    h2 = None
    h3 = None
    while index >= 0:
        heading = headings[index]
        if heading["level"] == 3 and h3 is None:
            h3 = heading
        if heading["level"] == 2:
            h2 = heading
            if h3 and h3["position"] < h2["position"]:
                h3 = None
            break
        index -= 1
    return h2, h3


def zone_for(position: int) -> str:
    if in_ranges(position, toc_ranges):
        return "toc"
    if in_ranges(position, nav_ranges):
        return "nav"
    if in_ranges(position, chapter_head_ranges):
        return "chapter-head"
    if position >= backmatter_start:
        return "end-matter"
    return "prose"


reference_re = re.compile(r"\b(Chapter|Chapters|Appendix|Appendices)\s+[0-9A-F]\b")
markup_reference_count = len(list(reference_re.finditer(text_pass)))
references = []
for match in reference_re.finditer(visible):
    h2, h3 = enclosing_headings(match.start())
    context_start = max(0, match.start() - 120)
    context_end = min(len(source), match.end() + 120)
    context = re.sub(r"\s+", " ", html_module.unescape(source[context_start:context_end])).strip()
    references.append(
        {
            "match": match.group(0),
            "position": match.start(),
            "utf8_byte_position": len(source[: match.start()].encode("utf-8")),
            "line": line_number(match.start()),
            "zone": zone_for(match.start()),
            "h2": {"id": h2["id"], "text": h2["text"]} if h2 else None,
            "h3": {"id": h3["id"], "text": h3["text"]} if h3 else None,
            "context": context,
        }
    )


section_records = []
for section in top_level_sections(source, article_start, article_end):
    body = source[section["start"] : section["end"]]
    h2_match = re.search(r'<h2\b([^>]*)>(.*?)</h2\s*>', body, re.I | re.S)
    eyebrow_match = re.search(r'<p\b[^>]*class="[^"]*\bchapter-eyebrow\b[^"]*"[^>]*>(.*?)</p\s*>', body, re.I | re.S)
    visible_body = masked_text(body)
    words = re.findall(r"\b[\w’'-]+\b", html_module.unescape(visible_body), re.UNICODE)
    record = {
        "section_id": attr(section["open_tag"], "id"),
        "classes": attr(section["open_tag"], "class").split(),
        "h2_id": attr(h2_match.group(1), "id") if h2_match else "",
        "h2": text_of(h2_match.group(2)).rstrip("#").strip() if h2_match else "",
        "eyebrow": text_of(eyebrow_match.group(1)) if eyebrow_match else "",
        "start": section["start"],
        "end": section["end"],
        "word_count": len(words),
        "source_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }
    section_records.append(record)


def owner_section(position: int) -> dict | None:
    for section in section_records:
        if section["start"] <= position < section["end"]:
            return section
    return None


asset_elements = []
asset_node_re = re.compile(
    r'<(?P<tag>p|span)\b(?P<attrs>[^>]*class="[^"]*\basset-label(?:-inline)?\b[^"]*"[^>]*)>'
    r'(?P<body>.*?)</(?P=tag)\s*>',
    re.I | re.S,
)
asset_text_re = re.compile(r"\b(Figure|Table)\s+([0-9A-F]+)\.(\d+)\b")
for node in asset_node_re.finditer(source):
    label_match = asset_text_re.search(text_of(node.group("body")))
    if not label_match:
        continue
    owner = owner_section(node.start())
    asset_elements.append(
        {
            "label": label_match.group(0),
            "kind": label_match.group(1),
            "prefix": label_match.group(2),
            "index": int(label_match.group(3)),
            "id": attr(node.group(0).split(">", 1)[0] + ">", "id"),
            "position": node.start(),
            "line": line_number(node.start()),
            "section_id": owner["section_id"] if owner else "",
            "section_h2_id": owner["h2_id"] if owner else "",
            "section_h2": owner["h2"] if owner else "",
            "section_eyebrow": owner["eyebrow"] if owner else "",
            "source_sha256": hashlib.sha256(node.group(0).encode("utf-8")).hexdigest(),
        }
    )

asset_label_ranges = [(node.start(), node.end()) for node in asset_node_re.finditer(source)]
asset_index_ranges = []
for index_id in ("figure-index", "table-index"):
    match = re.search(r'<ol\b[^>]*\bid="%s"[^>]*>' % index_id, source, re.I)
    if match:
        asset_index_ranges.append(element_range(source, match.start(), "ol"))

asset_occurrences = []
for match in asset_text_re.finditer(visible):
    owner = owner_section(match.start())
    h2, h3 = enclosing_headings(match.start())
    last_open = source.rfind("<", 0, match.start())
    last_close = source.rfind(">", 0, match.start())
    if in_ranges(match.start(), asset_label_ranges):
        role = "label"
    elif in_ranges(match.start(), asset_index_ranges):
        role = "index"
    elif last_open > last_close:
        role = "attribute"
    else:
        role = "prose-reference"
    asset_occurrences.append(
        {
            "label": match.group(0),
            "kind": match.group(1),
            "prefix": match.group(2),
            "index": int(match.group(3)),
            "role": role,
            "position": match.start(),
            "line": line_number(match.start()),
            "zone": zone_for(match.start()),
            "section_id": owner["section_id"] if owner else "",
            "section_h2_id": owner["h2_id"] if owner else "",
            "section_h2": owner["h2"] if owner else "",
            "section_eyebrow": owner["eyebrow"] if owner else "",
            "h3": {"id": h3["id"], "text": h3["text"]} if h3 else None,
        }
    )


id_matches = list(re.finditer(r'\bid="([^"]+)"', source))
href_matches = list(re.finditer(r'href="#([^"]+)"', source))
id_counts = collections.Counter(match.group(1) for match in id_matches)
href_counts = collections.Counter(match.group(1) for match in href_matches)

script_records = []
for index, match in enumerate(re.finditer(r'<script\b([^>]*)>(.*?)</script\s*>', source, re.I | re.S), 1):
    attrs = match.group(1)
    body = match.group(2)
    structure_hits = sorted(
        word
        for word in ("toc", "chapter", "appendix", "figure", "table", "footnote", "reading", "eyebrow")
        if re.search(r"\b%s\b" % word, body, re.I)
    )
    script_records.append(
        {
            "index": index,
            "start": match.start(),
            "line": line_number(match.start()),
            "src": attr(match.group(0).split(">", 1)[0] + ">", "src"),
            "attributes": re.sub(r"\s+", " ", attrs).strip(),
            "characters": len(body),
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "structure_terms": structure_hits,
        }
    )

style_records = [
    {
        "index": index,
        "start": match.start(),
        "line": line_number(match.start()),
        "characters": len(match.group(1)),
        "sha256": hashlib.sha256(match.group(1).encode("utf-8")).hexdigest(),
    }
    for index, match in enumerate(re.finditer(r'<style\b[^>]*>(.*?)</style\s*>', source, re.I | re.S), 1)
]

footnote_ref_re = re.compile(
    r'<sup id="fnref:(?P<key>[^"]+)"><a class="footnote-ref" href="#fn:(?P=key)">(?P<num>\d+)</a></sup>'
)
footnote_refs = [
    {"key": match.group("key"), "number": int(match.group("num")), "position": match.start()}
    for match in footnote_ref_re.finditer(source[:footnotes_start])
]
footnote_notes = [match.group(1) for match in re.finditer(r'<li id="fn:([^"]+)">', source[footnotes_start:])]
ref_numbers = [item["number"] for item in footnote_refs]
footnote_scheme = "global-sequential" if ref_numbers == list(range(1, len(ref_numbers) + 1)) else "non-global"

end_matter_headings = [
    {"level": heading["level"], "id": heading["id"], "text": heading["text"], "position": heading["position"]}
    for heading in headings
    if heading["position"] >= backmatter_start
]

asset_prefix_counts = collections.Counter(asset["prefix"] for asset in asset_occurrences)
zone_counts = collections.Counter(reference["zone"] for reference in references)
match_counts = collections.Counter(reference["match"] for reference in references)

expected_asset_prefixes = {
    "1": 10, "2": 10, "3": 8, "4": 6, "5": 20, "6": 14, "7": 20,
    "8": 15, "9": 17, "10": 10, "11": 7, "12": 6, "13": 6,
    "A": 2, "B": 4, "C": 10, "D": 8, "E": 10, "F": 12,
}
app_f_record = next(section for section in section_records if section["section_id"] == "app-F")
app_f_labels = [asset for asset in asset_elements if asset["section_id"] == "app-F"]

report = {
    "metadata": {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "book": os.path.relpath(BOOK, REPO).replace(os.sep, "/"),
        "characters": len(source),
        "utf8_bytes": len(source_bytes),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
    },
    "summary": {
        "textual_reference_count": len(references),
        "markup_inclusive_reference_count": markup_reference_count,
        "reference_zone_counts": dict(sorted(zone_counts.items())),
        "reference_match_counts": dict(sorted(match_counts.items())),
        "numbered_asset_count": len(asset_occurrences),
        "labelled_asset_object_count": len(asset_elements),
        "asset_prefix_counts": dict(sorted(asset_prefix_counts.items())),
        "id_count": len(id_matches),
        "unique_id_count": len(id_counts),
        "internal_href_count": len(href_matches),
        "unique_internal_href_targets": len(href_counts),
        "duplicate_ids": sorted(key for key, count in id_counts.items() if count > 1),
        "broken_internal_hrefs": sorted(key for key in href_counts if key not in id_counts),
        "unreferenced_ids": sorted(key for key in id_counts if key not in href_counts),
        "footnote_ref_count": len(footnote_refs),
        "footnote_note_count": len(footnote_notes),
        "footnote_scheme": footnote_scheme,
        "footnote_missing_notes": sorted(set(item["key"] for item in footnote_refs) - set(footnote_notes)),
        "footnote_orphan_notes": sorted(set(footnote_notes) - set(item["key"] for item in footnote_refs)),
        "appendix_f_textual_reference_count": match_counts.get("Appendix F", 0),
        "legacy_anchor_count": len(re.findall(r'class="[^"]*\blegacy-anchor\b', source)),
        "placeholder_token_count": source.count("%%"),
    },
    "expected_baseline_comparison": {
        "textual_references": {
            "expected_approx": 200,
            "actual_visible_text": len(references),
            "actual_including_markup_attributes": markup_reference_count,
        },
        "assets": {
            "expected_chapter_occurrences": 149,
            "actual_chapter_occurrences": sum(count for prefix, count in asset_prefix_counts.items() if prefix.isdigit()),
            "expected_total_with_appendices": sum(expected_asset_prefixes.values()),
            "actual_total_with_appendices": len(asset_occurrences),
        },
        "asset_prefix_counts_expected": expected_asset_prefixes,
        "asset_prefix_count_deltas": {
            key: asset_prefix_counts.get(key, 0) - expected
            for key, expected in expected_asset_prefixes.items()
        },
    },
    "textual_references": references,
    "numbered_assets": asset_occurrences,
    "labelled_asset_objects": asset_elements,
    "anchors": {
        "id_counts": dict(sorted(id_counts.items())),
        "href_target_counts": dict(sorted(href_counts.items())),
    },
    "h2_sections": section_records,
    "scripts": script_records,
    "styles": style_records,
    "footnotes": {"refs": footnote_refs, "note_keys": footnote_notes},
    "end_matter_headings": end_matter_headings,
    "guards": {
        "appendix_f": {
            "start": app_f_record["start"],
            "end": app_f_record["end"],
            "word_count": app_f_record["word_count"],
            "source_sha256": app_f_record["source_sha256"],
            "textual_appendix_f_reference_count": match_counts.get("Appendix F", 0),
            "label_objects": [
                {
                    "label": asset["label"],
                    "id": asset["id"],
                    "source_sha256": asset["source_sha256"],
                }
                for asset in app_f_labels
            ],
        },
        "exclusion_exact_text_counts": {
            phrase: visible.count(phrase)
            for phrase in (
                "Chapters 1, 2 and 6",
                "Chapters 1 to 4",
                "Chapters 2 to 4",
                "Chapters 2 and 3",
                "Chapters 3 and 4",
                "Chapters 3–4",
            )
        },
    },
}

with io.open(OUTPUT, "w", encoding="utf-8", newline="\n") as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write("\n")

print("wrote", os.path.relpath(OUTPUT, REPO))
print("textual references:", len(references), dict(sorted(zone_counts.items())))
print("numbered asset occurrences:", len(asset_occurrences), dict(sorted(asset_prefix_counts.items())))
print("labelled asset objects:", len(asset_elements))
print("ids / hrefs:", len(id_counts), "/", len(href_counts))
print("broken hrefs:", len(report["summary"]["broken_internal_hrefs"]))
print("duplicate ids:", len(report["summary"]["duplicate_ids"]))
print("footnotes:", len(footnote_refs), footnote_scheme)
