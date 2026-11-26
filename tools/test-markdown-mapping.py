"""Tests for the Markdown mapping check (tools/markdown_mapping.py)."""
import copy
import unittest

import markdown_mapping as mm


class MappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = mm.BOOK.read_text(encoding="utf-8")
        cls.mapping = mm.load_mapping()
        cls.report = mm.check(cls.source, cls.mapping)

    def test_every_class_and_element_is_mapped_once(self):
        for key in ("errors", "unmapped_classes", "stale_classes", "unmapped_elements", "stale_elements"):
            with self.subTest(key=key):
                self.assertEqual(self.report[key], [])
        self.assertTrue(mm.ok(self.report))

    def test_constructs_are_documented(self):
        ids = [c["id"] for c in self.mapping["constructs"]]
        self.assertEqual(len(ids), len(set(ids)))
        for construct in self.mapping["constructs"]:
            with self.subTest(construct=construct["id"]):
                self.assertIn(construct["status"], mm.STATUSES)
                self.assertTrue(construct["classes"])
                self.assertTrue(construct.get("markdown"))

    def test_new_class_is_reported(self):
        edited = self.source.replace('<p class="chapter-eyebrow">Chapter 2</p>',
                                     '<p class="chapter-eyebrow brand-new">Chapter 2</p>', 1)
        report = mm.check(edited, self.mapping)
        self.assertEqual(report["unmapped_classes"], ["brand-new"])
        self.assertFalse(mm.ok(report))

    def test_stale_class_is_reported(self):
        mapping = copy.deepcopy(self.mapping)
        mapping["constructs"][0]["classes"].append("no-longer-used")
        self.assertEqual(mm.check(self.source, mapping)["stale_classes"], ["no-longer-used"])

    def test_duplicate_and_unknown_status_are_errors(self):
        mapping = copy.deepcopy(self.mapping)
        mapping["constructs"][1]["classes"].append(mapping["constructs"][0]["classes"][0])
        mapping["constructs"][2]["status"] = "magic"
        errors = mm.check(self.source, mapping)["errors"]
        self.assertTrue(any("mapped by both" in e for e in errors))
        self.assertTrue(any("unknown status" in e for e in errors))

    def test_raw_html_stays_below_the_stop_threshold(self):
        # reviews/markdown-conversion-plan.md: above about a quarter, most of
        # the benefit of Markdown is lost.
        self.assertLess(self.report["raw_share_of_authored"], 0.25)
        self.assertLess(self.report["raw_element_share_of_authored"], 0.25)
        self.assertGreater(self.report["words"]["authored-markdown"], 50000)

    def test_status_priority(self):
        mapping = {
            "constructs": [
                {"id": "g", "status": "generated", "classes": ["gen"], "markdown": "-"},
                {"id": "r", "status": "raw", "classes": ["raw"], "markdown": "-"},
                {"id": "w", "status": "template", "propagates": False, "classes": ["wrap"], "markdown": "-"},
            ],
            "elements": {"native": ["p", "div"], "raw": ["svg", "text"]},
        }
        source = ('<div class="wrap"><p>one two</p><div class="raw"><p>three</p>'
                  '<div class="gen"><p>four five six</p></div></div>'
                  '<svg><text>seven</text></svg></div>')
        words, _ = mm.word_shares(mm.eq.parse(source), mapping)
        self.assertEqual(words, {"authored-markdown": 2, "raw": 2, "generated": 3})


if __name__ == "__main__":
    unittest.main()
