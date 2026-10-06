"""Generate glossary navigation and an embedded local lookup index, not definitions."""
from collections import Counter, defaultdict
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'search-textbook.html'
MAP = ROOT / 'data/glossary-map.json'
BLOCK = re.compile(r'<details\b[^>]*\bid="glossary"[^>]*>.*?</details>', re.S)
PAIRS = re.compile(r'<dt\b[^>]*>(.*?)</dt>\s*<dd\b[^>]*>(.*?)</dd>', re.S)
GENERATED = re.compile(r'<!-- BEGIN GLOSSARY (LOOKUP|NAV) -->.*?<!-- END GLOSSARY \1 -->\n?', re.S)


def plain(value):
    value=re.sub(r'<a\b[^>]*class="heading-anchor"[^>]*>.*?</a>', '', value, flags=re.S)
    return re.sub(r'\s+', ' ', unescape(re.sub('<[^>]+>', '', value))).strip()


def normalise(value):
    value=''.join(c for c in unicodedata.normalize('NFKD',value) if not unicodedata.combining(c))
    return re.sub('[^a-z0-9]+',' ',value.lower()).strip()


def definitions(book):
    blocks=BLOCK.findall(book)
    if len(blocks)!=1: raise ValueError('Expected one glossary')
    entries=[]
    for label,body in PAIRS.findall(blocks[0]):
        body=GENERATED.sub('',body)
        wrapper=re.fullmatch(r'<span class="glossary-definition" id="[^"]+">(.*?)</span>\s*',body,re.S)
        if wrapper: body=wrapper[1]
        entries.append((plain(label), label, body))
    if not entries: raise ValueError('No glossary definitions')
    return entries


class Headings(HTMLParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=True)
        self.sections=[]; self.labels={}; self.items=[]; self.capture=None; self.eyebrow=None; self.skip_anchor=0
        self.feed(source)

    def owner(self):
        return next((s.get('id','') for s in reversed(self.sections) if set(s.get('class','').split()) & {'chapter','appendix'}),'')

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='section': self.sections.append(a)
        if tag=='p' and 'chapter-eyebrow' in a.get('class','').split(): self.eyebrow=[self.owner(),[]]
        if tag in ('h2','h3','h4','h5') and a.get('id'):
            self.capture={'id':a['id'],'level':tag,'owner':self.owner(),'parts':[]}
        if self.capture and tag=='a' and 'heading-anchor' in a.get('class','').split(): self.skip_anchor+=1

    def handle_data(self,data):
        if self.eyebrow: self.eyebrow[1].append(data)
        if self.capture and not self.skip_anchor: self.capture['parts'].append(data)

    def handle_endtag(self,tag):
        if tag=='a' and self.skip_anchor: self.skip_anchor-=1
        if tag=='p' and self.eyebrow:
            self.labels[self.eyebrow[0]]=re.sub(r'\s+',' ',''.join(self.eyebrow[1])).strip(); self.eyebrow=None
        if self.capture and tag==self.capture['level']:
            c=self.capture
            self.items.append({'id':c['id'],'title':re.sub(r'\s+',' ',''.join(c['parts'])).strip(),
                'location':self.labels.get(c['owner'],'Book reference'),'owner':c['owner']})
            self.capture=None
        if tag=='section' and self.sections: self.sections.pop()


def source_headings(book):
    # Generated evidence and the search data must never become duplicate lookup hits.
    source=re.sub(r'<!-- BEGIN PRODUCT CLAIMS.*?<!-- END PRODUCT CLAIMS[^>]*-->', '', book, flags=re.S)
    source=GENERATED.sub('',source)
    return Headings(source).items


def validate(mapping,book):
    if mapping.get('schema_version')!=1: raise ValueError('Unsupported glossary mapping version')
    entries=definitions(book); terms=mapping['terms']
    labels=[e[0] for e in entries]
    if Counter(labels)!=Counter(t['label'] for t in terms) or any(v!=1 for v in Counter(labels).values()):
        raise ValueError('Glossary labels and mapping must match one-to-one; additions/renames need a mapping')
    ids=[t['id'] for t in terms]
    if len(ids)!=len(set(ids)) or any(not re.fullmatch('[a-z][a-z0-9-]*',i) for i in ids):
        raise ValueError('Invalid/duplicate term ID')
    headings={h['id']:h for h in source_headings(book)}
    counts=Counter(re.findall(r'\bid="([^"]+)"',book))
    if any(count>1 for count in counts.values()): raise ValueError('Duplicate document IDs')
    aliases=defaultdict(set)
    for t in terms:
        if not t['targets'] or len(set(t['targets']))!=len(t['targets']): raise ValueError(f'{t["id"]}: missing/duplicate destinations')
        for dest in t['targets']:
            if dest not in headings or counts[dest]!=1: raise ValueError(f'{t["id"]}: invalid explanation heading {dest}')
        for related in t.get('related',[]):
            if related not in ids or related==t['id']: raise ValueError('Invalid related term')
        for alias in [t['label']]+t['aliases']:
            key=normalise(alias)
            if not key: raise ValueError('Empty alias')
            aliases[key].add(t['id'])
    actual={k:sorted(v) for k,v in aliases.items() if len(v)>1}
    expected={normalise(k):sorted(v) for k,v in mapping['shared_aliases'].items()}
    if actual!=expected: raise ValueError(f'Unreviewed ambiguous aliases: {actual}; declared: {expected}')
    return entries,headings


