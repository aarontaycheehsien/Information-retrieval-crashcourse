"""Generate the printable questionnaire from anchored textbook questions.

Standard library only. --check reports drift without writing anything.
"""
import argparse
from html import escape, unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "search-textbook.html"
MAPPING = ROOT / "tools/fixtures/vendor-questionnaire.json"
TEMPLATE = ROOT / "tools/templates/vendor-questionnaire.html"
OUTPUT = ROOT / "vendor-questionnaire.html"


def element(book, tag, anchor):
    matches = re.findall(rf'<{tag}\b[^>]*\bid="{re.escape(anchor)}"[^>]*>(.*?)</{tag}>', book, re.S)
    if len(matches) != 1:
        raise ValueError(f"Expected one <{tag}> with id={anchor}; found {len(matches)}")
    return matches[0].strip()


def prose(fragment):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def source_content(book, spec, tag="li"):
    fragment = element(book, tag, spec["source_id"])
    # The source list wraps core items in one paragraph; appendix items are inline.
    if fragment.startswith("<p>") and fragment.endswith("</p>"):
        fragment = fragment[3:-4].strip()
    marker = spec.get("omit_after")
    if marker:
        if fragment.count(marker) != 1:
            raise ValueError(f"Narrative boundary changed for {spec['source_id']}; review the mapping")
        fragment = fragment.split(marker)[0].rstrip()
    return re.sub(r'href="#', 'href="search-textbook.html#', fragment)


def writing_field(label, lines=1, extra_class=""):
    rules = ''.join('<span class="writing-line" aria-hidden="true"></span>' for _ in range(lines))
    return f'<div class="response-field {extra_class}"><p class="field-label">{label}</p>{rules}</div>'


def split_title(source):
    match = re.match(r"<strong>(.*?)</strong>\s*(.*)", source, re.S)
    title, body = (match[1], match[2]) if match else (source, "")
    # Appendix E titles end in a colon that introduces the body; the heading does not need it.
    return title.rstrip().removesuffix(":"), body


def detail(ident, body):
    """Letter a body made only of questions, so answers can cite Q13b; words are unchanged."""
    if not body:
        return ''
    parts = [p for p in re.split(r'(?<=\?)\s+(?=[A-Z])', body.strip()) if p]
    if len(parts) < 2 or not all(p.endswith('?') for p in parts):
        return f'<p class="question-detail">{body}</p>'
    items = ''.join(f'<li id="{ident.lower()}{chr(97 + i)}">{p}</li>' for i, p in enumerate(parts))
    return f'<ol class="question-detail sub-prompts" type="a">{items}</ol>'


def card(book, spec, section):
    ident = spec["id"]
    source = source_content(book, spec)
    title, body = split_title(source)
    related = spec.get("related", [])
    reference = ""
    if related:
        links = ', '.join(f'<a href="#{q.lower()}">{q}</a>' for q in related)
        reference = f'<p class="related">Already covered? Cite {links} and answer any remaining parts here.</p>'
    local_evaluation = ''
    if ident in ("Q17", "Q19"):
        local_evaluation = '<p class="related">Local comparison: <a href="evaluation-kit.html">evaluation kit</a>.</p>'
    return f'''<article class="question" data-question="{ident}" aria-labelledby="{ident.lower()}">
  <h3 id="{ident.lower()}"><span class="question-id">{ident}</span> {title}</h3>
  {detail(ident, body)}
  <p class="listen-for"><strong>Listen for</strong> {escape(spec['listen_for'])}</p>
  <p class="source"><a href="search-textbook.html#{spec['source_id']}">{section['source_label']} source · {ident}</a></p>
  {reference}{local_evaluation}
  <div class="response-block">
  <div class="response-status"><span class="field-label">Vendor response:</span> <span><i class="tick"></i> Answered</span> <span><i class="tick"></i> Partly answered</span> <span><i class="tick"></i> Unanswered</span> <span><i class="tick"></i> Not applicable</span></div>
  {writing_field('Vendor answer / existing answer reference', 2)}
  {writing_field('Vendor supporting evidence: document, URL or demonstration reference', 2)}
  {writing_field('Library verification: what was checked, observed or remains unverified', 2)}
  <div class="field-pair">{writing_field('Date checked (YYYY-MM-DD)')}{writing_field('Reason if not applicable')}</div>
  {writing_field('Unresolved follow-up / action-log reference')}
  </div>
</article>'''


