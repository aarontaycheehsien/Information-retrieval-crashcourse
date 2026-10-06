"""Check source grounding, mock-trace boundaries, questionnaire coverage and motion."""
import re
import unittest
from html.parser import HTMLParser

import numpy as np
import skia
import render
from scenes import Film, MOCK_TRACE, QUESTION_GROUPS


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        self.data.append(data)


class ChapterExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = render.read_config()
        parser = PlainText()
        source = (render.ROOT/'search-textbook.html').read_text(encoding='utf-8')
        start = source.index('id="sec-library-practice"')
        parser.feed(source[start:source.index('id="exercise3"', start)])
        cls.source_text = re.sub(r'\s+', ' ', ' '.join(parser.data))

    def test_mock_trace_is_grounded_in_chapter(self):
        for fixture in ['Does open access increase citations?', '“open access” AND citation*',
                        '18 of 100 supplied candidates', 'moved P to rank 3', 'first 10 records',
                        'not disclosed', 'All record details and ranks are hypothetical']:
            self.assertIn(fixture, self.source_text)
        self.assertEqual(MOCK_TRACE['candidate_rank'], 18)
        self.assertEqual(MOCK_TRACE['candidate_count'], 100)
        self.assertEqual(MOCK_TRACE['final_rank'], 3)
        self.assertEqual(MOCK_TRACE['display_cutoff'], 10)
        self.assertIsNone(MOCK_TRACE['reranker_details'])

    def test_reranking_changes_display_eligibility(self):
        self.assertGreater(MOCK_TRACE['candidate_rank'], MOCK_TRACE['display_cutoff'])
        self.assertLessEqual(MOCK_TRACE['final_rank'], MOCK_TRACE['display_cutoff'])
        self.assertLessEqual(MOCK_TRACE['candidate_rank'], MOCK_TRACE['candidate_count'])

    def test_all_nineteen_questions_have_exactly_one_scene(self):
        questions = [q for scene in self.cfg['episodes'][2]['scenes'] for q in scene.get('question_ids', [])]
        self.assertEqual(questions, list(range(1, 20)))
        for scene in self.cfg['episodes'][2]['scenes']:
            qs = set(scene.get('question_ids', []))
            if qs:
                self.assertTrue(any(qs <= set(group) for group in QUESTION_GROUPS))

    def test_scripts_preserve_the_evidence_limits(self):
        narration = ' '.join(s['narration'] for e in self.cfg['episodes'] for s in e['scenes'])
        for required in ['Dense retrieval is not inherently random', 'action and observation trace',
                         'observed, vendor documented, or unknown', 'internal scoring details remain undisclosed',
                         'This is inspection order, not execution order', 'not a probability of relevance',
                         'saved transformation', 'per-query consumption', 'individual failures as well as averages']:
            self.assertIn(required, narration)

    def test_narration_has_a_complete_eight_scene_structure(self):
        for episode in self.cfg['episodes']:
            self.assertEqual(len(episode['scenes']), 8)
            words = sum(len(s['narration'].split()) for s in episode['scenes'])
            self.assertGreater(words, 350)
            self.assertLess(words, 550)

    def test_every_scene_draws_and_contains_motion(self):
        for episode in self.cfg['episodes']:
            timeline = {'scenes': {s['id']: (i*24, (i+1)*24) for i, s in enumerate(episode['scenes'])}, 'takes': []}
            film = Film(episode, timeline)
            surface = skia.Surface(1920, 1080)
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
                                # Main visual region must change, beyond titles and captions.
                                self.assertGreater(np.count_nonzero(np.any(first != pixels, axis=2)), 250)


if __name__ == '__main__':
    unittest.main()
