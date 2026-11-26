---
key: "appendix-character-and-byte-tokenisation"
kind: "appendix"
eyebrow: "Appendix B"
meta: "About 3 min · optional"
section_id: "app-B"
---

## How neural models receive text {#appendix-character-and-byte-tokenisation}

This optional appendix expands the short account of subword tokenisation given in [Chapter 6](#model-tokens-are-not-indexed-terms).
It follows one named tokeniser through every stage, then explains two input levels that are useful to recognise but are not central to the book’s comparison of lexical and dense retrieval.

### Worked example: BERT’s WordPiece tokeniser {#appendix-wordpiece-worked-example}

The stages are easier to see with one named tokeniser.
The example below follows the uncased [BERT base tokeniser](https://huggingface.co/google-bert/bert-base-uncased).
Its vocabulary was learnt before the query arrived; at search time, the tokeniser applies its fixed rules and selects pieces already in that vocabulary.

The *stages* are the point here.
The pieces and IDs below follow the published [google-bert/bert-base-uncased vocabulary](https://huggingface.co/google-bert/bert-base-uncased/raw/main/vocab.txt).
Two of the words are complete vocabulary entries and pass through whole; the invented one does not exist in a vocabulary learnt years before anyone wrote it, so the tokeniser has to build it from pieces.[^tokeniser-check]

:::: {.figure key="wordpiece-pipeline"}
From text to BERT model input

::: {.include src="figures/wordpiece-pipeline.html"}
:::

::: caption
The `##` marker means that a piece continues the preceding one inside the same original word.
It is a tokeniser convention, not text typed by the user.
Note what the split is *not*: this vocabulary contains no `rizz` piece at all, so the tokeniser cannot recover the parts a reader sees.
It produces `ri` · `##zz` · `##lord`, which is representable without being meaningful.
Exact stages, pieces, indices and special tokens differ across model families and releases, so another tokeniser will divide the same string differently.
:::
::::

The two square-bracketed items in the final stage are **special tokens** rather than words from the text.
BERT-style models mark the start of a sequence and the boundary between segments, and the representation computed at the opening position is one of the things a retrieval model may later pool into a single vector for the whole text.

### Character and byte inputs {#appendix-character-and-byte-inputs}

| Input level | Possible treatment of `rizzlord` | Main trade-off |
|---|---|---|
| Character-level | `r` · `i` · `z` · `z` · `l` · `o` · `r` · `d` | Can represent unfamiliar strings when the characters are supported or a fallback exists, but produces longer sequences whose individual units carry less information. |
| Byte-level | The sequence of byte values used to encode the string | A fixed inventory can represent arbitrary digital text, but the sequence may be longer and further removed from recognisable words. |

: Character and byte tokenisation compared on an unfamiliar string.

A **character** is a written symbol such as `r`, although the exact boundary is less simple for combining marks and some emoji.
Character-level models process text in units at roughly this scale rather than first assembling a conventional word or subword vocabulary.
Their coverage still depends on which characters the model supports or whether it provides a fallback for unfamiliar ones.

A **byte** is a numerical unit with 256 possible values.
Text encodings such as UTF-8 represent each character using one or more bytes.
Many basic Latin letters use one byte, while many other scripts and emoji require several.
A byte-level model can therefore accept any valid UTF-8 string without needing an unknown token at the byte level.

The price is usually sequence length.
A short familiar word that occupies one subword token may require several characters or several bytes, so the encoder must process more input positions.

Pure byte-level models are also different from **byte-level subword tokenisers**.
A model such as [ByT5](https://aclanthology.org/2022.tacl-1.17/) processes bytes directly.
GPT-2-style byte-level BPE begins with byte-representable symbols but merges frequent sequences into larger tokens.
Both avoid a hard inability to represent arbitrary input, but only the first remains byte-level throughout tokenisation.

A pure character-level model is likewise not the same as a subword tokeniser that occasionally falls back to individual characters.
The relevant lesson for retrieval is modest: finer input units make unfamiliar strings encodable, but they do not guarantee that the resulting query or passage embedding captures the string’s intended meaning.

[^tokeniser-check]: Tokeniser output is easy to check and easy to get wrong.
    Online tokeniser playgrounds sometimes label a model correctly while running a different tokeniser underneath, so tokens carrying a leading-space convention from another tokeniser, or vocabulary indices beyond the model’s vocabulary size (28,996 for BERT base cased and 30,522 for BERT base uncased) are reasons to verify the implementation.
    Absence of `##` alone proves nothing: whole vocabulary words need no continuation markers.
    The authoritative check is to run the tokeniser itself:

    ```
    from transformers import AutoTokenizer
    t = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
    t.tokenize("Unbelievable rizzlord scenes!")
    t("Unbelievable rizzlord scenes!")["input_ids"]
    ```

    The second call returns the vocabulary indices with the `[CLS]` and `[SEP]` boundary tokens already added.
