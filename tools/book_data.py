# -*- coding: utf-8 -*-
"""Authored apparatus for the textbook edition.

Every string here is NEW prose drafted for review. Anything emitted from this
file is marked `drafted` in the HTML so it can be found and rewritten.
"""

# Pipeline stages used by the per-chapter "you are here" map.
STAGES = [
    ("t", "Query<br>transformation"),
    ("a", "Analysis &amp;<br>execution rules"),
    ("r", "First-stage<br>retrieval"),
    ("f", "Fusion"),
    ("k", "Reranking"),
    ("p", "Presentation"),
]

PARTS = {
    1: ("Part I", "How lexical retrieval works",
        "Words as admission rules, words as weighted evidence, and the difference "
        "between a lexical system and a Boolean one."),
    2: ("Part II", "Representations and retrieval pipelines",
        "What changes when a system compares learnt representations instead of "
        "strings, and how several components are assembled into a pipeline."),
    3: ("Part III", "Control, failure and professional judgement",
        "Who chooses the next retrieval action, where retrieval goes wrong, and "
        "what libraries must record, inspect and require."),
}

# chapter key -> metadata
CHAPTERS = {
    "intro": dict(
        eyebrow="Introduction",
        title="The retrieval problem",
        question="What is the retrieval half of an AI search tool actually doing?",
        stages=[],
        controller=False,
        orient=[
            "Every AI search product contains two machines. One decides which records "
            "exist as far as your question is concerned, and in what order they are "
            "placed. The other turns some of those records into prose. Almost all public "
            "discussion of AI search concerns the second machine. This book is about the "
            "first.",
            "The introduction sets the boundary of the subject, supplies the vocabulary "
            "the rest of the book depends on, and ends with two entirely ordinary search "
            "results that ought to be impossible. Those two puzzles are not decoration. "
            "Part I resolves them, and the explanation turns out to require most of the "
            "machinery of lexical retrieval.",
        ],
        established=[
            "Retrieval and generation are separate problems. A fabricated citation is a "
            "generation failure; a missing relevant paper is a retrieval one.",
            "An LLM can sit inside the retrieval half of a pipeline. Its presence says "
            "nothing about which retrieval method is being used.",
            "Tools differ along two independent axes: what they hand you, and how much "
            "retrieval they perform.",
            "Two familiar results—a nonsense term that did not empty a result list, and a "
            "reported count far larger than the viewable list—cannot be explained by "
            "strict Boolean matching.",
        ],
        transition="Explaining either puzzle requires knowing what a search system does "
                   "with words before it does anything else. Part I begins with the "
                   "strictest possible answer: words as admission rules.",
    ),
    "ch1": dict(
        eyebrow="Chapter 1", part=1,
        title="Boolean admission and the inverted index",
        question="How does a system decide which records are eligible?",
        stages=["a", "r"],
        controller=False,
        orient=[
            "Strict Boolean retrieval is the oldest answer to the retrieval problem and "
            "still the clearest. A query states conditions; a record either satisfies them "
            "or it does not. There is no notion of a better or a worse match, only "
            "membership of an eligible set.",
            "That simplicity is worth understanding precisely, because everything later in "
            "this book is a departure from it. This chapter follows a document from raw "
            "text through tokenisation, stemming and indexing, then shows how Boolean "
            "conditions are evaluated over the resulting structure—and why the answer "
            "arrives so quickly.",
        ],
        established=[
            "Text is not searched; analysed terms are. Tokenisation, case folding, "
            "stop-word handling and stemming all happen before anything is indexed.",
            "Query and document must be analysed compatibly. A mismatch between the two is "
            "a silent and common source of retrieval failure.",
            "An inverted index maps terms to posting lists, which is why Boolean evaluation "
            "is set intersection and union rather than a scan of documents.",
            "Boolean retrieval produces an eligible set, not an ordering. Nothing in the "
            "mechanism says which eligible record should appear first.",
        ],
        transition="An eligible set of forty thousand records is not a result list anyone "
                   "can use. The next chapter asks what has to be added to turn matching "
                   "into ranking.",
    ),
    "ch2": dict(
        eyebrow="Chapter 2", part=1,
        title="BM25 and ranked lexical retrieval",
        question="How does matching evidence become a relevance ranking?",
        stages=["r"],
        controller=False,
        orient=[
            "Boolean retrieval treats every matching term as equally informative and every "
            "eligible record as equally good. Neither is true. A term occurring in three "
            "records is far more discriminating than one occurring in three hundred "
            "thousand, and a record using a term eight times is usually more about it than "
            "a record using it once.",
            "BM25 is the standard way of turning those two intuitions into a score. This "
            "chapter explains what it measures, why repetition saturates rather than "
            "counting linearly, and how it runs over exactly the same inverted index the "
            "previous chapter built. The ranking is added; the index is not replaced.",
        ],
        established=[
            "BM25 treats matching terms as unequal, graded evidence rather than as "
            "satisfied conditions.",
            "Rarer terms carry more weight, repeated terms saturate, and longer documents "
            "are discounted for their length.",
            "The index does not change. The same posting lists that answered a Boolean "
            "query support a ranked one.",
            "BM25 is a first-stage ranker in production library and scholarly systems, not "
            "a historical curiosity.",
        ],
        transition="Ranking changes what a result list looks like. It also changes what "
                   "happens to a query term the system cannot match at all—and that is "
                   "where the central misconception of this book begins.",
    ),
    "ch3": dict(
        eyebrow="Chapter 3", part=1,
        title="Lexical search beyond strict Boolean",
        question="How can a search remain lexical without behaving like strict Boolean?",
        stages=["t", "a", "r"],
        controller=False,
        orient=[
            "Librarians routinely treat <em>lexical</em> and <em>Boolean</em> as synonyms, "
            "so that any system tolerating an unmatched word must be doing something "
            "semantic. That inference is wrong, and correcting it is the most important "
            "thing this book does early.",
            "A lexical system can require every term, require some proportion of them, or "
            "require none of them while still scoring on words alone. This chapter "
            "separates three layers that are easily conflated—how a query is analysed, "
            "which execution rule is applied, and whether the query was rewritten before "
            "retrieval began—and then uses them to resolve the two opening puzzles.",
        ],
        established=[
            "Lexical retrieval is broader than Boolean retrieval. Requiring every term is "
            "one execution rule among several.",
            "A missing query word has several possible lexical explanations that should be "
            "exhausted before any semantic one is reached for.",
            "Query transformation is an upstream stage, not a retrieval method. It changes "
            "what is sent to retrieval without changing what retrieval does.",
            "Early Google was non-Boolean and non-semantic at the same time, which is the "
            "cleanest available counterexample to the category error.",
            "Both opening puzzles are fully explained without invoking embeddings.",
        ],
        transition="One category error is now resolved: non-Boolean does not mean "
                   "non-lexical. A second remains. Everything so far has matched words to "
                   "words, and no amount of flexibility in the execution rule connects a "
                   "query to a document that shares none of them.",
    ),
    "ch4": dict(
        eyebrow="Chapter 4", part=2,
        title="Embeddings and dense retrieval",
        question="How can a system retrieve related texts that do not share words?",
        stages=["r"],
        controller=False,
        orient=[
            "Every method so far has compared strings. Two documents saying the same thing "
            "in different words are, to a lexical index, unrelated. Dense retrieval attacks "
            "that limitation directly: instead of matching terms, it converts text into a "
            "vector of numbers and compares positions in a space where proximity is meant "
            "to encode similarity of meaning.",
            "This is the longest chapter in the book, and it has two halves. The first "
            "builds the basic model end to end—how text reaches a model, how a vector is "
            "produced, how similar vectors are found quickly, and where the result list is "
            "cut off. The second supplies four qualifications without which the basic model "
            "is actively misleading.",
        ],
        established=[
            "A dense retriever compares learnt representations rather than strings, which "
            "is what allows it to bridge paraphrase.",
            "Model tokenisation and index analysis are different processes producing "
            "different units. A model token is not an indexed term.",
            "Approximate nearest-neighbour search is what makes dense retrieval practical, "
            "and it introduces its own effects at the candidate boundary.",
            "Top-<em>k</em> is a result boundary chosen by the system, not a property of "
            "dense retrieval.",
            "<em>Vector</em> does not imply dense or semantic, and one document does not "
            "correspond to one vector.",
        ],
        transition="A first-stage retriever, lexical or dense, has to be fast enough to run "
                   "against an entire collection—which limits how carefully it can compare "
                   "anything. The next chapter asks what a system can afford once it has a "
                   "shortlist.",
    ),
    "ch5": dict(
        eyebrow="Chapter 5", part=2,
        title="Reranking, multi-stage and hybrid retrieval",
        question="How are several retrieval and ranking components assembled into a pipeline?",
        stages=["f", "k"],
        controller=False,
        orient=[
            "No production search system is a single retriever. Comparing a query against "
            "every document in a collection rules out any expensive comparison, so real "
            "systems retrieve cheaply and broadly first, then spend computation on a "
            "shortlist small enough to afford it.",
            "That staging decision is what explains cross-encoders, LLM rerankers and the "
            "place of late interaction. It also explains hybrid retrieval, which runs more "
            "than one retriever at once and must then decide how to combine what they "
            "return. Both ideas only become meaningful now that the first-stage methods "
            "exist.",
        ],
        established=[
            "Multi-stage retrieval exists because accuracy and scale trade against each "
            "other.",
            "A reranker can only reorder what the first stage returned. It cannot recover a "
            "document that was never retrieved.",
            "Hybrid retrieval is a claim about how results are combined, not merely about "
            "containing two retrievers.",
            "Blending and routing are different designs: one merges on every query, the "
            "other chooses per query.",
        ],
        transition="Routing raises a question deferred since Chapter 3. If a system can "
                   "choose between retrieval routes, it can also change the query it sends "
                   "to them—and it need not send only one.",
    ),
    "ch6": dict(
        eyebrow="Chapter 6", part=2,
        title="Query transformation and retrieval routing",
        question="What can happen before and around retrieval once the system is no longer limited to one query?",
        stages=["t"],
        controller=False,
        orient=[
            "Chapter 3 introduced query transformation while only lexical machinery was "
            "available, so the most a system could do was rewrite one query into another. "
            "Dense retrieval, fusion and reranking change what is possible at that same "
            "stage.",
            "A system can now expand a query with learnt alternatives, decompose it into "
            "subqueries, generate a hypothetical document and retrieve with that, or send "
            "different formulations down different retrieval routes and fuse the results. "
            "This chapter returns to the transformation stage and asks what it becomes with "
            "the rest of the pipeline behind it.",
        ],
        established=[
            "Transformation remains an upstream stage, however sophisticated it becomes.",
            "Expansion, decomposition and pseudo-relevance feedback change the query. They "
            "do not change the retriever that receives it.",
            "Query2doc and HyDE retrieve using generated text, which makes that generated "
            "text part of the search strategy and part of what must be recorded.",
            "Natural-language filter extraction is genuinely useful and reliably partial.",
        ],
        transition="Every operation described so far could have been arranged in advance. A "
                   "designer could have specified the expansions, the routes and the fusion "
                   "rule before any user arrived. Part III begins where that stops being "
                   "true.",
    ),
    "ch7": dict(
        eyebrow="Chapter 7", part=3,
        title="Agentic search",
        question="Who chooses the next retrieval action?",
        stages=[],
        controller=True,
        orient=[
            "Everything to this point has been a pipeline: an arrangement of stages, "
            "possibly with branches, all decided before the search ran. Agentic search "
            "removes that guarantee. A model inspects what came back and decides what to do "
            "next.",
            "That is a change in control, not in retrieval. The retrievers, rerankers and "
            "fusion rules are the ones already described. This chapter separates fixed, "
            "adaptive and agentic arrangements, locates current academic tools among them, "
            "and is candid about what agency costs—including two problems specific to "
            "retrieval that iteration can make worse rather than better.",
        ],
        established=[
            "Fixed, adaptive and agentic describe who decides the next action, not how "
            "documents are scored.",
            "Agency changes the sequence, not the retrieval. Nothing about a loop improves "
            "the retriever inside it.",
            "A trace shows what a system did. It does not reveal what the system could have "
            "done, which is a separate and largely invisible limit.",
            "Recall failures compound across rounds, because each round is chosen on the "
            "basis of what the previous one returned.",
            "Agentic RAG is a narrower case of agentic search, not a synonym for it.",
        ],
        transition="The pipeline is now complete, from query transformation through to the "
                   "controller that sequences everything. That makes a different question "
                   "possible: not what each component does, but where a particular search "
                   "went wrong.",
    ),
    "ch8": dict(
        eyebrow="Chapter 8", part=3,
        title="Diagnosing retrieval failure",
        question="At which layer did retrieval fail, and what remedy actually addresses it?",
        stages=["t", "a", "r", "f", "k", "p"],
        controller=True,
        orient=[
            "From the result screen, every retrieval failure looks the same: a relevant "
            "record is missing, or an irrelevant one sits near the top. From inside the "
            "pipeline they are not the same at all, and the interventions that fix them "
            "have almost nothing in common.",
            "This chapter works backwards. It separates four problems that are routinely "
            "collapsed into a single complaint about vocabulary, matches each to the "
            "remedies that actually address it, and closes by comparing what the three "
            "first-stage approaches preserve and what each characteristically loses.",
        ],
        established=[
            "Mismatch, gap, domain shift and composition failure look alike on screen and "
            "originate at different points in the pipeline.",
            "Only the first two are vocabulary problems. Domain shift is a learnt-relevance "
            "problem, and composition failure is about combination.",
            "The remedy follows from the origin, which is why the diagnosis matters more "
            "than the symptom.",
            "No first-stage approach preserves everything, and asking whether a product "
            "uses vectors reveals almost nothing about its behaviour.",
        ],
        transition="If no label reliably predicts behaviour, a library cannot evaluate a "
                   "search product from its description. The final chapter asks what it "
                   "must record, inspect and require instead.",
    ),
    "ch9": dict(
        eyebrow="Chapter 9", part=3,
        title="Implications for library practice and tool evaluation",
        question="What must libraries record, inspect, test and require?",
        stages=["t", "a", "r", "f", "k", "p"],
        controller=True,
        orient=[
            "Most librarians will never train a retriever. They will license one, teach with "
            "it, document searches performed in it, and be asked whether its results can be "
            "trusted. The technical content of this book exists to make those four things "
            "possible.",
            "Three consequences follow, and they are ordered by dependency. A search must be "
            "documentable before it can be compared. Retrieval must be inspectable before an "
            "explanation means anything. And both must be required in advance, because "
            "neither can be retrofitted to a product that was not built to expose them.",
        ],
        established=[
            "Reproducibility is conditional on a fixed system, and it is also a "
            "documentation practice rather than a property of a method.",
            "Saving the natural-language question is insufficient whenever the system "
            "rewrote it.",
            "A faithful explanation is an execution trace. A plausible narrative is not "
            "evidence of what drove a result.",
            "Libraries do not need model weights. They need enough visibility to establish "
            "what was searched, enough documentation to compare it later, and enough control "
            "to test it locally.",
        ],
        transition=None,
    ),
}

