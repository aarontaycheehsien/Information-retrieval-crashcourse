"""Fidelity, navigation, coverage and failure-mode checks for the generated digest."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

spec = importlib.util.spec_from_file_location('digest', Path(__file__).with_name('build-digest.py'))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class DigestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = d.BOOK.read_text(encoding='utf-8')
        cls.manifest = json.loads(d.MANIFEST.read_text(encoding='utf-8'))
        cls.template = d.TEMPLATE.read_text(encoding='utf-8')
        cls.output = d.build(cls.book, cls.manifest, cls.template)

    def test_reproducibility_and_drift(self):
        self.assertEqual(self.output, d.OUTPUT.read_text(encoding='utf-8'))
        self.assertEqual(self.output, d.build(self.book, self.manifest, self.template))
        changed = self.book.replace('The shortlist bottleneck:', 'The shortlist constraint:')
        self.assertNotEqual(changed, self.book)
        self.assertNotEqual(self.output, d.build(changed, self.manifest, self.template))

    def test_verbatim_excerpts(self):
        source, rendered = d.Document(self.book), d.Document(self.output)
        for stage in self.manifest['stages']:
            for item in stage['items']:
                label, raw, anchor = d.select(source, item)
                self.assertEqual(d.plain(raw), d.plain(d.adapt(raw, item['id'])))
                article = rendered.raw(rendered.by_id(item['id']))
                self.assertIn(d.adapt(raw, item['id']), article)
                self.assertIn(f'search-textbook.html#{anchor}', article)

    def test_coverage_and_budget(self):
        self.assertEqual(self.output.count('class="chapter-close"'), 15)
        self.assertEqual(self.output.count('class="distinction-map"'), 3)
        self.assertEqual(self.output.count('class="reflection"'), 5)
        self.assertEqual(sum(s['minutes'] for s in self.manifest['stages']), 45)
        self.assertIn('at 200 words per minute', self.output)
        self.assertIn('not tested completion times', self.output)
        self.assertIn('August 2026', self.output)
        self.assertIn('remains unproven', self.output)
        self.assertNotIn('<script', self.output)
        self.assertNotIn('<img', self.output)

    def test_ids_aria_and_links(self):
        doc = d.Document(self.output)
        ids = [n.attrs['id'] for n in doc.nodes if 'id' in n.attrs]
        self.assertEqual(len(ids), len(set(ids)))
        for n in doc.nodes:
            for attr in ('aria-labelledby', 'aria-describedby'):
                for key in n.attrs.get(attr, '').split(): self.assertIn(key, ids)
            for attr in ('href', 'src'):
                value = n.attrs.get(attr)
                if not value: continue
                u = urlsplit(value)
                if u.scheme or u.netloc: continue
                target = d.ROOT / unquote(u.path) if u.path else d.OUTPUT
                self.assertTrue(target.exists(), value)
                if u.fragment:
                    target_ids = [x.attrs.get('id') for x in d.Document(target.read_text(encoding='utf-8')).nodes]
                    self.assertIn(unquote(u.fragment), target_ids, value)

    def test_reject_bad_sources_and_manifest(self):
        for mutation in ('missing', 'duplicate', 'order', 'timing'):
            m = copy.deepcopy(self.manifest)
            if mutation == 'missing': m['stages'][0]['items'][0]['source'] = 'no-such-anchor'
            if mutation == 'duplicate': m['stages'][1]['items'][0]['id'] = 'opening-puzzles'
            if mutation == 'order': m['stages'][1]['items'].reverse()
            if mutation == 'timing': m['stages'][0]['minutes'] = 6
            with self.assertRaises(ValueError): d.build(self.book, m, self.template)
        for bad in (self.book.replace('class="chapter-close"', 'class="renamed-close"', 1),
                    self.book.replace('<strong>Puzzle 1.</strong>', '<strong>Renamed puzzle.</strong>', 1),
                    self.book.replace('If you do one thing with it,', 'Changed closing selection,', 1),
                    self.book.replace('id="sec-intro"', 'id="sec-preface"', 1)):
            with self.assertRaises(ValueError): d.build(bad, self.manifest, self.template)


if __name__ == '__main__': unittest.main(verbosity=2)