def build(mapping,book):
    entries,headings=validate(mapping,book)
    terms={t['label']:t for t in mapping['terms']}; by_id={t['id']:t for t in mapping['terms']}
    glossary=BLOCK.search(book)[0]
    def replace(match):
        label=plain(match[1]); spec=terms[label]
        body=next(e[2] for e in entries if e[0]==label)
        links=''.join(f'<li><a href="#{escape(dest)}">{escape(headings[dest]["location"])}: {escape(headings[dest]["title"])}</a></li>' for dest in spec['targets'])
        related=''
        if spec.get('related'):
            related='<p>Related: '+', '.join(f'<a href="#term-{i}">{escape(by_id[i]["label"])}</a>' for i in spec['related'])+'.</p>'
        nav=(f'<!-- BEGIN GLOSSARY NAV -->\n<nav class="glossary-entry-nav" aria-label="Navigation for {escape(label,quote=True)}">'
             f'<p>Read the explanation:</p><ul>{links}</ul>{related}'
             f'<a class="term-permalink" href="#term-{spec["id"]}">Link to this term<span class="hub-sr-only">: {escape(label)}</span></a>'
             '</nav>\n<!-- END GLOSSARY NAV -->')
        return (f'<dt id="term-{spec["id"]}" tabindex="-1">{match[1]}</dt>'
                f'<dd><span class="glossary-definition" id="definition-{spec["id"]}">{body}</span>{nav}</dd>')
    glossary=PAIRS.sub(replace,glossary)
    glossary=re.sub(r'<details\b[^>]*>', '<details class="glossary" id="glossary" open>',glossary,count=1)
    book=BLOCK.sub(lambda _:glossary,book,count=1)
    index=[]
    for label,_,body in entries:
        t=terms[label]; dest=headings[t['targets'][0]]
        index.append({'id':'term-'+t['id'],'kind':'Term','title':label,'aliases':t['aliases'],
          'text':plain(body),'location':'Glossary · '+dest['location']})
    for h in headings.values():
        index.append({'id':h['id'],'kind':'Section','title':h['title'],'aliases':[],
          'text':h['title'],'location':h['location']})
    payload=json.dumps(index,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    lookup=f'''<!-- BEGIN GLOSSARY LOOKUP -->
<div class="book-lookup" id="book-lookup" hidden>
<form role="search" aria-label="Book lookup">
<label for="book-lookup-input">Find a term or section</label>
<p id="book-lookup-help">Search glossary definitions, aliases and section titles. This is not full-text search; everything runs on this page.</p>
<div class="lookup-controls"><input id="book-lookup-input" type="search" autocomplete="off" spellcheck="false" aria-describedby="book-lookup-help"><button type="button" id="book-lookup-clear">Clear</button></div>
</form>
<p id="book-lookup-status" role="status" aria-live="polite" aria-atomic="true">Type a term, acronym or section title.</p>
<ol id="book-lookup-results" aria-label="Lookup results"></ol>
<button type="button" id="book-lookup-more" hidden>Show more results</button>
</div>
<noscript><p>Local lookup needs JavaScript. The glossary and explanation links below still work. Use your browser’s Find command to search this page.</p></noscript>
<script type="application/json" id="book-lookup-index">{payload}</script>
<!-- END GLOSSARY LOOKUP -->
'''
    old=re.search(r'<!-- BEGIN GLOSSARY LOOKUP -->.*?<!-- END GLOSSARY LOOKUP -->\n?',book,re.S)
    if old: book=book[:old.start()]+lookup+book[old.end():]
    else: book=book.replace('<details class="glossary" id="glossary" open>',lookup+'<details class="glossary" id="glossary" open>',1)
    return book


def load():
    return json.loads(MAP.read_text(encoding='utf-8')), BOOK.read_text(encoding='utf-8')
