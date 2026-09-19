"""Build a static reading route from explicit, uniquely resolved book selections."""
import argparse
from collections import Counter
from html import escape, unescape
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'search-textbook.html'
OUTPUT = ROOT / 'read-this-first.html'
MANIFEST = ROOT / 'data/digest-selections.json'
TEMPLATE = ROOT / 'tools/digest-template.html'
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Node:
    def __init__(self, tag, attrs, start, parent):
        self.tag, self.attrs, self.start, self.parent = tag, dict(attrs), start, parent
        self.end = None

    def has_class(self, name):
        return name in self.attrs.get('class', '').split()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.nodes, self.stack = source, [], []
        self.lines = [0]
        for m in re.finditer('\n', source): self.lines.append(m.end())
        self.feed(source)

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.position(), self.stack[-1] if self.stack else None)
        self.nodes.append(node)
        if tag in VOID: node.end = node.start + len(self.get_starttag_text())
        else: self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop().end = self.position() + len(self.get_starttag_text())

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i].tag == tag:
                self.stack[i].end = self.source.index('>', self.position()) + 1
                del self.stack[i:]
                return

    def raw(self, node):
        if node.end is None: raise ValueError(f'Unclosed selection: {node.tag}')
        return self.source[node.start:node.end]

    def by_id(self, key):
        return one([n for n in self.nodes if n.attrs.get('id') == key], f'anchor {key}')

    def inside(self, node):
        return [n for n in self.nodes if n.start > node.start and n.start < node.end]


def one(items, label):
    if len(items) != 1: raise ValueError(f'Expected exactly one {label}; found {len(items)}')
    return items[0]


def plain(value):
    value = re.sub(r'<!--.*?-->', '', value, flags=re.S)
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', value))).strip()


def select(doc, item):
    source = doc.by_id(item['source'])
    kind = item['kind']
    if kind == 'summary':
        inside = doc.inside(source)
        summary = one([n for n in inside if n.has_class('chapter-close')], 'chapter summary')
        heading = one([n for n in inside if n.tag == 'h2'], 'chapter heading')
        eyebrow = one([n for n in inside if n.has_class('chapter-eyebrow')], 'chapter label')
        # Ignore decorative heading permalinks when deriving titles.
        title = plain(re.sub(r'<a\b[^>]*class="heading-anchor"[^>]*>.*?</a>', '', doc.raw(heading), flags=re.S))
        return plain(doc.raw(eyebrow)) + ' · ' + title, doc.raw(summary), heading.attrs['id']
    if kind == 'panel':
        panel = source.parent
        if panel is None or not panel.has_class('distinction-map'):
            raise ValueError(f'{item["source"]}: expected a distinction panel')
        # The generated article supplies an h3; remove only the original heading.
        raw = doc.raw(panel).replace(doc.raw(source), '', 1)
        raw = raw.replace(f' aria-labelledby="{item["source"]}"', '')
        return plain(doc.raw(source)), raw, item['source']
    if kind == 'puzzles':
        following = [n for n in doc.nodes if n.start > source.start and n.tag in ('h2','h3')]
        boundary = following[0].start
        paragraphs = [n for n in doc.nodes if source.end < n.start < boundary and n.tag == 'p'
                      and re.match(r'<p><strong>Puzzle [123]\.</strong>', doc.raw(n))]
        if len(paragraphs) != 3: raise ValueError('Expected the three opening puzzle paragraphs')
        return 'Three observations to keep open', '\n'.join(doc.raw(n) for n in paragraphs), item['source']
    if kind == 'recommendation':
        candidates = doc.inside(source.parent)
        first = one([n for n in candidates if n.tag == 'p' and plain(doc.raw(n)).startswith('If you do one thing with it,')], 'closing recommendation')
        second = one([n for n in candidates if n.tag == 'p' and plain(doc.raw(n)).startswith('Start with one comparison using')], 'closing kit link')
        return 'Build a local evaluation set', doc.raw(first) + '\n' + doc.raw(second), item['source']
    raise ValueError(f'Unknown selection kind: {kind}')


