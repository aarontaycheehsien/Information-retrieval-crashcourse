"""Product evidence registry: validation, date semantics and deterministic HTML.

No network access and no assertion that a working URL verifies a claim.
"""
from collections import defaultdict, Counter
from datetime import date, timedelta
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit
import calendar
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data/product-claims.json'
BOOK = ROOT / 'search-textbook.html'
NOTES = ROOT / 'teaching-notes.html'
FINDINGS = {'supported': 'Supported within stated scope', 'changed': 'Changed', 'not established': 'Not established'}
BASES = {'documentation', 'observation', 'screenshot', 'inference'}
STATES = ('overdue', 'unknown', 'unresolved', 'historical', 'within-window')


def plain(s):
    s = re.sub(r'<sup\b.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<a[^>]*class="footnote-backref".*?</a>', '', s, flags=re.S)
    return re.sub(r'\s+', ' ', unescape(re.sub('<[^>]+>', ' ', s))).strip()


def date_bounds(value):
    """Inclusive possible dates; never replace unknown with the migration date."""
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?', value):
        raise ValueError(f'Invalid date: {value!r}')
    parts = list(map(int, value.split('-')))
    year = parts[0]
    if len(parts) == 1:
        return date(year, 1, 1), date(year, 12, 31)
    month = parts[1]
    if len(parts) == 2:
        return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])
    day = date(*parts)
    return day, day


def eligible_reviews(claim, as_of):
    # A month-only date is usable within that month, with explicitly approximate age.
    return [r for r in claim['reviews'] if r['checked_on'] is None or date_bounds(r['checked_on'])[0] <= as_of]


def last_support(claim, as_of):
    values = [r['checked_on'] for r in eligible_reviews(claim, as_of)
              if r['finding'] == 'supported' and r['checked_on']]
    return max(values, key=lambda v: date_bounds(v)[0]) if values else None


def currency(claim, as_of):
    reviews = eligible_reviews(claim, as_of)
    latest = reviews[-1] if reviews else None
    support = last_support(claim, as_of)
    flags = []
    if (latest and latest['finding'] != 'supported') or not claim['evidence'] or claim.get('evidence_gap'):
        flags.append('unresolved')
    if claim['temporal_scope'] == 'historical':
        flags.append('historical')
    elif not support:
        flags.append('unknown')
    elif (as_of - date_bounds(support)[0]).days > 365:
        flags.append('overdue')
    else:
        flags.append('within-window')
    return {'flags': flags, 'last_support': support,
            'last_attempt': latest['checked_on'] if latest else None,
            'finding': FINDINGS[latest['finding']] if latest else 'No recorded verification finding',
            'approximate': bool(support and len(support) < 10)}


def strip_generated(book):
    return re.sub(r'<!-- BEGIN PRODUCT CLAIMS.*?<!-- END PRODUCT CLAIMS[^>]*-->', '', book, flags=re.S)


