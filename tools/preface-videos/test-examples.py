"""Check preface coverage, evidence limits, narration timing, and animated scenes."""
import re
import unittest
from html.parser import HTMLParser

import numpy as np
import skia
import render
from scenes import Film, LABELS, ROUTES


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        self.data.append(data)


class PrefaceExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = render.read_config()
        source = (render.ROOT/'search-textbook.html').read_text(encoding='utf-8')
        start = source.index('id="sec-preface"')
        parser = PlainText()
        parser.feed(source[start:source.index('<section class="part-divider" id="part1"', start)])
        cls.source = re.sub(r'\s+', ' ', ' '.join(parser.data))
        cls.narration = ' '.join(s['narration'] for e in cls.cfg['episodes'] for s in e['scenes'])

    def test_core_distinctions_are_grounded(self):
        for phrase in ['why did this record get into the candidate set at all',
                       'why did it rank where it did',
                       'No single neural architecture has simply replaced lexical retrieval',
                       'semantic search as another name for dense retrieval',
                       'A citation list alone establishes neither faithful writing nor adequate retrieval']:
            self.assertIn(phrase, self.source)
        for phrase in ['why it was admitted, then why it ranked there',
                       'Semantic search, for example, is not another name for dense retrieval',
                       'a citation list alone establishes neither faithful writing nor adequate retrieval']:
            self.assertIn(phrase, self.narration)

    def test_labels_audiences_and_routes_have_source_support(self):
        self.assertEqual(len(LABELS), 6)
        for label in LABELS:
            self.assertIn(label.lower().replace('ai-powered', 'AI-powered'), self.source)
        self.assertEqual(len(ROUTES), 5)
        for phrase in ['Information literacy librarians', 'Evidence synthesis librarians',
                       'Systems and discovery librarians', 'Short orientation', 'Instruction',
                       'Evidence synthesis', 'Procurement', 'Curiosity',
                       'On this route, Appendix F is core rather than optional']:
            self.assertIn(phrase, self.source)
        self.assertIn('Appendix F is core reading on this route', self.narration)

    def test_scripts_keep_examples_and_scope_honest(self):
        for phrase in ['schematic, not measured scores', 'not a real citation',
                       'glowing paper is hypothetical', 'dated illustrations',
                       'current product recommendation', 'No prior information retrieval knowledge',
                       'generation remains outside its main scope']:
            self.assertIn(phrase, self.narration)
        for episode in self.cfg['episodes']:
            words = sum(len(s['narration'].split()) for s in episode['scenes'])
            self.assertGreater(words, 300)
            self.assertLess(words, 450)

    def test_word_reveal_uses_actual_scene_relative_time(self):
        ep = self.cfg['episodes'][0]
        film = Film(ep, {'scenes': {'inside': (100, 125)},
                         'takes': [{'id': 'inside', 'words': [{'text': 'label.', 'start': 107.4}]}]})
        self.assertAlmostEqual(film.at('inside', 'label'), 7.4)
        self.assertEqual(film.at('inside', 'not-spoken', 8), 8)

    def test_every_scene_draws_and_moves(self):
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
