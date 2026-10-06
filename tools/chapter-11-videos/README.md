# Chapter 11: understanding, transforming and routing queries, animated

Three narrated films adapted from Aaron Tay's *How Search Decides What You See*.
The maintained source is `search-textbook.html#query-transformation`.

| Film | Duration | Focus |
|---|---|---|
| Eight doors to the same question | 3:47 | Eight overlapping query objects, receiver-specific phrasing, combining mechanisms and berrypicking |
| The hidden life of a query | 3:43 | Understanding, transformation, routing, coordination, feedback and representations |
| Imaginary text, real sources | 3:43 | Query2doc, HyDE, assumptions, product arrangements, partial filter extraction and audit trails |

The requested Kurzgesagt-inspired visual direction uses original geometric
artwork, a cosmic library, eight glowing portals, expressive index robots,
paper characters, moving signals, orbiting vocabulary and animated diagrams.
Skia draws every frame directly. The films use the project's original synthesized
music and Microsoft's locally installed synthetic `Hazel Desktop` narration.
Locally loaded Windows Segoe UI fonts are not distributed.

## Render

From the repository root, reuse the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-11-videos/render.py --check-only
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-11-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-11-videos/render.py
```

A separate Python 3.12 environment can install `requirements.txt`.
Speech synthesis runs locally through Windows System.Speech at the voice's
16 kHz clock, then the media engine resamples to 48 kHz. No narration leaves
the computer. The adapter validates returned word text and audio-clock positions.
Word timings control captions; recorded narration determines scene lengths.
Speech is never cropped or time-stretched. The installed Hazel Desktop voice
is required when generating new narration takes.

`--episode 1`, `2`, or `3` selects one film. Mutually exclusive modes are
`--check-only`, `--prepare-only`, `--stills-only`, `--render-only`, and
`--verify-only`. `--output` changes the delivery directory. Source and production
hashes reject stale prepared assets. Rendering uses bounded Windows pipe writes
and two encoder threads to reduce memory pressure.

## Watch and download

Outputs stay in `outputs/chapter-11-videos/`, excluded by its scoped `.gitignore`.
`preview.html` links to three 1920×1080, 30 fps H.264/AAC MP4s, captions,
transcripts and storyboards. Captions are burnt in and embedded, with SRT and
VTT sidecars. Each film also has a poster, eight scene stills, a contact sheet,
word-timed timeline, separate voice/music stems, mastered audio and verification.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-11-videos --port 8811
```

Open `http://127.0.0.1:8811/preview.html`. The server supports seeking with byte
ranges. For browser checks, set `CHAPTER11_NODE_MODULES` to the bundled Node
packages directory and run `node tools/chapter-11-videos/check-preview.cjs`.
The script uses installed Edge to play and seek all films, load captions,
check range requests and mobile widths, and capture the players.

After media checks, run `python tools/chapter-11-videos/package.py` in the same
environment. The delivery ZIP contains films, captions, transcripts, posters,
storyboards, production notes, reports and a local gallery. Packaging checks
production freshness, media hashes and archive CRCs.

## Accuracy, sources and adaptation choices

- The eight doors are overlapping distinctions, not mutually exclusive query
  types. A seed can start citation traversal; an API can carry text.
- Citation arrows run from citing paper to reference. Backward traversal follows
  those arrows; forward traversal reverses them. Similarity, bibliographic
  coupling and co-citation are different relations. The small graph is invented.
- PubMed Similar Articles uses weighted title, abstract and MeSH words, according
  to the [PubMed guide](https://pubmed.ncbi.nlm.nih.gov/help/#similar-articles).
  A seed-based interface does not establish a dense retriever.
- A/B/C in the year-filter example are invented records. Both A and B fit the
  2020–2024 scope; requiring the study itself to be open access excludes paywalled
  A even though it addresses the citation-advantage topic. The films do not answer
  whether an open-access citation advantage exists.
- The task brief addresses the controller. Lexical terms, dense descriptions,
  generated structured queries and detailed controller instructions are not
  interchangeable. Test phrasing against known useful records.
- Pseudo-relevance feedback assumes the top records are useful. Its second query
  depends on an earlier retrieval. A prescribed two-pass workflow need not be
  agentic. Retrieval feedback may add candidates; active-learning screening
  feedback reprioritises the existing candidate pool.
- SPLADE vocabulary weights are schematic and unmeasured. Weighted vocabulary
  representations and LLM-generated text differ in form; both can be inspected
  and passed across component boundaries.
- [Query2doc (Wang et al., 2023)](https://aclanthology.org/2023.emnlp-main.585/)
  expands the original query with a generated pseudo-document. Lexical retrieval
  is drawn; dense retrieval is also possible. No effectiveness number is claimed.
- [HyDE (Gao et al., 2023)](https://aclanthology.org/2023.acl-long.99/)
  embeds the hypothetical document and searches nearby real document vectors.
  The drawings simplify the vector space. Generated text is a retrieval aid,
  not a source. Unsupported details can steer either method.
- [Web of Science Smart Search](https://webofscience.zendesk.com/hc/en-us/articles/32587676013713-Smart-Search)
  documents Boolean conversion, semantic vector retrieval and blended results.
  The animation is a schematic arrangement, not a complete vendor algorithm.
- [EBSCO AI-Assisted Search](https://about.ebsco.com/artificial-intelligence/products/ai-assisted-search)
  parses keyword and noun phrases before its established search engine. The
  source does not identify that parsing model as an LLM.
- [Primo NDE Natural Language Search](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/040Search_Configurations/Natural_Language_Search_in_the_NDE_UI)
  documents a generative model, Boolean alternatives, inspectable Advanced
  Search input, a defined field/filter list and known author/OR relationship
  issues. It is distinct from Primo Research Assistant.
- Official sources above were checked on **4 October 2026**. These are documented
  examples, not observations or benchmarks of a local deployment. Vendor support
  can change; inspect the interface and documentation for the installation used.
- For brevity, these films summarize the chapter's mechanisms. They do not
  reproduce every table row, research statistic or screenshot. Read Chapter 11
  for the full research discussion and more product comparisons.

## Verification

Checks cover source anchors, 24 unique scenes, the graph's citation direction,
the date/filter candidate boundary, and every scene at five animation times.
Export verification fully decodes each MP4 and checks frame count, dimensions,
30 fps, H.264/AAC/subtitle codecs, exact ordered embedded captions, fast-start
atom order and SHA-256. Encoded audio must be within 1 LU of −16 LUFS and below
−1 dBTP; each narration take must exceed its music bed by at least 10 dB.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing these adaptations.
