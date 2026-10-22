"""Chapter-grounded collection and independently calculated Boolean demonstrations."""
import re

RECORDS = {
    "D1": "Delulu job interview expectations",
    "D2": "Job interview preparation guide",
    "D3": "Unrealistic job expectations",
    "D4": "Delulu about my dream job",
}
SELECTED_POSTINGS = {
    "delulu": ("D1", "D4"),
    "job": ("D1", "D2", "D3", "D4"),
    "interview": ("D1", "D2"),
    "expectations": ("D1", "D3"),
    "unrealistic": ("D3",),
    "preparation": ("D2",),
}


def analysed_words(value):
    # Only the operations used by this small demonstration: word boundaries and lowercasing.
    return re.findall(r"[a-z]+", value.lower())


def build_postings(records):
    result = {}
    for ident, value in records.items():
        for word in set(analysed_words(value)):
            result.setdefault(word, set()).add(ident)
    return {term: tuple(sorted(ids)) for term, ids in result.items()}


POSTINGS = build_postings(RECORDS)


def combine(a, operator, b):
    left, right = set(POSTINGS[a]), set(POSTINGS[b])
    result = left & right if operator == "AND" else left | right if operator == "OR" else left - right if operator == "NOT" else None
    assert result is not None, operator
    return tuple(sorted(result))


POINTER_LEFT = (1, 4, 8, 13, 21)
POINTER_RIGHT = (2, 4, 5, 13, 20)


def intersection_trace(left=POINTER_LEFT, right=POINTER_RIGHT):
    i = j = 0
    kept, steps = [], []
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        action = "keep" if a == b else "advance left" if a < b else "advance right"
        steps.append({"i": i, "j": j, "a": a, "b": b, "kept_before": list(kept), "action": action})
        if a == b:
            kept.append(a); i += 1; j += 1
        elif a < b:
            i += 1
        else:
            j += 1
    return steps, tuple(kept)


def check_examples():
    assert len(RECORDS) == 4
    assert all(POSTINGS[term] == ids for term, ids in SELECTED_POSTINGS.items())
    assert combine("delulu", "AND", "job") == ("D1", "D4")
    assert combine("delulu", "OR", "unrealistic") == ("D1", "D3", "D4")
    assert combine("delulu", "AND", "interview") == ("D1",)
    assert combine("delulu", "OR", "interview") == ("D1", "D2", "D4")
    assert combine("delulu", "NOT", "interview") == ("D4",)
    # The weak-alternative record is deliberately additional, not a changed source record.
    extra = build_postings({**RECORDS, "E": "Foolish decisions in a garden"})
    before = set(extra["delulu"]) | set(extra["unrealistic"]) | set(extra.get("irrational", ()))
    assert "E" not in before and "E" in before | set(extra["foolish"])
    assert [n+1 for n, word in enumerate(analysed_words(RECORDS["D1"])) if word == "job"] == [2]
    steps, kept = intersection_trace()
    assert tuple(sorted(set(POINTER_LEFT) & set(POINTER_RIGHT))) == kept == (4, 13)
    assert all(b["i"] >= a["i"] and b["j"] >= a["j"] for a, b in zip(steps, steps[1:]))
    return {"source_records": 4, "selected_posting_lists": 6, "boolean_examples": 5,
            "pointer_comparisons": len(steps), "pointer_result": list(kept), "passed": True}
