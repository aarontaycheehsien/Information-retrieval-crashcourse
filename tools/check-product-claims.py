"""Read-only currency report. Age warnings do not fail; invalid data does."""
import argparse
from datetime import date
from product_claims import load, currency, STATES, status_text

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    args=parser.parse_args()
    data,_,_=load()
    print(f'Currency as of {args.as_of}; not an external source verification.')
    for category in STATES:
        rows=[c for c in data['claims'] if category in currency(c,args.as_of)['flags']]
        print(f'\n{category.upper()}: {len(rows)}')
        for c in rows:
            state=currency(c,args.as_of)
            print(f'  {c["id"]}: support={state["last_support"] or "unknown"}; attempt={state["last_attempt"] or "unknown"}; {status_text(state)}')
    print('\nHistorical and unresolved categories may overlap. Warnings do not refresh dates or modify files.')

if __name__=='__main__':
    main()