# One substantial application exercise at the end of each part.
EXERCISES = {
    1: dict(
        title="Application exercise I — Explain a result list without invoking meaning",
        lead="Part I claims that a great deal of apparently intelligent search behaviour is "
             "lexical. This exercise tests that claim against a system you actually support.",
        steps=[
            "Choose a discovery layer or database your library licenses. Run a natural-language "
            "query of six to eight words—a real question, not a keyword string.",
            "Record four observations: the reported result count; how many records you can "
            "actually page through; whether every query term appears somewhere in the first "
            "result; and what happens to the count when you add one invented word to the query.",
            "Account for each observation using only Chapters 1 to 3. For each, name which of "
            "the three layers explains it: query analysis, the execution rule, or query "
            "transformation before retrieval.",
            "Repeat the query with every term quoted and joined by <code>AND</code>. Note what "
            "changes, and decide whether the difference tells you about the execution rule or "
            "about the analyser.",
        ],
        deliverable="A one-page note stating which layer explains each observation—and, "
                    "importantly, listing any observation you could not explain lexically. That "
                    "residue is what Parts II and III have to account for.",
    ),
    2: dict(
        title="Application exercise II — Map a product onto the pipeline",
        lead="Part II assembled a pipeline: transformation, first-stage retrieval, fusion, "
             "reranking, presentation. This exercise asks how much of it a vendor will tell you.",
        steps=[
            "Choose one product your library licenses that advertises semantic, natural-language "
            "or AI search.",
            "Using vendor documentation, release notes and help pages only—not marketing "
            "copy—fill in each of the six pipeline stages for that product.",
            "Mark every stage as <strong>documented</strong> (the vendor states it), "
            "<strong>inferred</strong> (you deduced it from observed behaviour), or "
            "<strong>unknown</strong>.",
            "For the indexed unit specifically, establish whether the product retrieves titles, "
            "abstracts, passages or full text. Test it: find a claim that appears only in the "
            "full text of a paper you know, and search for it.",
        ],
        deliverable="A completed six-stage map with each stage labelled by evidence type, plus "
                    "the single question you would put to the vendor about the stage you could "
                    "least determine. Bring the map to your next renewal conversation.",
    ),
    3: dict(
        title="Application exercise III — Diagnose a failure, then try to document it",
        lead="Part III supplied a diagnosis (Chapter 8) and a record (Chapter 9). This exercise "
             "runs both against a search that genuinely disappointed you.",
        steps=[
            "Find a search where a product returned a poor result for a topic you know well "
            "enough to judge—ideally one where you can name a relevant record it missed.",
            "Diagnose it using Chapter 8's four categories. State which one it is and what "
            "evidence rules out the other three.",
            "Apply the remedy the diagnosis implies, not the one you would have reached for "
            "first. Record whether it worked.",
            "Now attempt the Chapter 9 record: query interpretation, candidate retrieval, "
            "ranking and fusion, and agentic control if any. Fill in everything the product "
            "will let you capture.",
        ],
        deliverable="Two lists. The diagnosis with its supporting evidence, and—more useful "
                    "institutionally—a gap list of everything the product would not let you "
                    "record. The second list is the practical case for or against renewal.",
    ),
}

