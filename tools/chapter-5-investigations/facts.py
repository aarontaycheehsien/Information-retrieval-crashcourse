"""Declared teaching examples; none of these values are trained-model outputs."""
import math

TOY_WORDS = {"man": (1., 1.), "woman": (4., 2.), "king": (2., 4.),
             "queen": (5., 5.), "tree": (6., 1.)}
PROJECTION_POINTS = {"P": (2., 2., 0.), "Q": (2., 2., 10.)}
POOL_INPUT = ((1., 3.), (3., 1.), (2., 2.))
SENTENCE = "The patient received heart treatment after the attack".split()


def analogy():
    return tuple(k-m+w for k, m, w in zip(TOY_WORDS["king"], TOY_WORDS["man"], TOY_WORDS["woman"]))


def project(point):
    """Drop the third coordinate. This is not PCA or a trained projection."""
    return tuple(point[:2])


def mean_pool(vectors=POOL_INPUT):
    return tuple(sum(column)/len(vectors) for column in zip(*vectors))


def training_tasks():
    return {
        "cbow": {"visible_positions": [1, 2, 4, 5], "target_position": 3},
        "masked": {"visible_positions": [i for i in range(8) if i != 4], "target_position": 4},
        "next_token": {"visible_positions": list(range(5)), "target_position": 5},
    }


def check_examples():
    result = analogy()
    candidates = {k: v for k, v in TOY_WORDS.items() if k not in ("king", "man", "woman")}
    nearest = min(candidates, key=lambda k: math.dist(result, candidates[k]))
    assert result == TOY_WORDS["queen"] and nearest == "queen"
    assert tuple(b-a for a, b in zip(TOY_WORDS["man"], TOY_WORDS["woman"])) == (3., 1.)
    assert tuple(b-a for a, b in zip(TOY_WORDS["king"], TOY_WORDS["queen"])) == (3., 1.)
    assert math.dist(*PROJECTION_POINTS.values()) == 10
    assert math.dist(*(project(v) for v in PROJECTION_POINTS.values())) == 0
    assert mean_pool() == (2., 2.)
    assert list("jobs") == ["j", "o", "b", "s"]
    expected_targets = {"cbow": "heart", "masked": "treatment", "next_token": "after"}
    for name, task in training_tasks().items():
        assert task["target_position"] not in task["visible_positions"]
        assert SENTENCE[task["target_position"]] == expected_targets[name]
    nxt = training_tasks()["next_token"]
    assert all(i < nxt["target_position"] for i in nxt["visible_positions"])
    assert [SENTENCE[i] for i in training_tasks()["cbow"]["visible_positions"]] == ["patient", "received", "treatment", "after"]
    return {"declared_toy_examples": True, "trained_model_outputs": False,
            "analogy_result": list(result), "nearest_after_input_exclusion": nearest,
            "distance_before_projection": 10, "distance_after_projection": 0,
            "mean_pool": list(mean_pool()), "training_targets": expected_targets,
            "hidden_targets_absent_from_input": True, "passed": True}
