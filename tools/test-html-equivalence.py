"""Tests for the Markdown-conversion equivalence check (tools/html_equivalence.py)."""
import html
import json
import unittest
from pathlib import Path

import html_equivalence as eq

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "search-textbook.html"


def same(a, b, **kw):
    return not eq.compare(eq.load(None, "a", source=a, **kw), eq.load(None, "b", source=b, **kw))


def reserialise(source):
    """Write the book back out the way a different HTML writer might.

    Newlines around every block element, attributes in reverse order,
    self-closing void elements and every non-ASCII character as a numeric
    character reference. None of this changes how the page renders.
    """
    out = []

    def esc(text, attr=False):
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if attr:
            text = text.replace('"', "&quot;")
        return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in text)

    def walk(node, raw, block_parent):
        for child in node.children:
            if child.kind == "text":
                out.append(child.text if raw else esc(child.text))
            elif child.kind == "comment":
                out.append(f"<!--{child.text}-->")
            elif child.kind == "decl":
                out.append(f"<!{child.text}>")
            elif child.kind == "pi":
                out.append(f"<?{child.text}>")
            else:
                block = child.tag not in eq.INLINE
                if block and block_parent and not raw:
                    out.append("\n")
                attrs = "".join(
                    f' {k}="{esc(v or "", True)}"' for k, v in reversed(child.attrs))
                if child.tag in eq.VOID:
                    out.append(f"<{child.tag}{attrs} />")
                else:
                    out.append(f"<{child.tag}{attrs}>")
                    walk(child, raw or child.tag in eq.VERBATIM, block)
                    out.append(f"</{child.tag}>")
                if block and block_parent and not raw:
                    out.append("\n")

    walk(eq.parse(source), False, True)
    return "".join(out)


class BookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = BOOK.read_text(encoding="utf-8")
        cls.lines = eq.load(BOOK, source=cls.source)

    def test_book_parses_strictly_and_equals_itself(self):
        self.assertGreater(len(self.lines), 30000)
        self.assertEqual(eq.compare(self.lines, eq.load(BOOK)), [])

    def test_reserialised_book_is_equivalent(self):
        rewritten = reserialise(self.source)
        self.assertNotEqual(rewritten, self.source)
        self.assertEqual(eq.compare(self.lines, eq.load(None, "rewritten", source=rewritten)), [])

    def test_deliberate_edits_fail(self):
        edits = [
            ("delulu AND job</p>", "delulu AND jobs</p>"),          # one word of prose
            ('id="boolean-admission"', 'id="boolean-admision"'),     # an anchor
            ('class="chapter-eyebrow">Chapter 2<', 'class="chapter-kicker">Chapter 2<'),
            ("<!-- END PRODUCT CLAIMS REGISTER", "<!-- END CLAIMS REGISTER"),  # generator marker
            ("<p>A Boolean system requires", "<p><em>A</em> Boolean system requires"),
        ]
        for old, new in edits:
            with self.subTest(old=old):
                self.assertEqual(self.source.count(old), 1)
                edited = self.source.replace(old, new)
                report = eq.compare(self.lines, eq.load(None, "edited", source=edited))
                self.assertTrue(report)
                self.assertTrue(report[0].startswith("Not equivalent"))

    def test_section_restriction(self):
        edited = self.source.replace("delulu AND job</p>", "delulu AND jobs</p>")
        for section, differs in [("sec-intro", False), ("sec-boolean-admission", True)]:
            with self.subTest(section=section):
                a = eq.load(BOOK, source=self.source, section=section)
                b = eq.load(None, "edited", source=edited, section=section)
                self.assertEqual(bool(eq.compare(a, b)), differs)

    def test_baseline_manifest_matches_its_commit(self):
        manifest = json.loads(eq.BASELINE_MANIFEST.read_text(encoding="utf-8"))
        source = eq._git_show(manifest["commit"], manifest["source"])
        lines = eq.load(None, "baseline", source=source)
        self.assertEqual(eq.digest(lines), manifest["canonical_sha256"])
        self.assertEqual(len(lines), manifest["canonical_lines"])


class RuleTests(unittest.TestCase):
    def test_insignificant_differences(self):
        pairs = [
            ('<p class="b a" id="x">t</p>', '<p id="x" class="a  b">t</p>'),
            ("<p>A &amp; B&#8217;s</p>", "<p>A & B’s</p>"),
            ("<p>a&nbsp;b</p>", "<p>a b</p>"),
            ("<p>a<br>b</p>", "<p>a<br/>b</p>"),
            ('<script defer="" src="x.js"></script>', '<script defer src="x.js"></script>'),
            ("<p>one\n  two</p>", "<p>one two</p>"),
            ("<div><p>a</p><p>b</p></div>", "<div>\n  <p>a</p>\n\n  <p>b</p>\n</div>"),
            ("<li><p>a</p></li>", "<li>\n<p>a</p>\n</li>"),
            ("<p>a</p>", "<p>\n a\n</p>"),
            ("<!-- BEGIN X -->", "<!--   BEGIN X\n-->"),
        ]
        for a, b in pairs:
            with self.subTest(a=a):
                self.assertTrue(same(a, b))

    def test_significant_differences(self):
        pairs = [
            ("<p>a b</p>", "<p>a b</p>"),                       # NBSP is not a space
            ("<p>a <em>b</em></p>", "<p>a<em>b</em></p>"),           # inline spacing
            ("<p><em>a</em> <strong>b</strong></p>", "<p><em>a</em><strong>b</strong></p>"),
            ("<pre>a  b</pre>", "<pre>a b</pre>"),                   # verbatim content
            ("<script>var a=1;</script>", "<script>var a = 1;</script>"),
            ('<a href="#x">t</a>', '<a href="#y">t</a>'),
            ('<img alt="a" src="x.png">', '<img alt="b" src="x.png">'),
            ("<p>a</p><p>b</p>", "<p>a</p><p>b</p><p></p>"),           # extra element
            ("<p>a</p>", "<div>a</div>"),
            ("<!-- BEGIN X -->", "<!-- BEGIN Y -->"),
            ("<p>“a”</p>", '<p>"a"</p>'),                             # smart quotes
            ("<p>a–b</p>", "<p>a-b</p>"),                             # en dash
        ]
        for a, b in pairs:
            with self.subTest(a=a):
                self.assertFalse(same(a, b))

    def test_ignore_comments_option(self):
        self.assertTrue(same("<p>a</p><!-- x -->", "<p>a</p>", ignore_comments=True))
        self.assertFalse(same("<p>a</p><!-- x -->", "<p>a</p>"))

    def test_malformed_input_is_an_error(self):
        for bad in ["<div><p>a</div>", "<p>a", "<p>a</p></p>", "<br></br>"]:
            with self.subTest(bad=bad):
                with self.assertRaises(eq.EquivalenceError):
                    eq.load(None, "bad", source=bad)

    def test_report_names_the_location(self):
        a = '<h3 id="here">H</h3><p>one</p>'
        b = '<h3 id="here">H</h3><p>two</p>'
        report = eq.compare(eq.load(None, "a", source=a), eq.load(None, "b", source=b))
        self.assertIn("#here", report[1])
        self.assertIn('-  #text "one"', report)
        self.assertIn('+  #text "two"', report)

    def test_quote_makes_invisible_characters_visible(self):
        self.assertEqual(eq._quote("a b"), '"a\\u00a0b"')
        self.assertEqual(html.unescape("&nbsp;"), " ")


if __name__ == "__main__":
    unittest.main()
