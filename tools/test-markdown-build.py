"""Unit tests for the Markdown build (tools/markdown/build_md.py and book.lua).

The full round trip, with every generator and companion page, is
tools/markdown/pilot.py; these tests pin the individual conventions.
Requires pandoc.
"""
import html
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "markdown"))
import build_md as b  # noqa: E402
import html_to_md  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BOOK = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
# The patterns maintain.py uses to number assets: the build must satisfy them.
TABLE_LBL_RE = re.compile(r'<p class="(asset-label[^"]*)"(?:\s+id="[^"]*")?>Table\s+[0-9A-Za-z]+\.\d+')
FIG_LBL_RE = re.compile(r'<span class="(asset-label-inline[^"]*)"(?:\s+id="[^"]*")?>Figure\s+[0-9A-Za-z]+\.\d+')
TABLE_RE = re.compile(r'<div class="table-wrap"><table>')


def build(markdown):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "x.md"
        path.write_text(markdown, encoding="utf-8")
        return b.build_file(path, Path(tmp))


def body(markdown):
    return build("---\nkind: fragment\n---\n\n" + markdown)[0]


class StageMapTests(unittest.TestCase):
    def test_renderer_reproduces_every_standard_map(self):
        data = b.load_stage_map()
        label_to_key = {s["label_html"]: s["key"] for s in data["stages"]}
        maps = re.findall(r'<div class="stage-map"[^>]*>.*?</div></div>', BOOK, re.S)
        exact = 0
        for m in maps:
            on = [label_to_key.get(x, "?") for x in re.findall(r'class="stage on"[^>]*>(.*?)</a>', m)]
            label = html.unescape(re.search(r'aria-label="([^"]*)"', m)[1])
            controller = re.search(r"stage-controller (on|off)", m)[1]
            try:
                exact += b.render_stage_map(on, controller, "" if label == data["default_label"] else label, data) == m
            except b.BuildError:
                pass
        self.assertEqual(len(maps), 15)
        self.assertEqual(exact, 14)  # the Part II map is bespoke and stays raw

    def test_unknown_stage_is_an_error(self):
        with self.assertRaises(b.BuildError):
            b.render_stage_map(["retrieval"])


