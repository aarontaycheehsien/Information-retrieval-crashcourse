"""Computed toy vector comparisons and source-exact six-point neighbour example."""
import math

QUERY = (1., 0.)
VECTORS = {"A": (.9, .3), "B": (1., 1.), "C": (-.4, .8)}
ANN_QUERY = (0., 0.)
ANN_POINTS = {"A": (1., 0.), "B": (0., 2.), "C": (2., 2.),
              "D": (3., 1.), "E": (4., 3.), "F": (1., 5.)}
APPROX_EXAMINED = ("A", "B", "D", "F")
K = 3


def dot(a, b):
    assert len(a) == len(b)
    return sum(x*y for x, y in zip(a, b))


def normalise(vector):
    length = math.hypot(*vector)
    assert length > 0
    return tuple(value/length for value in vector)


def cosine(a, b):
    return dot(normalise(a), normalise(b))


def scores(rule="cosine", unit=False):
    compare = cosine if rule == "cosine" else dot
    query = normalise(QUERY) if unit else QUERY
    return {name: compare(query, normalise(v) if unit else v) for name, v in VECTORS.items()}


def ranking(rule="cosine", unit=False):
    values = scores(rule, unit)
    return sorted(values, key=values.get, reverse=True)


def distances():
    # This source example uses Euclidean distance, not cosine at the zero vector.
    return {name: math.dist(ANN_QUERY, point) for name, point in ANN_POINTS.items()}


def nearest(examined=None, k=K):
    values = distances()
    return sorted(ANN_POINTS if examined is None else examined, key=values.get)[:k]


def check_examples():
    assert ranking("cosine") == ["A", "B", "C"]
    assert ranking("dot") == ["B", "A", "C"]
    assert math.isclose(scores()["A"], 3/math.sqrt(10))
    assert math.isclose(scores()["B"], 1/math.sqrt(2))
    assert math.isclose(scores("dot")["A"], .9) and scores("dot")["B"] == 1
    assert cosine(QUERY, QUERY) == 1 and cosine(QUERY, (0, 1)) == 0 and cosine(QUERY, (-1, 0)) == -1
    for name, vector in VECTORS.items():
        assert math.isclose(cosine(QUERY, vector), cosine(QUERY, tuple(x*3 for x in vector)))
        assert math.isclose(scores("cosine", True)[name], scores("dot", True)[name])
    assert ranking("cosine", True) == ranking("dot", True) == ["A", "B", "C"]
    assert [round(v*v) for v in distances().values()] == [1, 4, 8, 10, 25, 26]
    assert nearest() == ["A", "B", "C"] and nearest(APPROX_EXAMINED) == ["A", "B", "D"]
    assert "C" not in APPROX_EXAMINED and distances()["C"] < distances()["D"]
    assert len(nearest()) == len(nearest(APPROX_EXAMINED)) == K
    assert len(ANN_POINTS) == 6 and len(APPROX_EXAMINED) == 4
    return {"declared_similarity_vectors": True, "measured_model_outputs": False,
            "cosine_scores": scores(), "dot_scores": scores("dot"),
            "unit_dot_scores": scores("dot", True), "ann_distances": distances(),
            "exact_top_three": nearest(), "approximate_top_three": nearest(APPROX_EXAMINED),
            "exact_comparisons": 6, "approximate_comparisons": 4,
            "simulates_hnsw": False, "scores_are_relevance_probabilities": False, "passed": True}