def validate(data, book, root=ROOT):
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported schema_version')
    for key in ('inventory_note', 'currency_as_of', 'claims', 'teaching_groups', 'coverage'):
        if not data.get(key):
            raise ValueError(f'Missing {key}')
    date.fromisoformat(data['currency_as_of'])
    source = strip_generated(book)
    ids = Counter(re.findall(r'\bid="([^"]+)"', source))
    clean = plain(source)
    groups = [g['id'] for g in data['teaching_groups']]
    if len(groups) != 9 or len(set(groups)) != 9:
        raise ValueError('Expected nine distinct teaching groups')
    seen = set()
    for c in data['claims']:
        ident = c['id']
        if not re.fullmatch('[a-z][a-z0-9-]+', ident) or ident in seen:
            raise ValueError(f'Invalid/duplicate claim ID: {ident}')
        seen.add(ident)
        for field in ('product', 'mode', 'claim', 'limitations', 'review_trigger', 'locations'):
            if not c.get(field):
                raise ValueError(f'{ident}: missing {field}')
        if c['temporal_scope'] not in ('historical', 'current-facing') or c['evidence_basis'] not in BASES:
            raise ValueError(f'{ident}: invalid scope/basis')
        date_bounds(c['evidence_date'])
        if not c['evidence'] and not c.get('evidence_gap'):
            raise ValueError(f'{ident}: missing evidence or explicit gap')
        for e in c['evidence']:
            if not e.get('title') or not e.get('locator'):
                raise ValueError(f'{ident}: missing evidence title/locator')
            u = urlsplit(e['url'])
            if u.scheme:
                if u.scheme not in ('https', 'http') or not u.netloc:
                    raise ValueError(f'{ident}: unsafe evidence URL')
            else:
                p = (root / u.path).resolve()
                if not p.is_relative_to(root.resolve()) or not p.is_file():
                    raise ValueError(f'{ident}: missing/unsafe local evidence')
        previous = date.min
        for review in c['reviews']:
            bounds = date_bounds(review['checked_on'])
            if bounds:
                if bounds[0] < previous:
                    raise ValueError(f'{ident}: review history must be chronological')
                previous = bounds[0]
            if review['finding'] not in FINDINGS or not review.get('notes'):
                raise ValueError(f'{ident}: invalid finding or missing review notes')
            indices = review['evidence_indices']
            if any(type(i) is not int or i < 0 or i >= len(c['evidence']) for i in indices):
                raise ValueError(f'{ident}: invalid review evidence reference')
            if review['finding'] == 'supported' and not indices:
                raise ValueError(f'{ident}: support requires evidence')
        for loc in c['locations']:
            if ids[loc['anchor']] != 1:
                raise ValueError(f'{ident}: missing/duplicate book anchor {loc["anchor"]}')
            if not loc['excerpt'] or loc['excerpt'] not in clean:
                raise ValueError(f'{ident}: source wording drift at {loc["anchor"]}; review the claim and its locations')
        if not set(c['teaching_groups']) <= set(groups):
            raise ValueError(f'{ident}: unknown teaching group')
    covered = set()
    coverage_anchors = set()
    for section in data['coverage']:
        if ids[section['anchor']] != 1 or section['anchor'] in coverage_anchors:
            raise ValueError(f'Invalid coverage anchor: {section["anchor"]}')
        coverage_anchors.add(section['anchor'])
        if not section['exclusions'] or not set(section['claim_ids']) <= seen:
            raise ValueError('Invalid coverage record')
        covered.update(section['claim_ids'])
    if seen - covered:
        raise ValueError(f'Claims missing from coverage: {seen - covered}')
    # New main chapters/appendices must be considered even when no claim is included.
    headings = set(re.findall(r'<h2\b[^>]*id="([^"]+)"', source))
    headings = {a for a in headings if not a.startswith('part') and a != 'backmatter-divider'}
    if headings - coverage_anchors:
        raise ValueError(f'New sections require a coverage decision: {headings - coverage_anchors}')


def load():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    book = BOOK.read_text(encoding='utf-8')
    validate(data, book)
    return data, book, NOTES.read_text(encoding='utf-8')


def date_label(value):
    return escape(value) if value else 'Unknown / not recorded'


def location_label(anchor):
    match = re.fullmatch(r'(tbl|fig)-([a-z0-9]+)-(\d+)', anchor)
    if match:
        return ('Table' if match[1] == 'tbl' else 'Figure')+' '+match[2].upper()+'.'+match[3]
    return anchor.replace('fn:', 'Footnote: ').replace('-', ' ').capitalize()


def status_text(state):
    labels = {'overdue': 'Review overdue (>365 days)', 'unknown': 'Supporting check date unknown',
              'historical': 'Historical example', 'unresolved': 'Changed / unresolved',
              'within-window': 'Supporting check within 365 days (not a current-product guarantee)'}
    return '; '.join(labels[f] for f in state['flags']) + (' · approximate age' if state['approximate'] else '')