# Table captions, keyed by the table's ordinal position in the source article (1-based).
TABLE_CAPTIONS = {
    1: "Stages of lexical analysis, and what a sample string looks like after each.",
    2: "Stemming and lemmatisation compared: how each reduces a word, and what to remember about the difference.",
    3: "A miniature four-record collection, used throughout this chapter.",
    4: "The same four records as an inverted index: each term paired with its posting list.",
    5: "Scholarly and library systems documented as running on Lucene-family lexical infrastructure.",
    6: "Word-level and subword tokenisation compared on an unfamiliar string.",
    7: "Lexical index terms and dense model tokens are produced by different processes and are not interchangeable.",
    8: "How the candidate set is bounded on the lexical route and on the dense-vector route.",
    9: "Three retrieval methods by representation: how their weights arise, and what their dimensions mean.",
    10: "The stages of a multi-stage pipeline, and why each belongs where it does.",
    11: "One discovery product mapped to every stage described in this book, with the chapter that explains each.",
    12: "Common query-understanding techniques: what each changes, and the main risk it introduces.",
    13: "Query transformation in current discovery products, and what each case illustrates.",
    14: "Natural-language filter extraction across products, with the documented boundary in each case.",
    15: "Fixed, adaptive and agentic control arrangements, distinguished by how the next action is decided.",
    16: "Deep search and deep research compared by search trajectory and by main output.",
    17: "Where current academic tools sat at the time of testing, by control arrangement.",
    18: "What agency costs and what it buys, against a fixed or rule-based workflow.",
    19: "Three distinct questions hidden inside a single complaint about an out-of-vocabulary term.",
    20: "Matching visible symptoms to their likely origin in the pipeline, and to the remedy that addresses it.",
    21: "The three main first-stage approaches: what each preserves, its characteristic strength and its blind spot.",
    22: "The four pipeline areas a reproducible search record must cover.",
    23: "Detailed reporting requirements by retrieval method.",
    24: "What an explanation can show at each pipeline stage, and what it cannot establish by itself.",
    25: "Character and byte tokenisation compared on an unfamiliar string.",
    26: "The same posting lists used for Boolean evaluation and for BM25 scoring.",
}
