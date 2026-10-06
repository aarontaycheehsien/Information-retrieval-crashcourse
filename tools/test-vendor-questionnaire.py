"""Source coverage, generation and local-link checks; standard library only."""
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools/build-vendor-questionnaire.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
book = builder.BOOK.read_text(encoding='utf-8')
mapping = json.loads(builder.MAPPING.read_text(encoding='utf-8'))
template = builder.TEMPLATE.read_text(encoding='utf-8')
output = builder.OUTPUT.read_text(encoding='utf-8')
assert output == builder.render(book, mapping, template), 'Generated page is stale'
ids = [q['id'] for q in mapping['questions']]
assert ids == [f'Q{i:02}' for i in range(1,20)] + [f'E{i:02}' for i in range(1,5)] + [f'G{i:02}' for i in range(1,8)]
assert len(mapping['sections'][0]['groups']) == 6
assert re.findall(r'data-question="([QEG]\d+)"', output) == ids
for q in mapping['questions']:
    card = re.search(rf'<article[^>]*data-question="{q["id"]}".*?</article>', output, re.S).group()
    source = builder.source_content(book, q)
    # The generated heading moves the leading strong text without rewriting it;
    # lettering a body of questions keeps every word in order.
    title, body = builder.split_title(source)
    assert title in card, q['id']
    detail = re.search(r'class="question-detail[^"]*"[^>]*>(.*?)</(?:p|ol)>', card, re.S)
    assert builder.prose(body) == (builder.prose(detail[1]) if detail else ''), q['id']
    assert q['listen_for'] and 'class="listen-for"' in card, q['id']
    for field in ['Vendor answer / existing answer reference', 'Vendor supporting evidence',
                  'Library verification', 'Date checked', 'Reason if not applicable', 'Unresolved follow-up']:
        assert field in card, (q['id'], field)
    assert len(re.findall('class="writing-line"', card)) == 9
    for related in q.get('related', []):
        assert related in ids and f'href="#{related.lower()}"' in card
assert 'id="section-e" hidden' in output and 'id="section-g" hidden' in output
assert 'localStorage' not in output and 'fetch(' not in output
assert output.count('class="question-page"') == 17
assert re.findall(r'<li id="(q13[a-z])">', output) == ['q13a', 'q13b']
assert output.count('<ul class="question-list">') == 3

# Source edits update the generated copy; structural drift must stop generation.
changed = book.replace('What does the system infer, change and decide?', 'What does this system infer, change and decide?', 1)
assert 'What does this system infer, change and decide?' in builder.render(changed, mapping, template)
for bad in [book.replace('id="vendor-q01"','id="removed-q01"',1),
            book.replace('<li id="vendor-e01">','<li>New unmapped question?</li><li id="vendor-e01">',1),
            book.replace(' Chapter 12 records both kinds of change:', ' Changed narrative boundary:',1)]:
    try:
        builder.render(bad, mapping, template)
    except ValueError:
        pass
    else:
        raise AssertionError('Source drift was not rejected')

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.hrefs=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='a' and 'href' in attrs: self.hrefs.append(attrs['href'])

pages={name:Links((ROOT/name).read_text(encoding='utf-8')) for name in ['vendor-questionnaire.html','search-textbook.html','teaching-notes.html']}
for name,page in pages.items():
    assert len(page.ids)==len(set(page.ids)), name
    for href in page.hrefs:
        url=urlsplit(href)
        if url.scheme or url.netloc: continue
        target=ROOT/unquote(url.path) if url.path else ROOT/name
        assert target.is_file(), (name,href)
        if url.fragment and target.suffix=='.html':
            dest=pages.get(target.name) or Links(target.read_text(encoding='utf-8'))
            assert unquote(url.fragment) in dest.ids, (name,href)
assert pages['search-textbook.html'].hrefs.count('vendor-questionnaire.html')==3
assert 'vendor-questionnaire.html' in pages['teaching-notes.html'].hrefs
assert re.search(r'\((?:https://[^)]*/)?vendor-questionnaire\.html\)', (ROOT/'README.md').read_text(encoding='utf-8'))
print('PASS: all 30 questions, six core groups, response fields, declared omissions, source drift guards and local links.')
