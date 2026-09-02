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


REPO = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(REPO, "search-textbook.html")
BASELINE_JSON = os.path.join(REPO, "baseline.json")
BASELINE_COMMIT = "65469bbd4e7aa811db0f0511ae10a4386299308f"


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
    parser.add_argument("--phase", choices=("1", "2", "3", "final"), required=True)
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

    if args.phase in ("1", "2", "3"):
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

    print("verification complete for phase", args.phase)


if __name__ == "__main__":
    main()
