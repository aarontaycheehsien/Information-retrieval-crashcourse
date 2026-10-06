"""Build static evidence views; --check is read-only. Standard library only."""
import argparse
from product_claims import load, book_html, notes_html, replace_block, backlinks, BOOK, NOTES

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args=parser.parse_args()
    data,book,notes=load()
    outputs={BOOK:backlinks(replace_block(book,'REGISTER',book_html(data)),data),
             NOTES:replace_block(notes,'TEACHING',notes_html(data))}
    drift=[]
    for path,content in outputs.items():
        if path.read_text(encoding='utf-8') != content:
            drift.append(path.name)
            if not args.check:
                path.write_text(content,encoding='utf-8')
    if args.check and drift:
        raise SystemExit('Generated-content drift: '+', '.join(drift))
    print(('Updated '+', '.join(drift)) if drift else 'PASS: product-claim views are up to date')

if __name__=='__main__':
    main()