class FilterTests(unittest.TestCase):
    def test_heading_anchor(self):
        out = body("### Why *this* matters {#why}\n")
        self.assertEqual(out.strip(), '<h3 id="why">Why <em>this</em> matters<a aria-label="Link to Why this matters" '
                                      'class="heading-anchor" href="#why">#</a></h3>')

    def test_table_matches_maintain_patterns(self):
        out = body("| A | B |\n|---|---|\n| `x` | y |\n\n: Caption with *stress*.\n")
        self.assertTrue(TABLE_LBL_RE.search(out))
        self.assertTrue(TABLE_RE.search(out))
        self.assertIn("Table 0.0 — Caption with <em>stress</em>.</p>", out)
        self.assertNotIn('class="header"', out)
        self.assertNotIn("<caption>", out)

    def test_figure_matches_maintain_patterns(self):
        out = body(':::: {.figure key="k"}\nA title\n\n![Alt *text*](images/none.png){width="10" height="5"}\n\n'
                   '::: caption\nThe caption.\n:::\n::::\n')
        self.assertTrue(FIG_LBL_RE.search(out))
        self.assertIn('<figure class="ir-figure" aria-labelledby="k-title">', out)
        self.assertIn('<p class="figure-title" id="k-title">A title</p>', out)
        self.assertIn('alt="Alt text"', out)
        self.assertNotIn("srcset", out)  # no .960.webp sibling

    def test_srcset_is_derived_only_when_the_webp_exists(self):
        src = ("images/02%20Boolean%20search%20-%20words%20as%20admission%20rules/"
               "ChatGPT%20Image%20Jul%2026,%202026,%2009_49_10%20PM.png")
        out = body(f':::: {{.figure key="k"}}\nT\n\n![a]({src}){{width="1448" height="1086"}}\n\n::: caption\nC\n:::\n::::\n')
        self.assertIn(f'srcset="{src[:-4].replace(",", "%2C")}.960.webp 960w, {src} 1448w"', out)
        self.assertIn('sizes="(max-width: 800px) 100vw, 760px"', out)

    def test_footnotes_keep_their_names(self):
        out, notes = build("---\nkind: fragment\n---\n\nText.[^my-note]\n\n[^my-note]: One.\n\n    Two.\n")
        self.assertIn('<sup id="fnref:my-note"><a class="footnote-ref" href="#fn:my-note">0</a></sup>', out)
        self.assertTrue(notes.startswith('<li id="fn:my-note">'))
        self.assertIn('Two.\u00a0<a class="footnote-backref" href="#fnref:my-note" '
                      'title="Jump back to footnote 0 in the text">↩</a></p>', notes)

    def test_maths_keeps_mathjax_delimiters(self):
        out = body("Inline $k_1$ here.\n\n::: math\n$$\na=\\frac{b}{c}\n$$\n:::\n")
        self.assertIn("Inline \\(k_1\\) here.", out)
        self.assertIn("$$\na=\\frac{b}{c}\n$$", out)

    def test_aside_derives_label_and_name(self):
        out = body('::: {.common-confusion label="IR terminology"}\n#### Head {#h}\n\nBody.\n:::\n')
        self.assertIn('<aside class="common-confusion" aria-labelledby="h">\n<p class="common-confusion-label">IR terminology</p>', out)
        out = body('::: {.common-confusion label="T" label-class="callout-label" aria-labelledby="p1"}\n'
                   '::: {#p1}\nBody.\n:::\n:::\n')
        self.assertIn('<aside class="common-confusion" aria-labelledby="p1">\n<p class="callout-label">T</p>', out)
        self.assertIn('<p id="p1">Body.</p>', out)

    def test_self_check_and_details(self):
        out = body("::: self-check\nWhy?\n\n:   Because.\n:::\n\n::: {.details .technical-note}\nMore\n\nHidden.\n:::\n")
        self.assertIn('<section class="self-check" aria-label="Questions on this chapter"><p class="self-check-label">'
                      'Check yourself</p>', out)
        self.assertIn('<details class="self-check-q"><summary>Why?</summary>', out)
        self.assertIn("<p>Because.</p>", out)
        self.assertIn('<details class="technical-note"><summary>More</summary>', out)

    def test_lists_code_and_text_survive_as_written(self):
        out = body("1. one\n2. two\n\n```\nD1  two  spaces\n```\n\nQuote “curly” 'straight' -- and\\ nbsp.\n")
        self.assertIn("<ol>", out)
        self.assertNotIn('type="1"', out)
        self.assertIn("<pre><code>D1  two  spaces</code></pre>", out)
        self.assertIn("Quote “curly” 'straight' -- and\u00a0nbsp.", out)

    def test_legacy_anchor_and_element_spans(self):
        out = body("::: {#old .legacy-anchor}\n:::\n\nA [d]{.var} and [*no*]{.verdict}.\n")
        self.assertIn('<span id="old" class="legacy-anchor"></span>', out)
        self.assertIn("<var>d</var>", out)
        self.assertIn('<em class="verdict">no</em>', out)


class ConverterTests(unittest.TestCase):
    def test_paragraph_starts_are_escaped(self):
        conv = html_to_md.Converter("", Path("."))
        node = html_to_md.N("text", text="2026. A year. - not a list")
        text = conv.para_text([node])
        self.assertTrue(text.startswith("2026\\."))
        self.assertEqual(body(text + "\n").strip(), "<p>2026. A year. - not a list</p>")

    def test_sentences_break_onto_lines_without_changing_text(self):
        conv = html_to_md.Converter("", Path("."))
        text = conv.para_text([html_to_md.N("text", text="One. Two? “Three.” Four")])
        self.assertEqual(text, "One.\nTwo?\n“Three.”\nFour")
        self.assertEqual(body(text + "\n").strip(), "<p>One. Two? “Three.” Four</p>")


if __name__ == "__main__":
    unittest.main()
