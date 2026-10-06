"""Offline glossary mapping, preservation and generation tests."""
from copy import deepcopy
from html import unescape
import json
import re
import unittest
import glossary_hub as g


class GlossaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.mapping,cls.book=g.load()

    def test_all_entries_and_targets(self):
        entries,headings=g.validate(self.mapping,self.book)
        self.assertEqual(len(entries),84)
        self.assertEqual(len(self.mapping['terms']),84)
        self.assertEqual(len(re.findall(r'<dt id="term-',self.book)),84)
        self.assertGreater(len(headings),150)
        for term in self.mapping['terms']:
            self.assertTrue(term['targets'])
            self.assertTrue(all(dest in headings for dest in term['targets']))

    def test_idempotence_and_wording(self):
        built=g.build(self.mapping,self.book)
        self.assertEqual(built,self.book)
        self.assertEqual(g.definitions(built),g.definitions(self.book))
        self.assertEqual(g.build(self.mapping,built),built)
        # Removing only generated navigation/attributes recovers identical definitions.
        definitions=g.definitions(self.book)
        original=self.book
        original=g.GENERATED.sub('',original)
        original=re.sub(r'<span class="glossary-definition" id="[^"]+">(.*?)</span>',r'\1',original,flags=re.S)
        self.assertEqual(definitions,g.definitions(original))

    def test_reject_bad_mapping(self):
        changes=[lambda m:m['terms'].pop(),
          lambda m:m['terms'].append(deepcopy(m['terms'][0])),
          lambda m:m['terms'][0].update(id=m['terms'][1]['id']),
          lambda m:m['terms'][0].update(targets=[]),
          lambda m:m['terms'][0].update(targets=['absent']),
          lambda m:m['terms'][0].update(targets=['claim-primo-candidate-budget']),
          lambda m:m['terms'][0]['aliases'].append('BM25'),
          lambda m:m['terms'][0].update(related=['absent']),
          lambda m:m.update(shared_aliases={})]
        for i,change in enumerate(changes):
            with self.subTest(case=i):
                bad=deepcopy(self.mapping);change(bad)
                with self.assertRaises(ValueError):g.build(bad,self.book)

    def test_aliases_and_qualifiers(self):
        self.assertEqual(g.normalise('Bi–encoder'),g.normalise('BI encoder'))
        self.assertEqual(g.normalise('Précision@k'),'precision k')
        self.assertEqual(self.mapping['shared_aliases']['pooling'],['pooling-encoder','pooling-test-collections'])
        terms={t['id']:t for t in self.mapping['terms']}
        self.assertNotEqual(terms['pooling-encoder']['targets'],terms['pooling-test-collections']['targets'])
        self.assertEqual(len(terms['hybrid-multi-stage']['targets']),2)

    def test_index_is_small_unique_and_not_full_text(self):
        raw=re.search(r'<script type="application/json" id="book-lookup-index">(.*?)</script>',self.book,re.S)[1]
        index=json.loads(raw)
        self.assertLess(len(raw.encode('utf-8')),140000)
        self.assertEqual(len(index),len({i['id'] for i in index}))
        self.assertEqual(sum(i['kind']=='Term' for i in index),84)
        self.assertFalse(any(i['id'].startswith(('claim-','claims-product-')) for i in index))
        self.assertFalse(any('claim-status' in i['text'] for i in index))
        self.assertNotIn('<',raw)
        for i in index:
            self.assertIn(i['kind'],['Term','Section'])
            self.assertTrue(i['location'])
            if i['kind']=='Section':self.assertEqual(i['text'],i['title'])

    def test_glossary_links_and_definition_spans(self):
        glossary=g.BLOCK.search(self.book)[0]
        ids=re.findall(r'\bid="([^"]+)"',self.book)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertRegex(glossary,r'^<details[^>]*\bopen>')
        for href in re.findall(r'href="#([^"]+)"',glossary): self.assertIn(unescape(href),ids)
        for term in self.mapping['terms']:
            self.assertIn('id="definition-'+term['id']+'"',glossary)


if __name__=='__main__':unittest.main(verbosity=2)
