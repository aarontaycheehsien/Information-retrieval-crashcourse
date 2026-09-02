# -*- coding: utf-8 -*-
"""Controlled, byte-preserving restructuring passes for search-textbook.html.

Each phase uses exact unique anchors, edits only named source ranges, validates
the result in memory, and writes only after all checks pass. Use --dry-run to
exercise a phase without changing the book.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re


REPO = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(REPO, "search-textbook.html")
BASELINE = os.path.join(REPO, "baseline.json")
PHASE2_AUDIT = os.path.join(REPO, "phase2-audit.json")


def read_bytes(path: str) -> tuple[bytes, str]:
    with open(path, "rb") as handle:
        raw = handle.read()
    return raw, raw.decode("utf-8")


def unique_index(text: str, needle: str, label: str | None = None) -> int:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError("%s: expected one match, found %d" % (label or needle, count))
    return text.index(needle)


def element_range(text: str, start: int, tag: str) -> tuple[int, int]:
    open_end = text.index(">", start) + 1
    depth = 1
    token_re = re.compile(r"<%s\b[^>]*>|</%s\s*>" % (tag, tag), re.I)
    for match in token_re.finditer(text, open_end):
        if match.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return start, match.end()
        else:
            depth += 1
    raise RuntimeError("unclosed <%s> at character %d" % (tag, start))


def section_range(text: str, section_id: str) -> tuple[int, int]:
    match = re.search(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(section_id), text)
    if not match:
        raise RuntimeError("section not found: " + section_id)
    if len(re.findall(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(section_id), text)) != 1:
        raise RuntimeError("section id is not unique: " + section_id)
    return element_range(text, match.start(), "section")


def section_text(text: str, section_id: str) -> str:
    start, end = section_range(text, section_id)
    return text[start:end]


def first_element(block: str, opening: str, tag: str, after: int = 0) -> tuple[int, int, str]:
    start = block.index(opening, after)
    low, high = element_range(block, start, tag)
    return low, high, block[low:high]


def stage_map_from(section: str) -> str:
    start = section.index('<div class="stage-map"')
    low, high = element_range(section, start, "div")
    return section[low:high]


def close_parts(block: str) -> tuple[str, list[str], str]:
    ol_start = unique_index(block, "<ol>", "chapter-close <ol>")
    ol_end = block.index("</ol>", ol_start)
    items = re.findall(r"<li>.*?</li>", block[ol_start:ol_end], re.S)
    if not items:
        raise RuntimeError("chapter close contains no list items")
    prefix = block[: ol_start + len("<ol>")]
    suffix = block[ol_end + len("</ol>") :]
    return prefix, items, suffix


def build_close(block: str, indexes: list[int], eol: str, keep_suffix: bool) -> str:
    prefix, items, suffix = close_parts(block)
    selected = "".join(items[index] for index in indexes)
    if keep_suffix:
        return prefix + selected + "</ol>" + suffix
    return prefix + selected + "</ol>" + eol + "<!-- TODO-PROSE -->" + eol + "</aside>"


def self_check_parts(block: str) -> tuple[str, list[str], str]:
    details = list(re.finditer(r'<details class="self-check-q">.*?</details>', block, re.S))
    if not details:
        raise RuntimeError("self-check contains no questions")
    return block[: details[0].start()], [match.group(0) for match in details], block[details[-1].end() :]


def build_self_check(block: str, indexes: list[int], eol: str, mark_todo: bool = False) -> str:
    prefix, questions, suffix = self_check_parts(block)
    selected = eol.join(questions[index] for index in indexes)
    marker = (eol + "<!-- TODO-PROSE -->") if mark_todo else ""
    if selected:
        selected += marker
    else:
        selected = "<!-- TODO-PROSE -->"
    return prefix + selected + eol + suffix.lstrip("\r\n")


def chapter_nav(prev_href: str, prev_text: str, next_href: str, next_text: str) -> str:
    return (
        '<nav class="chapter-nav" aria-label="Chapter navigation">'
        '<a class="cnav prev" href="#%s"><span>Previous</span>%s</a>'
        '<a class="cnav next" href="#%s"><span>Next</span>%s</a>'
        "</nav>"
    ) % (prev_href, prev_text, next_href, next_text)


def replace_nav(section: str, replacement: str) -> str:
    low, high, _ = first_element(section, '<nav class="chapter-nav"', "nav")
    return section[:low] + replacement + section[high:]


def new_header(
    eyebrow_token: str,
    time_token: str,
    heading_id: str,
    title: str,
    question: str,
    stage_map: str,
    eol: str,
) -> str:
    return eol.join(
        [
            '<header class="chapter-head"><p class="chapter-eyebrow">Chapter %s</p>' % eyebrow_token,
            '<p class="chapter-meta">About %s min</p>' % time_token,
            '<h2 id="%s">%s</h2>' % (heading_id, title),
            '<p class="chapter-question"><span>Central question</span>%s</p>' % question,
            stage_map,
            '<div class="chapter-orient"><!-- TODO-PROSE --></div></header>',
        ]
    )


def hash_element_bodies(document: str, tag: str) -> list[str]:
    return [
        hashlib.sha256(match.group(1).encode("utf-8")).hexdigest()
        for match in re.finditer(r'<%s\b[^>]*>(.*?)</%s\s*>' % (tag, tag), document, re.I | re.S)
    ]


def validate_common(document: str, baseline: dict, require_app_f_exact: bool) -> None:
    ids = re.findall(r'\bid="([^"]+)"', document)
    duplicates = sorted(key for key, count in __import__("collections").Counter(ids).items() if count > 1)
    if duplicates:
        raise RuntimeError("duplicate ids: " + ", ".join(duplicates))
    hrefs = re.findall(r'href="#([^"]+)"', document)
    broken = sorted(set(hrefs) - set(ids))
    if broken:
        raise RuntimeError("broken internal hrefs: " + ", ".join(broken))

    ref_keys = re.findall(r'<sup id="fnref:([^"]+)"><a class="footnote-ref" href="#fn:[^"]+">\d+</a></sup>', document)
    note_keys = re.findall(r'<li id="fn:([^"]+)">', document)
    if len(ref_keys) != len(set(ref_keys)) or set(ref_keys) != set(note_keys):
        raise RuntimeError("footnote ref/note pairs are incomplete or duplicated")

    expected_styles = [item["sha256"] for item in baseline["styles"]]
    expected_scripts = [item["sha256"] for item in baseline["scripts"]]
    if hash_element_bodies(document, "style") != expected_styles:
        raise RuntimeError("style blocks changed")
    if hash_element_bodies(document, "script") != expected_scripts:
        raise RuntimeError("script blocks changed")

    if require_app_f_exact:
        app_f = section_text(document, "app-F")
        actual = hashlib.sha256(app_f.encode("utf-8")).hexdigest()
        expected = baseline["guards"]["appendix_f"]["source_sha256"]
        if actual != expected:
            raise RuntimeError("Appendix F changed during a phase that must leave it byte-identical")


def phase1(document: str, baseline: dict) -> str:
    if 'id="sec-retrieval-encoder"' in document or 'id="sec-hybrid-and-fusion"' in document:
        raise RuntimeError("Phase 1 appears to have been applied already")
    eol = "\r\n" if "\r\n" in document else "\n"

    ch5_start, ch5_end = section_range(document, "sec-embeddings")
    ch5 = document[ch5_start:ch5_end]
    ch5_split_marker = '<span id="how-dense-models-receive-text" class="legacy-anchor"></span><h3 id="model-tokens-are-not-indexed-terms">'
    ch5_split = unique_index(ch5, ch5_split_marker, "Chapter 5 split boundary")
    close5_start, close5_end, close5 = first_element(ch5, '<aside class="chapter-close"', "aside", ch5_split)
    self5_start, self5_end, self5 = first_element(ch5, '<section class="self-check"', "section", close5_end)
    _, _, nav5 = first_element(ch5, '<nav class="chapter-nav"', "nav", self5_end)
    stage5 = stage_map_from(ch5)
    if len(close_parts(close5)[1]) != 3 or len(self_check_parts(self5)[1]) != 3:
        raise RuntimeError("unexpected Chapter 5 close/self-check structure")

    ch5_prefix = ch5[:ch5_split]
    old_title5 = '<h2 id="embeddings">Embeddings and the retrieval encoder</h2>'
    if ch5_prefix.count(old_title5) != 1:
        raise RuntimeError("Chapter 5 title did not match uniquely")
    ch5_prefix = ch5_prefix.replace(
        old_title5,
        '<h2 id="embeddings">Embeddings: what the learnt geometry encodes</h2>',
    )
    ch5_close = build_close(close5, [0], eol, keep_suffix=False)
    ch5_checks = build_self_check(self5, [], eol)
    ch5_nav = chapter_nav(
        "exercise1", "Application exercise I", "retrieval-encoder", "From language model to retrieval encoder"
    )
    new_ch5 = ch5_prefix + ch5_close + eol + ch5_checks + eol + ch5_nav + "</section>"

    ch6_header = new_header(
        "%%NEW6%%",
        "%%TIME6%%",
        "retrieval-encoder",
        "From language model to retrieval encoder",
        "How does a language model's internal representation become something a search index can use?",
        stage5,
        eol,
    )
    ch6_body = ch5[ch5_split:close5_start]
    ch6_close = build_close(close5, [1, 2], eol, keep_suffix=True)
    ch6_checks = build_self_check(self5, [0, 1, 2], eol)
    ch6_nav = chapter_nav(
        "embeddings", "Embeddings: what the learnt geometry encodes", "dense-at-scale", "Dense retrieval at collection scale"
    )
    new_ch6 = (
        '<section class="chapter" id="sec-retrieval-encoder">'
        + ch6_header
        + eol
        + ch6_body
        + ch6_close
        + eol
        + ch6_checks
        + eol
        + ch6_nav
        + "</section>"
    )

    ch8_start, ch8_end = section_range(document, "sec-reranking-and-hybrid")
    ch8 = document[ch8_start:ch8_end]
    hybrid_marker = '<h3 id="why-hybrid-retrieval-remains-attractive">'
    hybrid_start = unique_index(ch8, hybrid_marker, "Chapter 8 hybrid split boundary")
    close8_start, close8_end, close8 = first_element(ch8, '<aside class="chapter-close"', "aside", hybrid_start)
    self8_start, self8_end, self8 = first_element(ch8, '<section class="self-check"', "section", close8_end)
    stage8 = stage_map_from(ch8)
    if len(close_parts(close8)[1]) != 5 or len(self_check_parts(self8)[1]) != 3:
        raise RuntimeError("unexpected Chapter 8 close/self-check structure")

    app_e_start, app_e_end = section_range(document, "app-E")
    app_e = document[app_e_start:app_e_end]
    rrf_start = unique_index(app_e, '<h3 id="appendix-how-rrf-combines-ranked-lists">', "RRF section")
    rrf_end = app_e.index('<h3 id="appendix-learning-to-rank">', rrf_start)
    rrf = app_e[rrf_start:rrf_end]
    old_rrf_id = "appendix-how-rrf-combines-ranked-lists"
    new_rrf_id = "how-reciprocal-rank-fusion-combines-ranked-lists"
    if rrf.count(old_rrf_id) != 2:
        raise RuntimeError("RRF heading id/href structure was not the expected pair")
    moved_rrf = rrf.replace(old_rrf_id, new_rrf_id)
    app_e_alias = '<span id="%s" class="legacy-anchor"></span>%s' % (old_rrf_id, eol)
    new_app_e = app_e[:rrf_start] + app_e_alias + app_e[rrf_end:]

    ch9_prefix = ch8[:hybrid_start]
    old_title8 = '<h2 id="reranking-and-hybrid">Reranking, multi-stage and hybrid retrieval</h2>'
    if ch9_prefix.count(old_title8) != 1:
        raise RuntimeError("Chapter 8 title did not match uniquely")
    ch9_prefix = ch9_prefix.replace(
        old_title8,
        '<h2 id="reranking-and-hybrid">Reranking and multi-stage retrieval</h2>',
    )
    ch9_close = build_close(close8, [0, 1, 2], eol, keep_suffix=False)
    ch9_checks = build_self_check(self8, [0], eol, mark_todo=True)
    ch9_nav = chapter_nav(
        "representations-and-units",
        "Representations and indexed units",
        "hybrid-and-fusion",
        "Hybrid retrieval and rank fusion",
    )
    new_ch9 = ch9_prefix + ch9_close + eol + ch9_checks + eol + ch9_nav + "</section>"

    hybrid_body = ch8[hybrid_start:close8_start]
    two_hybrids = unique_index(
        hybrid_body, '<h3 id="two-hybrids-that-combine-differently">', "two-hybrids insertion point"
    )
    hybrid_body = hybrid_body[:two_hybrids] + moved_rrf + hybrid_body[two_hybrids:]
    ch10_header = new_header(
        "%%NEW10%%",
        "%%TIME10%%",
        "hybrid-and-fusion",
        "Hybrid retrieval and rank fusion",
        "When a system runs more than one retriever, how are their answers combined—and what does the combination hide?",
        stage8,
        eol,
    )
    ch10_close = build_close(close8, [3, 4], eol, keep_suffix=True)
    ch10_checks = build_self_check(self8, [1, 2], eol)
    ch10_nav = chapter_nav(
        "reranking-and-hybrid",
        "Reranking and multi-stage retrieval",
        "query-transformation",
        "Understanding, transforming and routing queries",
    )
    new_ch10 = (
        '<section class="chapter" id="sec-hybrid-and-fusion">'
        + ch10_header
        + eol
        + hybrid_body
        + ch10_close
        + eol
        + ch10_checks
        + eol
        + ch10_nav
        + "</section>"
    )

    dense_start, dense_end = section_range(document, "sec-dense-at-scale")
    dense = document[dense_start:dense_end]
    new_dense = replace_nav(
        dense,
        chapter_nav(
            "retrieval-encoder",
            "From language model to retrieval encoder",
            "representations-and-units",
            "Representations and indexed units",
        ),
    )

    query_start, query_end = section_range(document, "sec-query-transformation")
    query = document[query_start:query_end]
    new_query = replace_nav(
        query,
        chapter_nav(
            "hybrid-and-fusion",
            "Hybrid retrieval and rank fusion",
            "exercise2",
            "Application exercise II",
        ),
    )

    replacements = [
        (ch5_start, ch5_end, new_ch5 + new_ch6),
        (dense_start, dense_end, new_dense),
        (ch8_start, ch8_end, new_ch9 + new_ch10),
        (query_start, query_end, new_query),
        (app_e_start, app_e_end, new_app_e),
    ]
    for start, end, replacement in sorted(replacements, reverse=True):
        document = document[:start] + replacement + document[end:]

    for required in (
        'id="sec-retrieval-encoder"',
        'id="retrieval-encoder"',
        'id="sec-hybrid-and-fusion"',
        'id="hybrid-and-fusion"',
        'id="how-reciprocal-rank-fusion-combines-ranked-lists"',
        'id="appendix-how-rrf-combines-ranked-lists" class="legacy-anchor"',
    ):
        if document.count(required) != 1:
            raise RuntimeError("required Phase 1 marker is missing or duplicated: " + required)
    validate_common(document, baseline, require_app_f_exact=True)
    return document


def phase2(document: str, baseline: dict) -> str:
    if 'id="sec-retrieval-encoder"' not in document or 'id="sec-hybrid-and-fusion"' not in document:
        raise RuntimeError("Phase 2 requires the Phase 1 structure")
    if "%%ASSET" in document:
        raise RuntimeError("unresolved asset token found before Phase 2")
    original_tokens = sorted(set(re.findall(r"%%[A-Z0-9]+%%", document)))
    substitutions: list[tuple[str, int]] = []

    def exact(old: str, token: str, label: str) -> None:
        nonlocal document
        count = document.count(old)
        if count == 0:
            raise RuntimeError("Phase 2 target not found: " + label)
        document = document.replace(old, token)
        substitutions.append((label, count))

    # The second half of old Chapter 5 becomes the new Chapter 6.
    exact("Table 5.1", "Table %%ASSETT61%%", "Table 5.1 -> 6.1")
    exact("tbl-5-1", "%%ASSETIDT61%%", "tbl-5-1 -> tbl-6-1")
    for old_index, new_index in ((7, 1), (8, 2), (9, 3)):
        exact(
            "Figure 5.%d" % old_index,
            f"Figure %%ASSETF6{new_index}%%",
            "Figure 5.%d -> 6.%d" % (old_index, new_index),
        )
        exact(
            "fig-5-%d" % old_index,
            f"%%ASSETIDF6{new_index}%%",
            "fig-5-%d -> fig-6-%d" % (old_index, new_index),
        )

    # Existing chapter prefixes shift around the two inserted chapters.
    for old_prefix, new_prefix in ((13, 15), (12, 14), (11, 13), (10, 12), (9, 11), (8, 9), (7, 8), (6, 7)):
        text_pattern = re.compile(r"\b(Figure|Table) %d\.(\d+)\b" % old_prefix)
        id_pattern = re.compile(r"\b(fig|tbl)-%d-(\d+)\b" % old_prefix)
        text_matches = len(text_pattern.findall(document))
        id_matches = len(id_pattern.findall(document))
        if text_matches == 0 or id_matches == 0:
            raise RuntimeError("no asset text/id matches for Chapter %d" % old_prefix)
        document = text_pattern.sub(
            lambda match: f"{match.group(1)} %%ASSETP{new_prefix}%%.{match.group(2)}",
            document,
        )
        document = id_pattern.sub(
            lambda match: f"{match.group(1)}-%%ASSETIDP{new_prefix}%%-{match.group(2)}",
            document,
        )
        substitutions.append(("asset prefix %d -> %d" % (old_prefix, new_prefix), text_matches + id_matches))

    # The worked RRF table moved out of Appendix E with its section.
    exact("Table E.1", "Table %%ASSETT101%%", "Table E.1 -> 10.1")
    exact("tbl-e-1", "%%ASSETIDT101%%", "tbl-e-1 -> tbl-10-1")

    resolutions = {
        "%%ASSETT61%%": "6.1",
        "%%ASSETIDT61%%": "tbl-6-1",
        "%%ASSETF61%%": "6.1",
        "%%ASSETF62%%": "6.2",
        "%%ASSETF63%%": "6.3",
        "%%ASSETIDF61%%": "fig-6-1",
        "%%ASSETIDF62%%": "fig-6-2",
        "%%ASSETIDF63%%": "fig-6-3",
        "%%ASSETT101%%": "10.1",
        "%%ASSETIDT101%%": "tbl-10-1",
    }
    for new_prefix in (15, 14, 13, 12, 11, 9, 8, 7):
        resolutions[f"%%ASSETP{new_prefix}%%"] = str(new_prefix)
        resolutions[f"%%ASSETIDP{new_prefix}%%"] = str(new_prefix)
    for token, value in resolutions.items():
        if token in document:
            document = document.replace(token, value)
    if "%%ASSET" in document:
        raise RuntimeError("Phase 2 left unresolved asset tokens")
    if sorted(set(re.findall(r"%%[A-Z0-9]+%%", document))) != original_tokens:
        raise RuntimeError("Phase 2 changed non-asset placeholder tokens")

    print("asset substitutions:")
    for label, count in substitutions:
        print("  ", label, count)
    validate_common(document, baseline, require_app_f_exact=True)
    return document


def phase3(document: str, baseline: dict) -> str:
    with open(PHASE2_AUDIT, encoding="utf-8") as handle:
        phase2_audit = json.load(handle)
    current_hash = hashlib.sha256(document.encode("utf-8")).hexdigest()
    if current_hash != phase2_audit["metadata"]["sha256"]:
        raise RuntimeError("Phase 3 input does not match the Phase 2 snapshot")

    original_tokens = sorted(set(re.findall(r"%%[A-Z0-9]+%%", document)))
    simple_map = {6: 7, 7: 8, 9: 11, 10: 12, 11: 13, 12: 14, 13: 15}
    expected_counts = {6: 7, 7: 3, 9: 6, 10: 5, 11: 5, 12: 9, 13: 10}
    edits = []
    observed = collections.Counter()
    for reference in phase2_audit["textual_references"]:
        match = re.fullmatch(r"Chapter (\d+)", reference["match"])
        if not match or reference["zone"] not in ("prose", "end-matter"):
            continue
        old_number = int(match.group(1))
        if old_number not in simple_map:
            continue
        start = int(reference["position"])
        old_text = "Chapter %d" % old_number
        if document[start : start + len(old_text)] != old_text:
            raise RuntimeError("Phase 3 position drift at %d for %s" % (start, old_text))
        token = f"%%CHAPTER{simple_map[old_number]}%%"
        edits.append((start, start + len(old_text), token))
        observed[old_number] += 1
    if dict(observed) != expected_counts:
        raise RuntimeError("Phase 3 simple-reference counts changed: %r" % dict(observed))
    for start, end, token in sorted(edits, reverse=True):
        document = document[:start] + token + document[end:]

    ranges = [
        ("Chapters 5 and 6", "%%RANGE5TO7%%", "Chapters 5 to 7", 1),
        ("Chapters 5–6", "%%RANGE5DASH7%%", "Chapters 5–7", 1),
        ("Chapters 8 and 9", "%%RANGE9TO11%%", "Chapters 9 to 11", 1),
        (
            '<a href="#diagnosing-failure">Chapters 11</a>–<a href="#library-practice">13</a>',
            "%%RANGE13TO15LINKED%%",
            '<a href="#diagnosing-failure">Chapters 13</a> to <a href="#library-practice">15</a>',
            2,
        ),
        ("Chapters 11 and 12", "%%RANGE13AND14%%", "Chapters 13 and 14", 1),
        ("Chapters 1 and 12", "%%RANGE1AND14%%", "Chapters 1 and 14", 1),
    ]
    for old, token, _, expected in ranges:
        count = document.count(old)
        if count != expected:
            raise RuntimeError("Phase 3 range %r: expected %d, found %d" % (old, expected, count))
        document = document.replace(old, token)

    app_f_aria_old = 'aria-label="Link to Applying Chapter 13 to active learning"'
    app_f_aria_token = 'aria-label="Link to Applying %%APPFCH15%% to active learning"'
    if document.count(app_f_aria_old) != 1:
        raise RuntimeError("Appendix F heading aria-label did not match uniquely")
    document = document.replace(app_f_aria_old, app_f_aria_token)

    for new_number in simple_map.values():
        document = document.replace(f"%%CHAPTER{new_number}%%", "Chapter %d" % new_number)
    for _, token, replacement, _ in ranges:
        document = document.replace(token, replacement)
    document = document.replace("%%APPFCH15%%", "Chapter 15")

    if sorted(set(re.findall(r"%%[A-Z0-9]+%%", document))) != original_tokens:
        raise RuntimeError("Phase 3 changed or left non-structural placeholder tokens")
    for phrase, expected in baseline["guards"]["exclusion_exact_text_counts"].items():
        if document.count(phrase) != expected:
            raise RuntimeError("exclusion changed: %r" % phrase)
    validate_common(document, baseline, require_app_f_exact=False)
    print("simple Chapter substitutions:", dict(sorted(observed.items())))
    print("range substitutions:", sum(item[3] for item in ranges))
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("phase1", "phase2", "phase3"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    raw, document = read_bytes(BOOK)
    with open(BASELINE, encoding="utf-8") as handle:
        baseline = json.load(handle)

    if args.phase == "phase1":
        updated = phase1(document, baseline)
    elif args.phase == "phase2":
        updated = phase2(document, baseline)
    elif args.phase == "phase3":
        updated = phase3(document, baseline)
    else:
        raise AssertionError(args.phase)

    before_hash = hashlib.sha256(raw).hexdigest()
    updated_raw = updated.encode("utf-8")
    after_hash = hashlib.sha256(updated_raw).hexdigest()
    print("phase:", args.phase)
    print("bytes:", len(raw), "->", len(updated_raw))
    print("sha256:", before_hash, "->", after_hash)
    print("mode:", "dry-run" if args.dry_run else "write")
    if not args.dry_run:
        with open(BOOK, "wb") as handle:
            handle.write(updated_raw)


if __name__ == "__main__":
    main()
