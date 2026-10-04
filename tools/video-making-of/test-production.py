"""Check the retrospective against earlier records and review every animated scene."""
import json
import unittest
import numpy as np
import skia
import render
from film import Film


class ProductionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = render.read_config()

    def test_previous_facts_match_saved_scripts_and_reports(self):
        provenance = json.loads((render.HERE / 'provenance.json').read_text())
        old = json.loads((render.PREVIOUS / 'episodes.json').read_text())
        previous = provenance['earlier_production']
        self.assertEqual(previous['film_count'], len(old['episodes']))
        self.assertEqual(previous['narration_take_count'], len(old['lines']))
        self.assertEqual(previous['scene_count'], sum(len(e['scenes']) for e in old['episodes']))
        self.assertEqual(previous['voice'], old['voice'])
        for report in previous['verification_snapshot']:
            self.assertEqual(report['decoded_frames'], round(report['duration']*30))
            self.assertEqual(report['full_decode'], 'passed')
            self.assertEqual(report['embedded_captions'], 'passed')

    def test_narration_distinguishes_model_tools_and_historical_voice(self):
        scenes = {s['id']: s for s in self.cfg['episode']['scenes']}
        self.assertIn('setup you named', scenes['setup']['narration'])
        self.assertIn('how much reasoning the model applies', scenes['setup']['narration'])
        self.assertIn('Python code', scenes['art']['narration'])
        self.assertIn('with Skia', scenes['art']['narration'])
        self.assertIn('For those three films', scenes['clock']['narration'])
        self.assertIn('forty seven cached narration takes', scenes['clock']['narration'])
        self.assertEqual(self.cfg['voice']['name'], 'Microsoft David Desktop')
        self.assertIn('User supplied', json.loads((render.HERE/'provenance.json').read_text())['requested_setup']['basis'])

    def test_every_scene_draws_and_contains_motion(self):
        episode = self.cfg['episode']
        timeline = {'scenes': {s['id']: (i*24, (i+1)*24) for i, s in enumerate(episode['scenes'])}, 'takes': []}
        film, surface = Film(episode, timeline), skia.Surface(1920, 1080)
        for i, scene in enumerate(episode['scenes']):
            first = None
            for fraction in [.02, .25, .52, .82, .985]:
                with self.subTest(scene=scene['id'], time=fraction):
                    film.draw(surface.getCanvas(), i*24+fraction*24)
                    if fraction in [.25, .52]:
                        pixels = surface.makeImageSnapshot().toarray()[260:820, 140:1780]
                        if first is None:
                            first = pixels.copy()
                        else:
                            self.assertGreater(np.count_nonzero(np.any(first != pixels, axis=2)), 250)

    def test_original_posters_survive_lazy_image_decoding(self):
        episode = self.cfg['episode']
        timeline = {'scenes': {'read': (0, 24)}, 'takes': []}
        film, surface = Film(episode, timeline), skia.Surface(1920, 1080)
        film.draw(surface.getCanvas(), 12)
        pixels = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
        # Most of the first poster has a colored dark canvas, not neutral gray.
        poster = pixels[392:560, 667:973, :3].astype(int)
        self.assertGreater(np.median(poster.max(axis=2)-poster.min(axis=2)), 15)


if __name__ == '__main__':
    unittest.main()
