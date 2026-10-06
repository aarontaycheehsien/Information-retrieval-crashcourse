"""Check citation direction, filter exclusions, source scope and scene execution."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("chapter11_render_test", HERE / "render.py")
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)
from scenes import Film, REFERENCES, citation_neighbours, scoped_studies  # noqa: E402


class QueryExamples(unittest.TestCase):
    def test_backward_citations_are_references(self):
        self.assertEqual(citation_neighbours("A"), {"C", "D"})

    def test_forward_citations_are_citing_papers(self):
        self.assertEqual(citation_neighbours("A", forward=True), {"E"})
        self.assertNotIn("C", citation_neighbours("A", forward=True))

    def test_shared_references_differ_from_co_citation(self):
        self.assertEqual(REFERENCES["A"] & REFERENCES["B"], {"C"})
        self.assertTrue({"A", "B"}.issubset(REFERENCES["E"]))

    def test_oa_filter_excludes_a_relevant_paywalled_study(self):
        self.assertEqual(scoped_studies(), {"A", "B"})
        self.assertEqual(scoped_studies(require_oa=True), {"B"})
        self.assertNotIn("C", scoped_studies())

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
