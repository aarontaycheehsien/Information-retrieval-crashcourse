# -*- coding: utf-8 -*-
"""Verify restructuring checkpoints against the approved Phase 0 baseline."""

from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import os
import re
import subprocess
from html.parser import HTMLParser


REPO = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(REPO, "search-textbook.html")
BASELINE_JSON = os.path.join(REPO, "baseline.json")
BASELINE_COMMIT = "65469bbd4e7aa811db0f0511ae10a4386299308f"
PHASE2_COMMIT = "7b38db9"
PHASE3_COMMIT = "51e644c"
PHASE4_COMMIT = "1f3ab69"
PHASE5_COMMIT = "5d9575a"


def element_range(text: str, start: int, tag: str) -> tuple[int, int]:
    open_end = text.index(">", start) + 1
    depth = 1
    for match in re.finditer(r"<%s\b[^>]*>|</%s\s*>" % (tag, tag), text[open_end:], re.I):
        token = match.group(0)
        depth += -1 if token.startswith("</") else 1
        if depth == 0:
            return start, open_end + match.end()
    raise RuntimeError("unclosed <%s>" % tag)


def section(text: str, section_id: str) -> str:
    matches = list(re.finditer(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(section_id), text))
    if len(matches) != 1:
        raise RuntimeError("expected one section %s, found %d" % (section_id, len(matches)))
    start, end = element_range(text, matches[0].start(), "section")
    return text[start:end]


def remove_elements(fragment: str, tag: str, opening_pattern: str) -> str:
    while True:
        match = re.search(opening_pattern, fragment, re.I | re.S)
        if not match:
            return fragment
        start, end = element_range(fragment, match.start(), tag)
        fragment = fragment[:start] + fragment[end:]


def content_word_count(fragment: str) -> int:
    fragment = remove_elements(fragment, "header", r'<header\b[^>]*class="[^"]*\bchapter-head\b[^"]*"[^>]*>')
    fragment = remove_elements(fragment, "nav", r'<nav\b[^>]*class="[^"]*\bchapter-nav\b[^"]*"[^>]*>')
    fragment = remove_elements(fragment, "p", r'<p\b[^>]*class="[^"]*\bchapter-close-label\b[^"]*"[^>]*>')
    fragment = remove_elements(fragment, "p", r'<p\b[^>]*class="[^"]*\bself-check-label\b[^"]*"[^>]*>')
    fragment = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return len(re.findall(r"\b[\w’'-]+\b", html.unescape(fragment), re.UNICODE))


def self_check_count(fragment: str) -> int:
    return len(re.findall(r'class="self-check-q"', fragment))


