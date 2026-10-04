"""Check the instructional arithmetic, cutoffs, and animation scene coverage."""
from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("chapter10_render_test", HERE / "render.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)
from scenes import DENSE, LEXICAL, Film, order, rrf  # noqa: E402


class FusionExamples(unittest.TestCase):
    def test_chapter_values(self):
        expected = {"A": Fraction(123, 3782), "C": Fraction(124, 3843),
                    "B": Fraction(1, 62), "D": Fraction(1, 63)}
        for record, score in rrf((LEXICAL, DENSE)).items():
            self.assertAlmostEqual(score, float(expected[record]), places=14)

    def test_missing_from_one_list(self):
        self.assertEqual(rrf((("X",), ())), {"X": 1/61})

    def test_both_input_cutoffs_hide_record(self):
        full = (("A", "B", "E"), ("C", "D", "E"))
        self.assertIn("E", rrf(full))
        self.assertNotIn("E", rrf(tuple(r[:2] for r in full)))

    def test_output_cutoff_does_not_change_scores(self):
        scores = rrf((LEXICAL, DENSE))
        self.assertEqual(order(scores)[:2], ["A", "C"])
        self.assertEqual(len(scores), 4)

    def test_weighted_order(self):
        self.assertEqual(order(rrf((LEXICAL, DENSE), weights=(1, 2))), ["C", "A", "D", "B"])

    def test_duplicate_identity_rejected(self):
        with self.assertRaises(AssertionError):
            rrf((("A", "A"),))

    def test_all_scenes_draw_at_multiple_times(self):
        import skia
        cfg = render.read_config()
        for episode in cfg["episodes"]:
            timeline = {"scenes": {s["id"]: (i*20, (i+1)*20) for i, s in enumerate(episode["scenes"])}, "takes": []}
            film = Film(episode, timeline)
            surface = skia.Surface(1920, 1080)
            for i, scene in enumerate(episode["scenes"]):
                for fraction in (.02, .25, .52, .82, .985):
                    with self.subTest(episode=episode["id"], scene=scene["id"], fraction=fraction):
                        film.draw(surface.getCanvas(), i*20+20*fraction)


if __name__ == "__main__":
    unittest.main()
