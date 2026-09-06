"""Derive Figure B.1's pieces and IDs from the BERT vocabulary, never from memory.

Appendix B tells the reader that its pieces and IDs "follow the published
google-bert/bert-base-uncased vocabulary". This script is what makes that
sentence checkable: it reproduces the tokeniser's own rules over the real
vocabulary file and prints both the stage-by-stage walkthrough and the HTML
for the figure.

Usage
-----
    python tools/wordpiece_example.py --vocab path/to/vocab.txt
    python tools/wordpiece_example.py --vocab path/to/vocab.txt --text "Unbelievable rizzlord scenes!"
    python tools/wordpiece_example.py --transformers        # if the library is installed

Get vocab.txt from
https://huggingface.co/google-bert/bert-base-uncased/raw/main/vocab.txt

The vocabulary is validated before use (see EXPECTED below), so a wrong or
truncated file is rejected rather than silently producing plausible numbers.

Exit status is non-zero if validation fails, so this can be wired into CI
alongside tools/test-labs.cjs to catch the figure drifting from the vocabulary.
"""

import argparse
import sys
import unicodedata

# Properties only the real bert-base-uncased vocabulary satisfies. Checking
# these matters more than trusting where the file came from.
EXPECTED_SIZE = 30522
EXPECTED_IDS = {
    "[PAD]": 0,
    "[UNK]": 100,
    "[CLS]": 101,
    "[SEP]": 102,
    "[MASK]": 103,
}
# The three ids Appendix B currently prints. Checked so that a change to the
# figure's example cannot quietly invalidate the surrounding prose.
FIGURE_CLAIMS = {"unbelievable": 23653, "scenes": 5019, "!": 999}

MAX_INPUT_CHARS_PER_WORD = 100


def load_vocab(path):
    with open(path, encoding="utf-8") as handle:
        tokens = [line.rstrip("\n") for line in handle]
    return {token: index for index, token in enumerate(tokens)}


def validate(vocab):
    """Reject a vocabulary that is not bert-base-uncased. Returns a report."""
    problems = []
    if len(vocab) != EXPECTED_SIZE:
        problems.append("size is %d, expected %d" % (len(vocab), EXPECTED_SIZE))
    for token, expected in EXPECTED_IDS.items():
        actual = vocab.get(token)
        if actual != expected:
            problems.append("%s is id %s, expected %d" % (token, actual, expected))
    return problems


def is_punctuation(char):
    """BERT treats ASCII non-alphanumerics as punctuation, plus Unicode P*."""
    code = ord(char)
    if (33 <= code <= 47) or (58 <= code <= 64) or (91 <= code <= 96) or (123 <= code <= 126):
        return True
    return unicodedata.category(char).startswith("P")


def basic_tokenize(text):
    """Lowercase, strip accents, split on whitespace and punctuation."""
    text = text.lower()
    text = "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    out = []
    for word in text.split():
        piece = ""
        for char in word:
            if is_punctuation(char):
                if piece:
                    out.append(piece)
                    piece = ""
                out.append(char)
            else:
                piece += char
        if piece:
            out.append(piece)
    return out


def wordpiece(token, vocab):
    """Greedy longest-match-first, as in the original BERT tokenization.py."""
    chars = list(token)
    if len(chars) > MAX_INPUT_CHARS_PER_WORD:
        return ["[UNK]"]
    pieces = []
    start = 0
    while start < len(chars):
        end = len(chars)
        found = None
        while start < end:
            candidate = "".join(chars[start:end])
            if start > 0:
                candidate = "##" + candidate
            if candidate in vocab:
                found = candidate
                break
            end -= 1
        if found is None:
            return ["[UNK]"]
        pieces.append(found)
        start = end
    return pieces


def run(text, vocab):
    lowered = text.lower()
    basic = basic_tokenize(text)
    pieces = []
    for token in basic:
        pieces.extend(wordpiece(token, vocab))
    ids = [vocab.get(piece, vocab["[UNK]"]) for piece in pieces]
    return {
        "raw": text,
        "lowered": lowered,
        "basic": basic,
        "pieces": pieces,
        "ids": ids,
        "bert_pieces": ["[CLS]"] + pieces + ["[SEP]"],
        "bert_ids": [vocab["[CLS]"]] + ids + [vocab["[SEP]"]],
    }


