"""Explicit single-field BM25 teaching model; independent reference checks."""
import math
import re

RECORDS = {
    "D1": "Delulu job interview expectations",
    "D2": "Job interview preparation guide",
    "D3": "Unrealistic job expectations",
    "D4": "Delulu about my dream job",
}
QUERY = ("delulu", "job")
K1, B = 1.2, .75
TOKENS = {key: re.findall(r"[a-z]+", value.lower()) for key, value in RECORDS.items()}
LENGTHS = {key: len(words) for key, words in TOKENS.items()}
AVERAGE_LENGTH = sum(LENGTHS.values())/len(LENGTHS)
DOCUMENT_FREQUENCIES = {term: sum(term in words for words in TOKENS.values()) for term in QUERY}


def idf(n, df):
    """Common positive-IDF variant. Other implementations and variants can differ."""
    assert 0 <= df <= n and n > 0
    return math.log1p((n-df+.5)/(df+.5))


def factor(tf, length=100, average=100, k1=K1, b=B):
    assert tf >= 0 and length > 0 and average > 0 and k1 >= 0 and 0 <= b <= 1
    if tf == 0:
        return 0.
    return tf*(k1+1)/(tf+k1*(1-b+b*length/average))


def contributions():
    return {key: {term: idf(len(TOKENS), DOCUMENT_FREQUENCIES[term]) *
                  factor(words.count(term), len(words), AVERAGE_LENGTH)
                  for term in QUERY} for key, words in TOKENS.items()}


def totals():
    return {key: sum(parts.values()) for key, parts in contributions().items()}


def ranking(strict_and=False):
    scores = totals()
    candidates = [key for key, words in TOKENS.items()
                  if all(term in words for term in QUERY)] if strict_and else [
                      key for key, words in TOKENS.items() if any(term in words for term in QUERY)]
    return sorted(candidates, key=lambda key: scores[key], reverse=True)


def check_examples():
    # Independent values stated in the chapter or exact hand-reduced fractions.
    assert math.isclose(factor(1), 1.)
    assert math.isclose(factor(2), 11/8)
    assert math.isclose(factor(20), 110/53)
    assert round(factor(20), 2) == 2.08 and factor(20) < K1+1 == 2.2
    gains = [factor(t+1)-factor(t) for t in range(20)]
    assert all(a > b > 0 for a, b in zip(gains, gains[1:]))
    assert all(factor(t, length, 100, k1=0) == 1 for t in (1, 2, 20) for length in (40, 400))
    assert factor(0, k1=0) == 0
    assert math.isclose(factor(1, 40), 110/83)
    assert math.isclose(factor(1, 400), 22/49)
    assert math.isclose(factor(1, 40, b=0), factor(1, 400, b=0))
    assert math.isclose(idf(10, 2), math.log(22/5))
    assert math.isclose(idf(10, 9), math.log(22/19))
    assert round(idf(10, 2)+idf(10, 9), 2) == 1.63
    assert list(LENGTHS.values()) == [4, 4, 3, 5] and AVERAGE_LENGTH == 4
    assert DOCUMENT_FREQUENCIES == {"delulu": 2, "job": 4}
    assert math.isclose(totals()["D1"], math.log(20/9))
    assert math.isclose(totals()["D4"], math.log(20/9)*88/97)
    assert {k: round(v, 2) for k, v in totals().items()} == {"D1": .80, "D2": .11, "D3": .12, "D4": .72}
    assert ranking(True) == ["D1", "D4"] and ranking() == ["D1", "D4", "D3", "D2"]
    assert 3 < 5 < 7  # Separate, stipulated valid-bound illustration; no measured scores.
    return {"chapter_factors": [factor(t) for t in (1, 2, 20)], "limit": K1+1,
            "length_factors": [factor(1, length) for length in (40, 400)],
            "toy_scores": totals(), "strict_and_order": ranking(True), "direct_order": ranking(),
            "passed": True}
