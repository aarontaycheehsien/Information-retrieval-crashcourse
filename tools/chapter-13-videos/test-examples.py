"""Verify diagnostic boundaries, source examples, and scene execution."""
import unittest
import render
from scenes import Film, IDENTIFIERS, TOKEN_PIECES, DIRECTION_PAIR, bag, boundary, exact_matches


class ChapterExamples(unittest.TestCase):
    def test_four_alternative_boundaries(self):
        cases = ((False, None, None, None, "coverage"),
                 (True, False, None, None, "filter"),
                 (True, True, False, None, "candidate"),
                 (True, True, True, False, "display"),
                 (True, True, True, True, "visible"))
        for *flags, expected in cases:
            self.assertEqual(boundary(*flags), expected)

    def test_unknown_trace_does_not_prove_exclusion(self):
        self.assertEqual(boundary(None, None, None, False), "unknown")
        self.assertEqual(boundary(True, True, None, False), "unknown")

    def test_identifier_identity(self):
        self.assertEqual(exact_matches(IDENTIFIERS[0], IDENTIFIERS), [IDENTIFIERS[0]])
        self.assertEqual(exact_matches("DELULU-429", IDENTIFIERS), [])

    def test_opposing_relations_share_term_counts(self):
        self.assertEqual(bag(DIRECTION_PAIR[0]), bag(DIRECTION_PAIR[1]))
        self.assertNotEqual(DIRECTION_PAIR[0], DIRECTION_PAIR[1])

    def test_source_token_example(self):
        self.assertEqual(TOKEN_PIECES, ("ri", "##zz", "##lord"))
        self.assertEqual("".join(v.removeprefix("##") for v in TOKEN_PIECES), "rizzlord")

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
