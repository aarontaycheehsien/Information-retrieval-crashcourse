"""Verify metric arithmetic, chapter fixtures, and all animated scene branches."""
import math
import unittest
import render
from scenes import (Film, BEFORE, AFTER, RELEVANT, AP_A, AP_B, GRADES_A,
                    GRADES_B, precision_at, recall, reciprocal_rank,
                    average_precision, ndcg, ROWS_BEFORE, ROWS_AFTER)


class ChapterExamples(unittest.TestCase):
    def test_chapter_reranking_changes_display_not_candidates(self):
        self.assertEqual(set(BEFORE), set(AFTER))
        for ranking, expected in [(BEFORE, .2), (AFTER, .6)]:
            self.assertEqual(precision_at(ranking, RELEVANT, 10), expected)
            self.assertEqual(recall(ranking[:10], RELEVANT), expected)
            self.assertEqual(recall(ranking, RELEVANT), 1.)

    def test_depth_and_new_candidates(self):
        recoveries = [recall(AFTER[:k], RELEVANT) for k in range(1, 21)]
        self.assertEqual(recoveries, sorted(recoveries))
        self.assertEqual(recall('ABCD', 'ABE'), recall('ABCDF', 'ABE'))
        self.assertGreater(recall('ABCDE', 'ABE'), recall('ABCD', 'ABE'))
        self.assertEqual(recall('ABCDA', 'ABE'), recall('ABCD', 'ABE'))

    def test_mrr_ignores_later_hits(self):
        self.assertEqual(reciprocal_rank([0,1,0,0,1]), .5)
        self.assertEqual(reciprocal_rank([0,1,0,0,0]), .5)
        self.assertEqual(reciprocal_rank([0]*5), 0.)
        self.assertAlmostEqual((.5+.2)/2, .35)

    def test_average_precision_has_total_relevant_denominator(self):
        self.assertAlmostEqual(average_precision(AP_A,3), 34/45)
        self.assertAlmostEqual(average_precision(AP_B,3), 8/15)
        self.assertAlmostEqual(average_precision([1,0,0],3), 1/3)
        self.assertEqual(average_precision([0,0],3), 0.)

    def test_ndcg_normalises_graded_discount(self):
        self.assertEqual(round(ndcg(GRADES_A),3), .983)
        self.assertEqual(round(ndcg(GRADES_B),3), .590)
        self.assertEqual(ndcg([3,1,0]), 1.)
        self.assertEqual(ndcg([0,0,0]), 0.)

    def test_row_mean_hides_identifier_regression(self):
        self.assertGreater(sum(ROWS_AFTER)/3, sum(ROWS_BEFORE)/3)
        self.assertAlmostEqual(ROWS_AFTER[0]/ROWS_BEFORE[0], 1/3)

    def test_every_scene_draws_at_multiple_times(self):
        import skia
        cfg = render.read_config()
        source = (render.ROOT/'search-textbook.html').read_text(encoding='utf-8')
        # Anchor checks alone would miss a changed numeric teaching fixture.
        for value in ['2/10 = 0.2', '6/10 = 0.6', '10/10 = 1.0', '0.30 to 0.33', 'SLC6A4 promoter polymorphism']:
            self.assertIn(value, source)
        for episode in cfg['episodes']:
            timeline = {'scenes': {s['id']:(i*24,(i+1)*24) for i,s in enumerate(episode['scenes'])}, 'takes':[]}
            film = Film(episode,timeline)
            surface = skia.Surface(1920,1080)
            for i,scene in enumerate(episode['scenes']):
                for fraction in [.02,.25,.52,.82,.985]:
                    with self.subTest(film=episode['id'],scene=scene['id'],time=fraction):
                        film.draw(surface.getCanvas(),i*24+fraction*24)


if __name__ == '__main__':
    unittest.main()
