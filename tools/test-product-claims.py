"""Offline registry and integration checks. Run with Python's standard library."""
from copy import deepcopy
from datetime import date
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest
from html import unescape
from urllib.parse import unquote
import product_claims as p


class ClaimsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.book, cls.notes = p.load()

    def claim(self):
        return deepcopy(next(c for c in self.data['claims'] if c['id']=='primo-candidate-budget'))

    def review(self, c, when, finding='supported'):
        c['reviews'].append({'checked_on':when,'finding':finding,'notes':'Test review', 'evidence_indices':[0]})

    def test_dates(self):
        self.assertIsNone(p.date_bounds(None))
        self.assertEqual(p.date_bounds('2024-02'),(date(2024,2,1),date(2024,2,29)))
        self.assertEqual(p.date_bounds('2024'),(date(2024,1,1),date(2024,12,31)))
        for value in ['2025-02-29','2026-13','2026-1','yesterday',2026,'0000']:
            with self.subTest(value=value), self.assertRaises((ValueError,TypeError)):
                p.date_bounds(value)

    def test_overdue_boundary(self):
        c=self.claim(); c['reviews']=[]; self.review(c,'2025-09-19')
        self.assertIn('within-window',p.currency(c,date(2026,9,19))['flags'])
        self.assertIn('overdue',p.currency(c,date(2026,9,20))['flags'])

    def test_partial_dates_conservative(self):
        c=self.claim(); c['reviews']=[]; self.review(c,'2025-09')
        st=p.currency(c,date(2026,9,2))
        self.assertIn('overdue',st['flags']); self.assertTrue(st['approximate'])

    def test_failed_check_does_not_refresh(self):
        c=self.claim(); c['reviews']=[]
        self.review(c,'2024-01-01'); self.review(c,'2026-09-19','not established')
        st=p.currency(c,date(2026,9,19))
        self.assertEqual(st['last_support'],'2024-01-01')
        self.assertEqual(st['last_attempt'],'2026-09-19')
        self.assertEqual(st['flags'],['unresolved','overdue'])
        self.review(c,'2026-09-20','changed')
        self.assertIn('unresolved',p.currency(c,date(2026,9,20))['flags'])
        self.review(c,'2026-09-21')
        self.assertEqual(p.currency(c,date(2026,9,21))['flags'],['within-window'])

    def test_unknown_and_historical(self):
        c=self.claim(); c['reviews']=[]
        self.assertIn('unknown',p.currency(c,date(2026,9,19))['flags'])
        c['temporal_scope']='historical'; self.review(c,'2020-01-01')
        self.assertEqual(p.currency(c,date(2026,9,19))['flags'],['historical'])
        self.review(c,'2026-09-01','changed')
        self.assertEqual(p.currency(c,date(2026,9,19))['flags'],['unresolved','historical'])

    def test_future_reviews_do_not_leak(self):
        c=self.claim(); c['reviews']=[]; self.review(c,'2027-01-01')
        self.assertIn('unknown',p.currency(c,date(2026,9,19))['flags'])

    def test_validation_rejects_bad_records(self):
        mutations=[lambda d:d['claims'].append(deepcopy(d['claims'][0])),
          lambda d:d['claims'][0].update(evidence_date='2026-02-30'),
          lambda d:d['claims'][0]['locations'][0].update(anchor='absent-anchor'),
          lambda d:d['claims'][0]['locations'][0].update(excerpt='No such source wording exists.'),
          lambda d:d['claims'][0]['evidence'][0].update(url='javascript:alert(1)'),
          lambda d:d['claims'][0]['evidence'][0].update(url='../outside.png'),
          lambda d:d['claims'][0]['reviews'][0].update(evidence_indices=[999]),
          lambda d:d['claims'][0]['reviews'][0].update(finding='verified forever'),
          lambda d:d['teaching_groups'].pop(),
          lambda d:d['claims'][0].update(teaching_groups=['missing'])]
        for i,mutate in enumerate(mutations):
            with self.subTest(case=i):
                bad=deepcopy(self.data); mutate(bad)
                with self.assertRaises(ValueError): p.validate(bad,self.book)

    def test_views_and_preservation(self):
        rendered=p.backlinks(p.replace_block(self.book,'REGISTER',p.book_html(self.data)),self.data)
        self.assertEqual(rendered,self.book)
        self.assertEqual(p.strip_generated(rendered),p.strip_generated(self.book))
        self.assertEqual(p.backlinks(rendered,self.data),rendered)
        self.assertEqual(p.replace_block(self.notes,'TEACHING',p.notes_html(self.data)),self.notes)
        self.assertEqual(self.book.count('class="claim-entry"'),len(self.data['claims']))
        self.assertEqual(self.notes.count('id="claims-group-'),9)
        # Teaching view links reference canonical records rather than separate copies.
        for ident in re.findall('search-textbook.html#claim-([a-z0-9-]+)',self.notes):
            self.assertIn(f'id="claim-{ident}"',self.book)

    def test_local_links_and_duplicate_ids(self):
        for path in [p.BOOK,p.NOTES]:
            html=path.read_text(encoding='utf-8')
            ids=re.findall(r'\bid="([^"]+)"',html)
            self.assertEqual(len(ids),len(set(ids)),path.name)
            for href in re.findall(r'href="([^"]+)"',html):
                if re.match(r'[a-z]+:',href): continue
                file,_,anchor=unquote(unescape(href)).partition('#')
                target=(path.parent / file) if file else path
                self.assertTrue(target.is_file(),href)
                if anchor and target.suffix=='.html':
                    self.assertTrue(f'id="{anchor}"' in target.read_text(encoding='utf-8'),href)

    def test_report_is_read_only_and_reproducible(self):
        before=[x.read_bytes() for x in [p.DATA,p.BOOK,p.NOTES]]
        args=[sys.executable,str(p.ROOT/'tools/check-product-claims.py'),'--as-of','2027-10-01']
        one=subprocess.check_output(args); two=subprocess.check_output(args)
        self.assertEqual(one,two)
        self.assertIn(b'OVERDUE:',one)
        self.assertEqual(before,[x.read_bytes() for x in [p.DATA,p.BOOK,p.NOTES]])


if __name__=='__main__': unittest.main(verbosity=2)
