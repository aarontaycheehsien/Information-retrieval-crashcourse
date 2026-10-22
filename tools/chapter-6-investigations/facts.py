"""Pinned passage texts and declared arithmetic examples, not encoder measurements."""
import math

QUERY = "Am I being delulu about getting this job?"
PASSAGES = {
    "positive": "How to recognise unrealistic expectations during a job search",
    "easy": "A history of agricultural employment",
    "hard": "Ten signs that you performed well in your job interview",
}
TOY_TEXT = "delulu"
TOY_VOCABULARY = {"d": 3, "e": 8, "l": 11, "u": 21}
INITIAL_VECTORS = {3: (1, 0, 0), 8: (0, 1, 0), 11: (0, 0, 1), 21: (1, 1, 0)}
# Supplied contextual working vectors for arithmetic illustration, not a model run.
CONTEXT_VECTORS = ((2, 0, 1), (0, 2, 1), (1, 1, 4),
                   (3, 0, 2), (0, 3, 1), (0, 0, 3))
QUERY_VECTOR = (1., 0.)
ANGLES = {
    "before": {"positive": 80, "hard": 30, "easy": 140},
    "after": {"positive": 20, "hard": 70, "easy": 150},
}


def token_ids(text=TOY_TEXT):
    """Declared character tokenizer and vocabulary, limited to this toy input."""
    return tuple(TOY_VOCABULARY[char] for char in text)


def mean_pool(vectors=CONTEXT_VECTORS):
    return tuple(sum(column)/len(vectors) for column in zip(*vectors))


def unit_vector(degrees):
    angle = math.radians(degrees)
    return (math.cos(angle), math.sin(angle))


def cosine(a, b):
    return sum(x*y for x, y in zip(a, b)) / (math.hypot(*a)*math.hypot(*b))


def scores(state):
    return {name: cosine(QUERY_VECTOR, unit_vector(degrees)) for name, degrees in ANGLES[state].items()}


def ranking(state):
    values = scores(state)
    return sorted(values, key=values.get, reverse=True)


def check_examples():
    assert token_ids() == (3, 8, 11, 21, 11, 21)
    assert len(token_ids()) == len(CONTEXT_VECTORS) == 6
    assert INITIAL_VECTORS[token_ids()[2]] == INITIAL_VECTORS[token_ids()[4]]
    assert CONTEXT_VECTORS[2] != CONTEXT_VECTORS[4]
    assert [sum(v[i] for v in CONTEXT_VECTORS) for i in range(3)] == [6, 6, 12]
    assert mean_pool() == (1., 1., 2.)
    for state in ANGLES:
        for name, degrees in ANGLES[state].items():
            vector = unit_vector(degrees)
            assert math.isclose(math.hypot(*vector), 1)
            assert math.isclose(scores(state)[name], math.cos(math.radians(degrees)))
            assert -1 <= scores(state)[name] <= 1
    assert ranking("before") == ["hard", "positive", "easy"]
    assert ranking("after") == ["positive", "hard", "easy"]
    assert scores("after")["positive"] > scores("before")["positive"]
    return {"declared_toy_examples": True, "measured_model_outputs": False,
            "token_ids": list(token_ids()), "mean_pool": list(mean_pool()),
            "scores": {state: scores(state) for state in ANGLES},
            "rankings": {state: ranking(state) for state in ANGLES},
            "scores_are_relevance_probabilities": False, "passed": True}
