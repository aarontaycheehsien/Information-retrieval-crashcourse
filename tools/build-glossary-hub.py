"""Build glossary navigation/lookup; --check detects drift without writing."""
import argparse
from glossary_hub import load,build,BOOK

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); mapping,book=load(); result=build(mapping,book)
    if result!=book:
        if args.check: raise SystemExit('Glossary navigation/index is stale; rebuild it.')
        BOOK.write_text(result,encoding='utf-8'); print('Updated glossary navigation and embedded lookup.')
    else: print('PASS: glossary navigation and lookup are up to date.')

if __name__=='__main__':main()