def adapt(raw, prefix):
    """Only change navigation/IDs: every excerpt word stays in its source order."""
    ids = re.findall(r'\bid="([^"]+)"', raw)
    for key in ids:
        raw = raw.replace(f'id="{key}"', f'id="{prefix}-{key}"')
    def aria(match):
        values = [f'{prefix}-{v}' if v in ids else v for v in match[2].split()]
        return match[1] + '="' + ' '.join(values) + '"'
    raw = re.sub(r'(aria-labelledby|aria-describedby)="([^"]+)"', aria, raw)
    # Source references always lead to the complete book, not to an incidental excerpt.
    raw = re.sub(r'href="#([^"]+)"', r'href="search-textbook.html#\1"', raw)
    return raw


def build(book, manifest, template):
    if manifest.get('schema_version') != 1: raise ValueError('Unsupported manifest version')
    doc = Document(book)
    if any(c != 1 for c in Counter(n.attrs['id'] for n in doc.nodes if 'id' in n.attrs).values()):
        raise ValueError('Duplicate book IDs')
    stages = manifest['stages']
    if len(stages) != 5 or sum(s['minutes'] for s in stages) != 45:
        raise ValueError('Expected five stages totalling 45 minutes')
    items = [i for s in stages for i in s['items']]
    ids = [s['id'] for s in stages] + [i['id'] for i in items]
    if len(set(ids)) != len(ids) or any(not re.fullmatch('[a-z][a-z0-9-]*', i) for i in ids):
        raise ValueError('Invalid or duplicate digest IDs')
    chapters = [n.attrs['id'] for n in doc.nodes if n.tag == 'section' and n.has_class('chapter')
                and not n.has_class('appendix') and not n.has_class('backsection') and n.attrs.get('id') != 'sec-preface']
    selected = [i['source'] for i in items if i['kind'] == 'summary']
    if selected != chapters or len(selected) != 15: raise ValueError('Chapter summaries must cover all 15 chapters once, in order')
    if Counter(i['kind'] for i in items) != {'summary':15, 'panel':3, 'puzzles':1, 'recommendation':1}:
        raise ValueError('Unexpected excerpt coverage')
    blocks, contents = [], []
    for number, stage in enumerate(stages, 1):
        title = escape(stage['title']); key = stage['id']
        contents.append(f'<li><a href="#{key}">{title}</a> <span>· {stage["minutes"]} minutes including reflection</span></li>')
        articles = []
        for item in stage['items']:
            label, raw, anchor = select(doc, item)
            articles.append(f'<article class="excerpt" id="{item["id"]}" aria-labelledby="{item["id"]}-title">\n'
                            f'<h3 id="{item["id"]}-title">{escape(label)}</h3>\n{adapt(raw,item["id"])}\n'
                            f'<p class="source-link"><a href="search-textbook.html#{anchor}">Read the full explanation and evidence</a></p>\n</article>')
        blocks.append(f'<section class="digest-stage" id="{key}" aria-labelledby="{key}-title">\n'
                      f'<h2 id="{key}-title">{number}. {title}<span class="stage-budget">{stage["minutes"]} minutes · reading and reflection</span></h2>\n'
                      + '\n'.join(articles) + f'\n<aside class="reflection" aria-label="Reflection prompt"><p><strong>Pause and reflect</strong></p><p>{escape(stage["prompt"])}</p></aside>\n</section>')
    output = template.replace('{{STAGES}}', '\n'.join(blocks)).replace('{{CONTENTS}}', '\n'.join(contents))
    # Count visible reading prose in main, including prompts; not menus or footer.
    main = re.search(r'<main\b.*?</main>', output, re.S)[0]
    count = len(plain(main).split())
    output = output.replace('{{WORD_COUNT}}', f'{count:,}').replace('{{READING_MINUTES}}', str(math.ceil(count/200)))
    if re.search(r'{{[A-Z_]+}}', output): raise ValueError('Unresolved template placeholder')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        result = build(BOOK.read_text(encoding='utf-8'), json.loads(MANIFEST.read_text(encoding='utf-8')), TEMPLATE.read_text(encoding='utf-8'))
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != result:
                raise ValueError('Digest is stale; run python tools/build-digest.py')
            print('PASS: digest is up to date.')
        else:
            OUTPUT.write_text(result, encoding='utf-8', newline='\n')
            print('Built read-this-first.html from 15 chapter summaries, 3 panels and opening/closing excerpts.')
    except (ValueError, KeyError) as error:
        parser.exit(1, f'ERROR: {error}\n')


if __name__ == '__main__': main()
