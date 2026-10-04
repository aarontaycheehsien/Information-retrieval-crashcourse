"""Check historical examples, uncertainty, narration reuse and animated scenes."""
import unittest
import numpy as np
import skia
import render
from scenes import Film


class ChapterExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = render.read_config()

    def test_documented_primo_boundaries_and_order(self):
        scene = next(s for s in self.cfg['episodes'][0]['scenes'] if s['id'] == 'primo')
        narration = scene['narration']
        for value in ['Boolean variations connected by OR', 'Up to thirty', 'selects five sources', 'from their abstracts']:
            self.assertIn(value, narration)
        self.assertLess(narration.index('thirty'), narration.index('five sources'))

    def test_query_example_preserves_the_full_need(self):
        text = ' '.join(s['narration'] for s in self.cfg['episodes'][1]['scenes'])
        for value in ['AI academic libraries', 'empirical studies since twenty twenty four',
                      'opinion piece from twenty nineteen', 'large language models', 'university library',
                      'different perspectives, not a ladder', 'Relevant to someone, for something']:
            self.assertIn(value, text)

    def test_puzzles_retain_quantities_dates_and_uncertainty(self):
        text = ' '.join(s['narration'] for s in self.cfg['episodes'][2]['scenes'])
        for value in ['nine point four million', 'a thousand', 'August twenty twenty six',
                      'thirteen results', 'thirty five thousand three hundred',
                      'not proof of a hidden mechanism', 'does not prove where the original run lost it']:
            self.assertIn(value, text)
        self.assertEqual(round(35300/13), 2715)

    def test_word_reveals_follow_the_matching_scene(self):
        episode = self.cfg['episodes'][0]
        timeline = {'scenes': {'opening': (0, 20), 'primo': (20, 50)}, 'takes': [
            {'scene': 'opening', 'words': [{'text': 'five', 'start': 8.0}]},
            {'scene': 'primo', 'words': [{'text': 'five', 'start': 40.0}]}]}
        film = Film(episode, timeline)
        self.assertEqual(film.at('opening', 'five'), 8)
        self.assertEqual(film.at('primo', 'five'), 20)

    def test_every_scene_draws_and_has_visible_motion(self):
        for episode in self.cfg['episodes']:
            timeline = {'scenes': {s['id']: (i*24, (i+1)*24) for i, s in enumerate(episode['scenes'])}, 'takes': []}
            film, surface = Film(episode, timeline), skia.Surface(1920, 1080)
            for i, scene in enumerate(episode['scenes']):
                first = None
                for fraction in [.02, .25, .52, .82, .985]:
                    with self.subTest(film=episode['id'], scene=scene['id'], time=fraction):
                        film.draw(surface.getCanvas(), i*24+fraction*24)
                        if fraction in [.25, .52]:
                            pixels = surface.makeImageSnapshot().toarray()[260:820, 140:1780]
                            if first is None:
                                first = pixels.copy()
                            else:
                                self.assertGreater(np.count_nonzero(np.any(first != pixels, axis=2)), 250)


if __name__ == '__main__':
    unittest.main()