def render(book, mapping, template):
    questions = {item["id"]: item for item in mapping["questions"]}
    if len(questions) != len(mapping["questions"]):
        raise ValueError("Duplicate question IDs in mapping")
    assigned = [q for section in mapping["sections"] for group in section["groups"] for q in group["questions"]]
    if len(assigned) != len(set(assigned)) or set(assigned) != set(questions):
        raise ValueError("Each mapped question must belong to exactly one group")
    anchors = re.findall(r'<li\b[^>]*\bid="(vendor-[qeg]\d+)"', book)
    if sorted(anchors) != sorted(q["source_id"] for q in questions.values()):
        raise ValueError("Source question anchors and mapping differ")
    # Also catch a new unanchored source question, not only renamed mapped IDs.
    for section in mapping["sections"]:
        start = book.index(f'id="{section["source_section"]}"')
        end = re.search(r'<aside class="chapter-close"|<nav class="chapter-nav"', book[start:])
        if not end:
            raise ValueError(f"Cannot find end of {section['source_section']}")
        count = len(re.findall(r'<li\b', book[start:start + end.start()]))
        mapped_count = sum(len(group["questions"]) for group in section["groups"])
        if count != mapped_count:
            raise ValueError(f"{section['source_section']}: {count} source questions but {mapped_count} mapped")
    fragments, overview = [], []
    for section in mapping["sections"]:
        entries = ''.join(f'<li><a href="#{q.lower()}">{q}</a> {split_title(source_content(book, questions[q]))[0]}</li>'
                          for group in section["groups"] for q in group["questions"])
        overview.append(f'<h3>{escape(section["label"])}</h3><ul class="question-list">{entries}</ul>')
    for section in mapping["sections"]:
        key = section["key"]
        pages = []
        number = 0
        for group in section["groups"]:
            heading = prose(element(book, "h5", group["heading_id"])) if "heading_id" in group else group["heading"]
            for offset in range(0, len(group["questions"]), 2):
                number += 1
                chunk = group["questions"][offset:offset + 2]
                continuation = ' <span class="continued">(continued)</span>' if offset else ''
                applicability = f'<p class="section-note">{escape(section["applicability"])}</p>' if number == 1 and "applicability" in section else ''
                contents = '\n'.join(card(book, questions[q], section) for q in chunk)
                pages.append(f'''<section class="question-page" data-section="{key}" aria-labelledby="{key}-page-{number}">
  <p class="page-context">Vendor questionnaire · {escape(section['source_label'])}</p>
  <h2 id="{key}-page-{number}">{escape(heading)}{continuation}</h2>
  {applicability}
  {contents}
</section>''')
        hidden = ' hidden' if key != "core" else ''
        fragments.append(f'<div id="section-{key}"{hidden}>\n' + '\n'.join(pages) + '\n</div>')
    intake = source_content(book, mapping["intake"], "p")
    fields = ''.join(writing_field(label) for label in ["Institution", "Library reviewer", "Vendor contact", "Review date (YYYY-MM-DD)", "Product", "Specific mode", "Version / unknown", "Intended library use"])
    followups = ''.join(f'<tr><th scope="row">{i}</th><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6))
    replacements = {"VERSION": escape(mapping["version"]), "INTAKE_FIELDS": fields, "INPUT_QUESTION": intake,
                    "QUESTION_PAGES": '\n'.join(fragments), "FOLLOWUP_ROWS": followups,
                    "QUESTION_LIST": '\n'.join(overview)}
    for key, value in replacements.items():
        placeholder = '{{' + key + '}}'
        if placeholder not in template:
            raise ValueError(f"Missing template slot {key}")
        template = template.replace(placeholder, value)
    if re.search(r'\{\{[A-Z_]+\}\}', template):
        raise ValueError("Unresolved template slot")
    return template


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated output without writing")
    args = parser.parse_args()
    generated = render(BOOK.read_text(encoding="utf-8"), json.loads(MAPPING.read_text(encoding="utf-8")), TEMPLATE.read_text(encoding="utf-8"))
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if args.check:
        if current != generated:
            raise SystemExit("Questionnaire is stale; run python tools/build-vendor-questionnaire.py")
        print("PASS: questionnaire matches its source questions, mapping and template.")
    elif current != generated:
        OUTPUT.write_text(generated, encoding="utf-8", newline="\n")
        print("Generated vendor-questionnaire.html (19 core, 4 ranking, 7 RAG questions).")
    else:
        print("Questionnaire already up to date.")


if __name__ == "__main__":
    main()