def book_html(data):
    as_of = date.fromisoformat(data['currency_as_of'])
    counts = Counter(f for c in data['claims'] for f in currency(c, as_of)['flags'])
    out = ['<section class="chapter backsection product-claims-register" aria-labelledby="product-evidence-currency">',
      '<h2 id="product-evidence-currency">Product evidence and currency</h2>',
      '<p>Named products are dated illustrations, not recommendations. This register separates evidence dates from verification dates and observations from documentation or inference. Reopening an old document does not establish current behaviour.</p>',
      f'<p>{escape(data["inventory_note"])}</p>',
      f'<p><strong>Currency snapshot: {data["currency_as_of"]}.</strong> {len(data["claims"])} claims: {counts["overdue"]} overdue; {counts["unknown"]} with unknown supporting check dates; {counts["unresolved"]} changed/unresolved; {counts["historical"]} historical. Categories can overlap. Run the maintenance report for a later date; this static page does not update itself.</p>',
      '<p>Age uses the last supporting check, never an unsuccessful attempt. For month/year-only dates, age is conservatively measured from the first possible day and labelled approximate. Historical examples are not overdue solely because they are old. “Supported” always means within the recorded scope.</p>',
      '<p><a href="data/product-claims.json" download>Download the machine-readable register (JSON)</a> · <a href="teaching-notes.html#currency">Nine teaching verification groups</a> · <a href="https://github.com/aarontaycheehsien/Information-retrieval-crashcourse/issues">Report an error (include the claim ID)</a></p>']
    by_product = defaultdict(list)
    for c in data['claims']:
        by_product[c['product']].append(c)
    def product_id(product):
        return 'claims-product-'+re.sub('[^a-z0-9]+','-',product.lower()).strip('-')
    out.append('<p>Jump to product: '+ ' · '.join(f'<a href="#{product_id(product)}">{escape(product)}</a>' for product in sorted(by_product,key=str.casefold))+'</p>')
    for product, claims in sorted(by_product.items(), key=lambda p: p[0].casefold()):
        # h4 keeps a large product index out of the main chapter TOC.
        out.append(f'<h4 id="{product_id(product)}">{escape(product)}</h4>')
        for c in sorted(claims, key=lambda c:(c['mode'], c['id'])):
            st = currency(c, as_of)
            locations = list(dict.fromkeys(l['anchor'] for l in c['locations']))
            links = ' · '.join(f'<a href="#{escape(a)}">{escape(location_label(a))}</a>' for a in locations)
            out.extend([f'<article class="claim-entry" id="claim-{c["id"]}">',
              f'<p class="claim-id">{c["id"]} · {escape(c["mode"])}</p>',
              f'<p><strong>{escape(c["claim"])}</strong></p>',
              f'<p class="claim-status">{escape(status_text(st))}</p>',
              f'<p>Evidence date: {date_label(c["evidence_date"])} · Last supporting check: {date_label(st["last_support"])}</p>',
              '<details><summary>Evidence, review history and book locations</summary>',
              f'<p>Basis: {escape(c["evidence_basis"])}. Finding: {escape(st["finding"])}. Last attempt: {date_label(st["last_attempt"])}.</p>',
              f'<p>{escape(c["limitations"])}</p>'])
            if c.get('evidence_gap'):
                out.append(f'<p><strong>Evidence gap:</strong> {escape(c["evidence_gap"])}</p>')
            out.append('<ul>')
            for e in c['evidence']:
                out.append(f'<li><a href="{escape(e["url"], quote=True)}">{escape(e["title"])}</a> — {escape(e["locator"])}</li>')
            out.append('</ul>')
            for r in c['reviews']:
                out.append(f'<p>Review {date_label(r["checked_on"])}: {FINDINGS[r["finding"]]}. {escape(r["notes"])}</p>')
            out.extend([f'<p>Review trigger: {escape(c["review_trigger"])}</p>', f'<p>Book locations: {links}</p>', '</details></article>'])
    out.extend(['<details class="claim-coverage"><summary>Inventory coverage and exclusions</summary>', '<p>This is an editorial inventory, not an automatic proof of semantic completeness. Source edits must include a claim and coverage review.</p>', '<ul>'])
    for s in data['coverage']:
        out.append(f'<li><a href="#{escape(s["anchor"])}">{escape(s["title"])}</a>: {len(s["claim_ids"])} mapped claims. {escape(s["exclusions"])}</li>')
    out.extend(['</ul></details>', '</section>'])
    return '\n'.join(out)


