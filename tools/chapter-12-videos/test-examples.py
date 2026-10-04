"""Check teaching examples and draw every scene at five animation times."""
import unittest
import render
from scenes import Film, REFERENCES, RELATED, ROUNDS, cumulative, uncited


class ChapterExamples(unittest.TestCase):
    def test_uncited_identity_comparison(self):
        self.assertEqual(uncited(RELATED, REFERENCES), ["B", "D"])
        self.assertEqual(uncited(["A", "B", "B"], ["A"]), ["B"])
        self.assertEqual(uncited([], REFERENCES), [])

    def test_repetition_and_recovery(self):
        self.assertEqual(cumulative((ROUNDS[0], ROUNDS[0]))[-1], ROUNDS[0])
        first, second = cumulative(ROUNDS)
        self.assertLess(first, second)
        self.assertIn("selection-bias methods", second)
        self.assertNotIn("selection-bias methods", first)

    def test_all_scenes_draw_at_multiple_times(self):
        import skia
        cfg = render.read_config()
        for episode in cfg["episodes"]:
            timeline = {"scenes": {s["id"]: (i*20, (i+1)*20) for i, s in enumerate(episode["scenes"])}, "takes": []}
            film = Film(episode, timeline)
            surface = skia.Surface(1920, 1080)
            for i, scene in enumerate(episode["scenes"]):
                for fraction in (.02, .25, .52, .82, .985):
                    with self.subTest(film=episode["id"], scene=scene["id"], time=fraction):
                        film.draw(surface.getCanvas(), i*20+20*fraction)


if __name__ == "__main__":
    unittest.main()