def nav_targets(fragment: str) -> list[str]:
    match = re.search(r'<nav\b[^>]*class="[^"]*\bchapter-nav\b[^"]*"[^>]*>(.*?)</nav>', fragment, re.I | re.S)
    if not match:
        return []
    return re.findall(r'href="#([^"]+)"', match.group(1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
    print("PASS", message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("1", "2", "3", "4", "5", "6", "final"), required=True)
    parser.add_argument("--audit", required=True)
    args = parser.parse_args()

    with open(BOOK, "rb") as handle:
        current = handle.read().decode("utf-8")
    with open(BASELINE_JSON, encoding="utf-8") as handle:
        baseline = json.load(handle)
    with open(args.audit, encoding="utf-8") as handle:
        audit = json.load(handle)

    require(not audit["summary"]["duplicate_ids"], "all IDs are unique")
    require(not audit["summary"]["broken_internal_hrefs"], "all internal hrefs resolve")
    require(not audit["summary"]["footnote_missing_notes"], "every footnote ref has a note")
    require(not audit["summary"]["footnote_orphan_notes"], "every footnote note has a ref")
    require(
        [item["sha256"] for item in audit["styles"]] == [item["sha256"] for item in baseline["styles"]],
        "style blocks match the baseline",
    )
    require(
        [item["sha256"] for item in audit["scripts"]] == [item["sha256"] for item in baseline["scripts"]],
        "script blocks match the baseline",
    )

    if args.phase in ("1", "2"):
        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        require(
            app_f["source_sha256"] == baseline["guards"]["appendix_f"]["source_sha256"],
            "Appendix F is byte-identical to the baseline",
        )

    if args.phase == "1":
        baseline_bytes = subprocess.check_output(
            ["git", "show", "%s:search-textbook.html" % BASELINE_COMMIT], cwd=REPO
        )
        original = baseline_bytes.decode("utf-8")
        old_ch5_words = content_word_count(section(original, "sec-embeddings"))
        new_ch5_words = sum(
            content_word_count(section(current, section_id))
            for section_id in ("sec-embeddings", "sec-retrieval-encoder")
        )
        require(new_ch5_words == old_ch5_words, "Chapter 5 split preserves every substantive word")

        old_transfer_words = sum(
            content_word_count(section(original, section_id))
            for section_id in ("sec-reranking-and-hybrid", "app-E")
        )
        new_transfer_words = sum(
            content_word_count(section(current, section_id))
            for section_id in ("sec-reranking-and-hybrid", "sec-hybrid-and-fusion", "app-E")
        )
        require(new_transfer_words == old_transfer_words, "Chapter 8/RRF move preserves every substantive word")

        expected_checks = {
            "sec-embeddings": 0,
            "sec-retrieval-encoder": 3,
            "sec-reranking-and-hybrid": 1,
            "sec-hybrid-and-fusion": 2,
        }
        for section_id, expected in expected_checks.items():
            require(
                self_check_count(section(current, section_id)) == expected,
                "%s has %d allocated self-check question(s)" % (section_id, expected),
            )
        expected_navs = {
            "sec-embeddings": ["exercise1", "retrieval-encoder"],
            "sec-retrieval-encoder": ["embeddings", "dense-at-scale"],
            "sec-dense-at-scale": ["retrieval-encoder", "representations-and-units"],
            "sec-reranking-and-hybrid": ["representations-and-units", "hybrid-and-fusion"],
            "sec-hybrid-and-fusion": ["reranking-and-hybrid", "query-transformation"],
            "sec-query-transformation": ["hybrid-and-fusion", "exercise2"],
        }
        for section_id, expected in expected_navs.items():
            require(nav_targets(section(current, section_id)) == expected, "%s navigation is correct" % section_id)
        require(current.count("<!-- TODO-PROSE -->") == 6, "six Phase 1 prose placeholders are present")
        require(
            sorted(set(re.findall(r"%%[A-Z0-9]+%%", current)))
            == ["%%NEW10%%", "%%NEW6%%", "%%TIME10%%", "%%TIME6%%"],
            "only the four planned Phase 1 tokens are present",
        )

    if args.phase == "2":
        expected_prefixes = {
            "1": 10, "2": 10, "3": 8, "4": 6, "5": 12, "6": 8,
            "7": 14, "8": 20, "9": 15, "10": 2, "11": 17, "12": 10,
            "13": 7, "14": 6, "15": 6, "A": 2, "B": 4, "C": 10,
            "D": 8, "E": 8, "F": 12,
        }
        require(audit["summary"]["numbered_asset_count"] == 195, "all 195 asset occurrences remain")
        require(audit["summary"]["asset_prefix_counts"] == expected_prefixes, "asset prefix counts match Phase 2")
        objects = audit["labelled_asset_objects"]
        object_labels = [item["label"] for item in objects]
        require(len(object_labels) == len(set(object_labels)) == 96, "all 96 physical asset labels are unique")
        require(
            set(item["label"] for item in audit["numbered_assets"]) == set(object_labels),
            "every asset occurrence has a matching physical label",
        )
        bad_ids = []
        for item in objects:
            expected_id = ("fig" if item["kind"] == "Figure" else "tbl") + "-%s-%d" % (
                item["prefix"].lower(), item["index"]
            )
            if item["id"] != expected_id:
                bad_ids.append("%s has %s, expected %s" % (item["label"], item["id"], expected_id))
        require(not bad_ids, "all physical asset IDs match their labels")
        moved_table = [item for item in objects if item["label"] == "Table 10.1"]
        require(
            len(moved_table) == 1 and moved_table[0]["section_id"] == "sec-hybrid-and-fusion",
            "the RRF worked example is Table 10.1 in the hybrid/fusion chapter",
        )
        require("%%ASSET" not in current, "no Phase 2 asset tokens remain")
        require(
            sorted(set(re.findall(r"%%[A-Z0-9]+%%", current)))
            == ["%%NEW10%%", "%%NEW6%%", "%%TIME10%%", "%%TIME6%%"],
            "Phase 1 structural tokens remain unchanged",
        )

    if args.phase == "3":
        from restructure import phase3

        phase2_bytes = subprocess.check_output(
            [
                "git", "cat-file", "--filters", "--path=search-textbook.html",
                "%s:search-textbook.html" % PHASE2_COMMIT,
            ],
            cwd=REPO,
        )
        expected = phase3(phase2_bytes.decode("utf-8"), baseline)
        require(current == expected, "Phase 3 output is exactly reproducible from the Phase 2 snapshot")

        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        baseline_words = baseline["guards"]["appendix_f"]["word_count"]
        require(
            abs(app_f["word_count"] - baseline_words) / baseline_words <= 0.005,
            "Appendix F word count remains within the 0.5% guard",
        )
        baseline_f_labels = {
            item["label"]: item["source_sha256"]
            for item in baseline["guards"]["appendix_f"]["label_objects"]
        }
        current_f_labels = {
            item["label"]: item["source_sha256"]
            for item in audit["labelled_asset_objects"]
            if item["section_id"] == "app-F"
        }
        require(current_f_labels == baseline_f_labels, "all Appendix F asset-label blocks are byte-identical")
        require(
            audit["summary"]["appendix_f_textual_reference_count"] == 13,
            "all 13 textual Appendix F references remain",
        )
        for phrase, expected_count in baseline["guards"]["exclusion_exact_text_counts"].items():
            require(current.count(phrase) == expected_count, "exclusion remains exact: %s" % phrase)
        with open(os.path.join(REPO, "phase2-audit.json"), encoding="utf-8") as handle:
            phase2_audit = json.load(handle)
        require(
            audit["summary"]["asset_prefix_counts"] == phase2_audit["summary"]["asset_prefix_counts"],
            "Phase 2 asset numbering is unchanged",
        )
        require(
            sorted(set(re.findall(r"%%[A-Z0-9]+%%", current)))
            == ["%%NEW10%%", "%%NEW6%%", "%%TIME10%%", "%%TIME6%%"],
            "only the four planned structural tokens remain",
        )

    if args.phase == "4":
        from restructure import phase4

        phase3_bytes = subprocess.check_output(
            [
                "git", "cat-file", "--filters", "--path=search-textbook.html",
                "%s:search-textbook.html" % PHASE3_COMMIT,
            ],
            cwd=REPO,
        )
        expected = phase4(phase3_bytes.decode("utf-8"), baseline)
        require(current == expected, "Phase 4 output is exactly reproducible from the Phase 3 snapshot")
        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        baseline_words = baseline["guards"]["appendix_f"]["word_count"]
        require(
            abs(app_f["word_count"] - baseline_words) / baseline_words <= 0.005,
            "Appendix F word count remains within the 0.5% guard",
        )
        require(audit["summary"]["appendix_f_textual_reference_count"] == 13,
                "all 13 textual Appendix F references remain")
        with open(os.path.join(REPO, "phase2-audit.json"), encoding="utf-8") as handle:
            phase2_audit = json.load(handle)
        require(audit["summary"]["asset_prefix_counts"] == phase2_audit["summary"]["asset_prefix_counts"],
                "Phase 2 asset numbering is unchanged")
        for phrase, expected_count in baseline["guards"]["exclusion_exact_text_counts"].items():
            require(current.count(phrase) == expected_count, "exclusion remains exact: %s" % phrase)
        require(
            sorted(set(re.findall(r"%%[A-Z0-9]+%%", current)))
            == ["%%NEW10%%", "%%NEW6%%", "%%TIME10%%", "%%TIME6%%"],
            "only the four planned structural tokens remain",
        )

    if args.phase == "5":
        from restructure import phase5

        phase4_bytes = subprocess.check_output(
            [
                "git", "cat-file", "--filters", "--path=search-textbook.html",
                "%s:search-textbook.html" % PHASE4_COMMIT,
            ],
            cwd=REPO,
        )
        expected = phase5(phase4_bytes.decode("utf-8"), baseline)
        require(current == expected, "Phase 5 output is exactly reproducible from the Phase 4 snapshot")
        eyebrows = [int(value) for value in re.findall(
            r'<p class="chapter-eyebrow">Chapter (\d+)</p>', current
        )]
        require(eyebrows == list(range(1, 16)), "chapter eyebrows run from 1 through 15")
        appendices = re.findall(r'<p class="chapter-eyebrow">Appendix ([A-F])</p>', current)
        require(appendices == list("ABCDEF"), "appendix eyebrows remain A through F")
        require("%%" not in current, "no placeholder tokens remain")
        require(current.count('data-ch="retrieval-encoder"') == 2,
                "both TOCs contain the new Chapter 6")
        require(current.count('data-ch="hybrid-and-fusion"') == 2,
                "both TOCs contain the new Chapter 10")
        require(current.count('<li class="toc-sec"><a href="#appendix-how-rrf-combines-ranked-lists"') == 0,
                "the slimmed Appendix E TOC no longer lists the moved RRF heading")
        stale_stage_text = [
            "Chapter 9 — the words you typed may be rewritten",
            "Chapter 9 — retrieval inputs may be rewritten",
            "Chapters 3 and 5–7 — one fast pass",
            "Chapter 8 — several candidate lists are combined",
            "Chapter 8 — a shortlist is compared again",
            "Chapter 13 — what the reader is finally shown",
            'class="stage-ch">Ch 5–7',
        ]
        require(not [text for text in stale_stage_text if text in current],
                "all stage-map numbering uses the fifteen-chapter map")
        with open(os.path.join(REPO, "phase4-audit.json"), encoding="utf-8") as handle:
            phase4_audit = json.load(handle)
        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        old_app_f = next(item for item in phase4_audit["h2_sections"] if item["section_id"] == "app-F")
        require(app_f["source_sha256"] == old_app_f["source_sha256"],
                "Phase 5 leaves Appendix F byte-identical to Phase 4")
        require(audit["summary"]["appendix_f_textual_reference_count"] == 13,
                "all 13 textual Appendix F references remain")
        with open(os.path.join(REPO, "phase2-audit.json"), encoding="utf-8") as handle:
            phase2_audit = json.load(handle)
        require(audit["summary"]["asset_prefix_counts"] == phase2_audit["summary"]["asset_prefix_counts"],
                "Phase 2 asset numbering is unchanged")

    if args.phase == "6":
        from restructure import phase6

        phase5_bytes = subprocess.check_output(
            [
                "git", "cat-file", "--filters", "--path=search-textbook.html",
                "%s:search-textbook.html" % PHASE5_COMMIT,
            ],
            cwd=REPO,
        )
        expected = phase6(phase5_bytes.decode("utf-8"), baseline)
        require(current == expected, "Phase 6 output is exactly reproducible from the Phase 5 snapshot")
        require("<!-- TODO-PROSE -->" not in current, "all empty prose placeholders are filled")
        require(current.count("<!-- TODO-PROSE-REVIEW -->") == 11,
                "all 11 new prose items are quarantined for author review")
        for section_id in ("sec-embeddings", "sec-retrieval-encoder",
                           "sec-reranking-and-hybrid", "sec-hybrid-and-fusion"):
            require(self_check_count(section(current, section_id)) >= 2,
                    "%s has at least two self-check questions" % section_id)
        with open(os.path.join(REPO, "phase5-audit.json"), encoding="utf-8") as handle:
            phase5_audit = json.load(handle)
        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        old_app_f = next(item for item in phase5_audit["h2_sections"] if item["section_id"] == "app-F")
        require(app_f["source_sha256"] == old_app_f["source_sha256"],
                "Phase 6 leaves Appendix F byte-identical to Phase 5")
        require(audit["summary"]["appendix_f_textual_reference_count"] == 13,
                "all 13 textual Appendix F references remain")
        require("%%" not in current, "no placeholder tokens remain")

    if args.phase == "final":
        from restructure import phase6

        phase5_bytes = subprocess.check_output(
            [
                "git", "cat-file", "--filters", "--path=search-textbook.html",
                "%s:search-textbook.html" % PHASE5_COMMIT,
            ],
            cwd=REPO,
        )
        expected = phase6(phase5_bytes.decode("utf-8"), baseline)
        require(current == expected, "final book is exactly reproducible from the Phase 5 snapshot")

        require(audit["summary"]["legacy_anchor_count"] == 37,
                "all 37 legacy anchors, including the moved RRF alias, remain")
        for anchor in ("reranking-and-hybrid", "why-hybrid-retrieval-remains-attractive",
                       "two-hybrids-that-combine-differently",
                       "appendix-how-rrf-combines-ranked-lists"):
            require(current.count('id="%s"' % anchor) == 1, "legacy target is unique: " + anchor)

        cues = [
            "Chapter 8</a> shows a 30-record reranker budget",
            "Chapter 8 returns to the LightGBM stage",
            "fusion machinery of Chapter 8",
            "Chapter 8’s LLM discussion",
            "Chapter 8 introduces result diversification",
            "Chapter 5’s retrieval-training story",
            "Appendix E</a> gives the formula and a worked example",
        ]
        require(not [cue for cue in cues if cue in current],
                "no retired Chapter 5/8 or RRF cross-reference cue remains")
        require(audit["summary"]["reference_match_counts"].get("Chapter 8") == 5,
                "the only Chapter 8 strings are two TOCs, its eyebrow, and three judged references")
        require(audit["summary"]["reference_match_counts"].get("Appendix E") == 12,
                "12 retained Appendix E references remain after replacing the moved RRF reference")

        for phrase, expected_count in baseline["guards"]["exclusion_exact_text_counts"].items():
            require(current.count(phrase) == expected_count, "exclusion remains exact: %s" % phrase)
        require(audit["summary"]["appendix_f_textual_reference_count"] == 13,
                "all 13 textual Appendix F references remain")

        with open(os.path.join(REPO, "phase2-audit.json"), encoding="utf-8") as handle:
            phase2_audit = json.load(handle)
        require(audit["summary"]["numbered_asset_count"] == 195,
                "all 195 audited asset occurrences remain")
        require(audit["summary"]["labelled_asset_object_count"] == 96,
                "all 96 physical figure/table labels remain")
        require(audit["summary"]["asset_prefix_counts"] == phase2_audit["summary"]["asset_prefix_counts"],
                "asset prefixes match the approved Phase 2 map")
        labels = audit["labelled_asset_objects"]
        require(len({item["label"] for item in labels}) == 96, "all physical asset labels are unique")
        for kind, list_id in (("Figure", "figure-index"), ("Table", "table-index")):
            expected_ids = [item["id"] for item in labels if item["kind"] == kind]
            list_match = re.search(r'<ol id="%s">(.*?)</ol>' % list_id, current, re.S)
            require(list_match is not None, "%s exists" % list_id)
            actual_ids = re.findall(r'<li><a href="#([^"]+)">', list_match.group(1))
            require(actual_ids == expected_ids, "%s is complete and in reading order" % list_id)
        baseline_f_labels = {
            item["label"]: item["source_sha256"]
            for item in baseline["guards"]["appendix_f"]["label_objects"]
        }
        current_f_labels = {
            item["label"]: item["source_sha256"] for item in labels if item["section_id"] == "app-F"
        }
        require(current_f_labels == baseline_f_labels, "all Appendix F asset-label blocks are byte-identical")

        require("%%" not in current, "no placeholder token remains")
        require("<!-- TODO-PROSE -->" not in current, "no empty prose placeholder remains")
        require(current.count("<!-- TODO-PROSE-REVIEW -->") == 11,
                "the final TODO inventory contains 11 review markers")

        ref_numbers = [int(number) for number in re.findall(
            r'<sup id="fnref:[^"]+"><a class="footnote-ref" href="#fn:[^"]+">(\d+)</a></sup>', current
        )]
        require(ref_numbers == list(range(1, 56)), "footnote references are globally sequential 1–55")
        back_numbers = [int(number) for number in re.findall(r'title="Jump back to footnote (\d+) in the text"', current)]
        require(back_numbers == list(range(1, 56)), "footnote back-reference labels are globally sequential 1–55")

        expected_navs = [
            ["intro"],
            ["preface", "boolean-admission"], ["intro", "bm25-ranking"],
            ["boolean-admission", "beyond-boolean"], ["bm25-ranking", "exercise1"],
            ["beyond-boolean", "embeddings"], ["exercise1", "retrieval-encoder"],
            ["embeddings", "dense-at-scale"], ["retrieval-encoder", "representations-and-units"],
            ["dense-at-scale", "reranking-and-hybrid"],
            ["representations-and-units", "hybrid-and-fusion"],
            ["reranking-and-hybrid", "query-transformation"],
            ["hybrid-and-fusion", "exercise2"], ["query-transformation", "agentic-search"],
            ["exercise2", "diagnosing-failure"], ["agentic-search", "evaluation"],
            ["diagnosing-failure", "library-practice"], ["evaluation", "exercise3"],
            ["library-practice", "what-you-can-now-ask"], ["exercise3", "backmatter"],
        ]
        actual_navs = [re.findall(r'href="#([^"]+)"', body) for body in re.findall(
            r'<nav class="chapter-nav"[^>]*>(.*?)</nav>', current, re.S
        )]
        require(actual_navs == expected_navs,
                "chapter navigation walks the 15 chapters, three exercises, and closing recap in order")
        eyebrows = [int(value) for value in re.findall(r'<p class="chapter-eyebrow">Chapter (\d+)</p>', current)]
        require(eyebrows == list(range(1, 16)), "chapter eyebrows run from 1 through 15")
        require(re.findall(r'<p class="chapter-eyebrow">Appendix ([A-F])</p>', current) == list("ABCDEF"),
                "appendix eyebrows remain A through F")

        HTMLParser().feed(current)
        require(current.count("Three parts, fifteen chapters") == 1,
                "hero identifies the fifteen-chapter structure")
        app_f = next(item for item in audit["h2_sections"] if item["section_id"] == "app-F")
        baseline_words = baseline["guards"]["appendix_f"]["word_count"]
        require(abs(app_f["word_count"] - baseline_words) / baseline_words <= 0.005,
                "Appendix F word count remains within the 0.5% guard")
        require("Applying Chapter 15 to active learning" in section(current, "app-F"),
                "Appendix F contains the one approved renamed heading")
        print("PASS HTML token stream parses without an exception")

    print("verification complete for phase", args.phase)


if __name__ == "__main__":
    main()
