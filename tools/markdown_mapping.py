"""Check the Markdown mapping (data/markdown-mapping.json) against the book.

Phase 2 of reviews/markdown-conversion-plan.md. Reports:

- classes and elements in search-textbook.html with no mapping, or mapped twice;
- mapped classes that no longer occur in the book (stale entries);
- how the book's words divide between statuses, and the raw-HTML share of
  authored words, which the plan's phase 3 stop rule compares with 25%.

Usage: python tools/markdown_mapping.py [--json]. Exit 1 if the mapping is
incomplete or stale. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import html_equivalence as eq

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "search-textbook.html"
MAPPING = ROOT / "data" / "markdown-mapping.json"
STATUSES = ("native", "filter", "derived", "generated", "template", "raw")
# When text sits inside several constructs, the outermost owner that is not
# authored Markdown decides: generated beats template beats raw.
PRIORITY = ("generated", "template", "raw")
WORD = re.compile(r"\S+")


def load_mapping(path: Path = MAPPING) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def class_owners(mapping: dict) -> tuple[dict[str, str], list[str]]:
    owners: dict[str, str] = {}
    errors = []
    for construct in mapping["constructs"]:
        if construct["status"] not in STATUSES:
            errors.append(f"{construct['id']}: unknown status {construct['status']!r}")
        for cls in construct["classes"]:
            if cls in owners:
                errors.append(f"class {cls!r} mapped by both {owners[cls]} and {construct['id']}")
            owners[cls] = construct["id"]
    return owners, errors


def element_status(mapping: dict) -> tuple[dict[str, str], list[str]]:
    status: dict[str, str] = {}
    errors = []
    for key, tags in mapping["elements"].items():
        if key not in STATUSES:
            errors.append(f"elements: unknown status {key!r}")
        for tag in tags:
            if tag in status:
                errors.append(f"element <{tag}> listed as both {status[tag]} and {key}")
            status[tag] = key
    return status, errors


def inventory(root: eq.Node) -> tuple[Counter, Counter]:
    classes: Counter = Counter()
    tags: Counter = Counter()
    todo = [root]
    while todo:
        node = todo.pop()
        if node.kind == "element":
            tags[node.tag] += 1
            for cls in (node.get("class") or "").split():
                classes[cls] += 1
        todo.extend(node.children)
    return classes, tags


def word_shares(root: eq.Node, mapping: dict) -> tuple[Counter, Counter]:
    """Words and elements by the status of the construct that owns them."""
    owners, _ = class_owners(mapping)
    construct_status = {c["id"]: (c["status"] if c.get("propagates", True) else "wrapper")
                        for c in mapping["constructs"]}
    elements, _ = element_status(mapping)
    words: Counter = Counter()
    nodes: Counter = Counter()

    def walk(node: eq.Node, inherited: str | None):
        for child in node.children:
            if child.kind == "text":
                if inherited in ("script", "style"):
                    continue
                n = len(WORD.findall(child.text))
                if n:
                    words[inherited if inherited in STATUSES else "authored-markdown"] += n
            elif child.kind == "element":
                if child.tag in ("script", "style"):
                    continue
                state = inherited
                candidates = [construct_status[owners[c]] for c in (child.get("class") or "").split() if c in owners]
                # Element statuses pass to descendants only for raw and generated
                # elements (svg, the lookup form). Template elements such as
                # <body> and <article> wrap the authored book itself.
                if elements.get(child.tag) in ("raw", "generated"):
                    candidates.append(elements[child.tag])
                for status in PRIORITY:
                    if status in candidates and (state not in PRIORITY or PRIORITY.index(status) < PRIORITY.index(state)):
                        state = status
                        break
                nodes[state if state in STATUSES else "authored-markdown"] += 1
                walk(child, state)

    walk(root, None)
    return words, nodes


def check(source: str, mapping: dict) -> dict:
    root = eq.parse(source, BOOK.name)
    classes, tags = inventory(root)
    owners, errors = class_owners(mapping)
    elements, element_errors = element_status(mapping)
    errors += element_errors
    unmapped_classes = sorted(set(classes) - set(owners))
    stale_classes = sorted(set(owners) - set(classes))
    unmapped_elements = sorted(set(tags) - set(elements))
    stale_elements = sorted(set(elements) - set(tags))
    words, nodes = word_shares(root, mapping)
    authored = words["authored-markdown"] + words["raw"]
    authored_nodes = nodes["authored-markdown"] + nodes["raw"]
    return {
        "errors": errors,
        "unmapped_classes": unmapped_classes,
        "stale_classes": stale_classes,
        "unmapped_elements": unmapped_elements,
        "stale_elements": stale_elements,
        "classes_in_book": len(classes),
        "constructs": len(mapping["constructs"]),
        "words": dict(words),
        "elements": dict(nodes),
        "raw_share_of_authored": round(words["raw"] / authored, 4) if authored else 0.0,
        "raw_element_share_of_authored": round(nodes["raw"] / authored_nodes, 4) if authored_nodes else 0.0,
    }


def ok(report: dict) -> bool:
    return not any(report[k] for k in ("errors", "unmapped_classes", "stale_classes",
                                        "unmapped_elements", "stale_elements"))


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    report = check(BOOK.read_text(encoding="utf-8"), load_mapping())
    if "--json" in argv:
        print(json.dumps(report, indent=2))
    else:
        for key in ("errors", "unmapped_classes", "stale_classes", "unmapped_elements", "stale_elements"):
            if report[key]:
                print(f"{key.replace('_', ' ')}: {', '.join(report[key])}")
        print(f"{report['classes_in_book']} classes in the book, {report['constructs']} constructs.")
        total = sum(report["words"].values())
        for status, n in sorted(report["words"].items(), key=lambda kv: -kv[1]):
            print(f"  {status:18} {n:7} words  {n / total:6.1%}")
        print(f"Raw HTML share of authored words: {report['raw_share_of_authored']:.1%}; "
              f"of authored elements: {report['raw_element_share_of_authored']:.1%} "
              "(plan's stop threshold: 25%)")
        print("Mapping complete." if ok(report) else "Mapping incomplete or stale.")
    return 0 if ok(report) else 1


if __name__ == "__main__":
    sys.exit(main())
