"""Calculate admission examples; keep illustrative order separate from scores."""
from pathlib import Path
import re

FRUIT_QUERY = frozenset(("apple", "orange", "banana"))
FRUIT_RECORDS = {
    "A": frozenset(("apple", "orange", "banana")),
    "B": frozenset(("apple", "orange")),
    "C": frozenset(("apple",)),
    "D": frozenset(("pear", "grape")),
}
# The chapter explicitly stipulates this order; no BM25 scores are inferred.
ILLUSTRATIVE_ORDER = ("B", "A", "C")


def lab_records():
    source = (Path(__file__).parent / "source-lab.html").read_text()
    raw = source.split("const RECORDS = [", 1)[1].split("];", 1)[0]
    matches = re.findall(r"id:'([A-F])',\s*title:'([^']*)',\s*body:'([^']*)'", raw)
    assert len(matches) == 6
    return {ident: {"title": title, "body": body} for ident, title, body in matches}


LAB_RECORDS = lab_records()
ORIGINAL_QUERY = frozenset(("delulu", "job", "interview", "expectations"))
EXPANDED_QUERY = ORIGINAL_QUERY | {"foolish"}


def terms(record):
    return frozenset(re.findall(r"[a-z]+", (record["title"] + " " + record["body"]).lower()))


def eligible(records, query, minimum):
    return tuple(ident for ident, ts in records.items() if len(query & ts) >= minimum)


def check_examples():
    assert eligible(FRUIT_RECORDS, FRUIT_QUERY, 3) == ("A",)
    assert eligible(FRUIT_RECORDS, FRUIT_QUERY, 2) == ("A", "B")
    assert eligible(FRUIT_RECORDS, FRUIT_QUERY, 1) == ("A", "B", "C")
    assert set(ILLUSTRATIVE_ORDER) == set(eligible(FRUIT_RECORDS, FRUIT_QUERY, 1))
    assert ILLUSTRATIVE_ORDER[:2] == ("B", "A")
    records = {ident: terms(rec) for ident, rec in LAB_RECORDS.items()}
    assert ORIGINAL_QUERY <= records["A"] and "foolish" not in records["A"]
    assert EXPANDED_QUERY & records["F"] == {"foolish", "job", "interview"}
    assert eligible(records, ORIGINAL_QUERY, 4) == ("A",)
    assert eligible(records, EXPANDED_QUERY, 5) == ()
    assert {"A", "F"} <= set(eligible(records, EXPANDED_QUERY, 1))
    assert [ident for ident, ts in records.items() if "foolish" in ts] == ["F"]
    # In the optional-term illustration, a term with no postings changes no eligibility.
    assert eligible(records, ORIGINAL_QUERY | {"zzqvplm"}, 1) == eligible(records, ORIGINAL_QUERY, 1)
    assert eligible(records, ORIGINAL_QUERY | {"zzqvplm"}, 5) == ()
    return {"all_three": ["A"], "minimum_two": ["A", "B"],
            "any_one": ["A", "B", "C"], "stipulated_order": list(ILLUSTRATIVE_ORDER),
            "top_two": list(ILLUSTRATIVE_ORDER[:2]), "foolish_document_frequency": 1,
            "lab_collection_size": len(records), "numerical_ranking_asserted": False,
            "passed": True}