def notes_html(data):
    as_of = date.fromisoformat(data['currency_as_of'])
    out = ['<div class="claim-teaching-groups">',
      '<p>Choose from nine verification groups below. Each group contains independently checkable claims, rather than one assertion about an entire product. Assign a group or selected claim IDs. In a copy, record the product mode, source and relevant passage, evidence date, date checked, finding (supported within scope, changed or not established), and limitations. Pass the record to the next instructor.</p>',
      f'<p>These views share the <a href="search-textbook.html#product-evidence-currency">book’s evidence register</a>. Currency snapshot: {data["currency_as_of"]}. Rechecking a historical source does not make the architecture current. Unknown dates are not fresh checks.</p>']
    for g in data['teaching_groups']:
        out.extend([f'<details id="claims-group-{g["id"]}"><summary>{escape(g["title"])}</summary>',f'<p>{escape(g["question"])}</p>', '<ul>'])
        for c in data['claims']:
            if g['id'] not in c['teaching_groups']:
                continue
            st=currency(c,as_of)
            out.append(f'<li><a href="search-textbook.html#claim-{c["id"]}">{c["id"]}</a> — {escape(c["claim"])}<br>Evidence: {date_label(c["evidence_date"])}; supporting check: {date_label(st["last_support"])}; finding: {escape(st["finding"])}. {escape(status_text(st))}.</li>')
        out.append('</ul></details>')
    out.extend(['<p>The full register also covers claims outside these nine groups, including API controls, commercial changes and screening software.</p>', '</div>'])
    return '\n'.join(out)


def backlinks(book, data):
    """Mechanical insertion beside existing anchors, never inside authored prose."""
    book = re.sub(r'<!-- BEGIN PRODUCT CLAIMS LINKS [^>]+ -->.*?<!-- END PRODUCT CLAIMS LINKS [^>]+ -->\n?', '', book, flags=re.S)
    by_anchor = defaultdict(dict)
    for c in data['claims']:
        for loc in c['locations']:
            anchor = loc['anchor']
            # Questionnaire question bodies are consumed by a separate generator.
            if anchor.startswith('vendor-'):
                anchor = 'choosing-and-governing-search-tools'
            by_anchor[anchor][c['id']] = c
    for anchor, claims in sorted(by_anchor.items()):
        match = re.search(r'<(h[2-5]|p|figcaption|li)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>', book)
        if not match:
            raise ValueError(f'Cannot place register links at {anchor}')
        pos = match.end() if match[1] == 'li' else book.index('</'+match[1]+'>',match.end())+len(match[1])+3
        links = ''.join(f'<p><a href="#claim-{c["id"]}">{escape(c["claim"])}</a></p>' for c in claims.values())
        block = (f'<!-- BEGIN PRODUCT CLAIMS LINKS {anchor} -->\n'
                 f'<details class="claim-links"><summary>Evidence register · {len(claims)} claim(s)</summary>{links}</details>\n'
                 f'<!-- END PRODUCT CLAIMS LINKS {anchor} -->\n')
        book = book[:pos]+block+book[pos:]
    return book


def replace_block(document, name, body):
    start, end = f'<!-- BEGIN PRODUCT CLAIMS {name} -->', f'<!-- END PRODUCT CLAIMS {name} -->'
    if document.count(start) != 1 or document.count(end) != 1:
        raise ValueError(f'Expected one generated block: {name}')
    before, rest = document.split(start)
    _, after = rest.split(end)
    return before + start + '\n' + body + '\n' + end + after