def dotted(items):
    return " · ".join("<code>%s</code>" % item for item in items)


def emit_html(result):
    """Print stages 1-6 as the figure's own markup, ready to paste."""
    lines = [
        '<div class="token-stage"><strong>1. Raw text</strong><p><code>%s</code></p></div>'
        % result["raw"],
        '<div class="token-arrow" aria-hidden="true">↓</div>',
        '<div class="token-stage"><strong>2. Normalisation</strong><p>The uncased '
        "tokeniser lowercases the text: <code>%s</code></p></div>" % result["lowered"],
        '<div class="token-arrow" aria-hidden="true">↓</div>',
        '<div class="token-stage"><strong>3. Basic tokenisation</strong><p>Whitespace '
        "and punctuation boundaries produce %s</p></div>" % dotted(result["basic"]),
        '<div class="token-arrow" aria-hidden="true">↓</div>',
        '<div class="token-stage"><strong>4. WordPiece segmentation</strong><p>%s</p></div>'
        % dotted(result["pieces"]),
        '<div class="token-arrow" aria-hidden="true">↓</div>',
        '<div class="token-stage"><strong>5. Vocabulary lookup</strong><p>%s</p></div>'
        % dotted(str(i) for i in result["ids"]),
        '<div class="token-arrow" aria-hidden="true">↓</div>',
        '<div class="token-stage"><strong>6. BERT-style input</strong><p>Special '
        "boundary tokens are added: <code>%s</code>, with IDs <code>%s</code></p></div>"
        % (" ".join(result["bert_pieces"]), " ".join(str(i) for i in result["bert_ids"])),
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocab", help="path to bert-base-uncased vocab.txt")
    parser.add_argument(
        "--transformers",
        action="store_true",
        help="load the vocabulary through an installed transformers instead",
    )
    parser.add_argument(
        "--text",
        default="Unbelievable rizzlord scenes!",
        help="the string to walk through the six stages",
    )
    args = parser.parse_args()

    if args.transformers:
        from transformers import AutoTokenizer  # noqa: PLC0415

        vocab = AutoTokenizer.from_pretrained("bert-base-uncased").get_vocab()
    elif args.vocab:
        vocab = load_vocab(args.vocab)
    else:
        parser.error("give --vocab path/to/vocab.txt or --transformers")

    problems = validate(vocab)
    if problems:
        print("This is not the bert-base-uncased vocabulary:", file=sys.stderr)
        for problem in problems:
            print("  - " + problem, file=sys.stderr)
        return 1

    print("Vocabulary validated: %d tokens, special ids as expected.\n" % len(vocab))

    print("Appendix B's current figure claims:")
    stale = False
    for token, expected in FIGURE_CLAIMS.items():
        actual = vocab.get(token)
        mark = "ok" if actual == expected else "MISMATCH"
        if actual != expected:
            stale = True
        print("  %-14s figure says %-6s vocabulary says %-6s %s"
              % (token, expected, actual, mark))
    print()

    result = run(args.text, vocab)
    print("Stages for %r:" % args.text)
    print("  2. lowercased      %s" % result["lowered"])
    print("  3. basic tokens    %s" % " · ".join(result["basic"]))
    print("  4. wordpieces      %s" % " · ".join(result["pieces"]))
    print("  5. ids             %s" % " ".join(str(i) for i in result["ids"]))
    print("  6. model input     %s" % " ".join(result["bert_pieces"]))
    print("     model input ids %s" % " ".join(str(i) for i in result["bert_ids"]))

    splits = [p for p in result["pieces"] if p.startswith("##")]
    print()
    if splits:
        print("Continuation pieces present (%s), so the ## caption earns its place."
              % ", ".join(splits))
    else:
        print("No continuation piece appears. This example does not exercise "
              "WordPiece splitting, which is the problem the figure has today.")

    print("\n--- figure markup ---\n")
    print(emit_html(result))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
