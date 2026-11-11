/* Search Time Machine interface: the decade dial, seven period screens and the placard.
 * Retrieval lives in search-time-machine-engine.js; this file only renders. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const up = s => esc(String(s).toUpperCase());

  const PRESETS = [
    { tag: 'A plain question', q: 'why did my search miss a relevant paper' },
    { tag: 'One exact term', q: 'BM25' },
    { tag: 'Two typos', q: 'retreival augmented genration' },
    { tag: 'Boolean logic', q: 'hybrid AND NOT dense' },
    { tag: 'A reviewer asks', q: 'can I reproduce a search for a systematic review' },
    { tag: 'No shared words', q: 'doctors hunting for clinical trials' },
  ];

  const REFS = {
    taube1952: ['Taube et al. 1952', 'Taube, M., Gull, C. D., &amp; Wachtel, I. S. (1952). Unit terms in coordinate indexing. <i>American Documentation</i>, 3(4), 213–218.', 'https://doi.org/10.1002/asi.5090030404'],
    cleverdon1967: ['Cleverdon 1967', 'Cleverdon, C. W. (1967). The Cranfield tests on index language devices. <i>Aslib Proceedings</i>, 19(6), 173–194.', 'https://doi.org/10.1108/eb050097'],
    lancaster1969: ['Lancaster 1969', 'Lancaster, F. W. (1969). MEDLARS: Report on the evaluation of its operating efficiency. <i>American Documentation</i>, 20(2), 119–142.', 'https://doi.org/10.1002/asi.4630200204'],
    bourne2003: ['Bourne &amp; Hahn 2003', 'Bourne, C. P., &amp; Hahn, T. B. (2003). <i>A history of online information services, 1963–1976</i>. MIT Press.', 'https://doi.org/10.7551/mitpress/3543.001.0001'],
    drew1966: ['Drew et al. 1966', 'Drew, D. L., Summit, R. K., Tanaka, R. I., &amp; Whiteley, R. B. (1966). An on-line technical library reference retrieval system. <i>American Documentation</i>, 17(1).', 'https://doi.org/10.1002/asi.5090170103'],
    borgman1986: ['Borgman 1986', 'Borgman, C. L. (1986). Why are online catalogs hard to use? Lessons learned from information-retrieval studies. <i>Journal of the American Society for Information Science</i>, 37(6), 387–400.', 'https://doi.org/10.1002/asi.4630370604'],
    borgman1996: ['Borgman 1996', 'Borgman, C. L. (1996). Why are online catalogs still hard to use? <i>Journal of the American Society for Information Science</i>, 47(7), 493–503.', 'https://doi.org/10.1002/(SICI)1097-4571(199607)47:7%3C493::AID-ASI3%3E3.0.CO;2-P'],
    robertson1997: ['Robertson 1997', 'Robertson, S. E. (1997). Overview of the Okapi projects. <i>Journal of Documentation</i>, 53(1), 3–7.', 'https://doi.org/10.1108/EUM0000000007186'],
    sparckjones1972: ['Spärck Jones 1972', 'Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. <i>Journal of Documentation</i>, 28(1), 11–21.', 'https://doi.org/10.1108/eb026526'],
    salton1975: ['Salton, Wong &amp; Yang 1975', 'Salton, G., Wong, A., &amp; Yang, C. S. (1975). A vector space model for automatic indexing. <i>Communications of the ACM</i>, 18(11), 613–620.', 'https://doi.org/10.1145/361219.361220'],
    harman1993: ['Harman 1993', 'Harman, D. (1993). Overview of the first TREC conference. <i>Proceedings of SIGIR 1993</i>, 36–47.', 'https://doi.org/10.1145/160688.160692'],
    porter1980: ['Porter 1980', 'Porter, M. F. (1980). An algorithm for suffix stripping. <i>Program</i>, 14(3), 130–137.', 'https://doi.org/10.1108/eb046814'],
    robertson1995: ['Robertson et al. 1995', 'Robertson, S. E., Walker, S., Jones, S., Hancock-Beaulieu, M. M., &amp; Gatford, M. (1995). Okapi at TREC-3. In <i>Overview of the Third Text REtrieval Conference (TREC-3)</i>. NIST Special Publication 500-225.', 'https://openalex.org/W1482214997'],
    robertson2009: ['Robertson &amp; Zaragoza 2009', 'Robertson, S., &amp; Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. <i>Foundations and Trends in Information Retrieval</i>, 3(4), 333–389.', 'https://doi.org/10.1561/1500000019'],
    brin1998: ['Brin &amp; Page 1998', 'Brin, S., &amp; Page, L. (1998). The anatomy of a large-scale hypertextual Web search engine. <i>Computer Networks and ISDN Systems</i>, 30(1–7), 107–117.', 'https://doi.org/10.1016/S0169-7552(98)00110-X'],
    franceschet2011: ['Franceschet 2011', 'Franceschet, M. (2011). PageRank: Standing on the shoulders of giants. <i>Communications of the ACM</i>, 54(6), 92–101. Preprint cited.', 'https://doi.org/10.48550/arXiv.1002.2858'],
    tombros1998: ['Tombros &amp; Sanderson 1998', 'Tombros, A., &amp; Sanderson, M. (1998). Advantages of query biased summaries in information retrieval. <i>Proceedings of SIGIR 1998</i>, 2–10.', 'https://doi.org/10.1145/290941.290947'],
    joachims2002: ['Joachims 2002', 'Joachims, T. (2002). Optimizing search engines using clickthrough data. <i>Proceedings of KDD 2002</i>, 133–142.', 'https://doi.org/10.1145/775047.775067'],
    mikolov2013: ['Mikolov et al. 2013', 'Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., &amp; Dean, J. (2013). Distributed representations of words and phrases and their compositionality. <i>Advances in Neural Information Processing Systems 26</i>, 3111–3119.', 'https://arxiv.org/abs/1310.4546'],
    pennington2014: ['Pennington, Socher &amp; Manning 2014', 'Pennington, J., Socher, R., &amp; Manning, C. D. (2014). GloVe: Global vectors for word representation. <i>Proceedings of EMNLP 2014</i>, 1532–1543.', 'https://doi.org/10.3115/v1/D14-1162'],
    devlin2019: ['Devlin et al. 2019', 'Devlin, J., Chang, M.-W., Lee, K., &amp; Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. <i>Proceedings of NAACL-HLT 2019</i>, 4171–4186.', 'https://doi.org/10.18653/v1/N19-1423'],
    karpukhin2020: ['Karpukhin et al. 2020', 'Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., &amp; Yih, W. (2020). Dense passage retrieval for open-domain question answering. <i>Proceedings of EMNLP 2020</i>, 6769–6781.', 'https://doi.org/10.18653/v1/2020.emnlp-main.550'],
    cormack2009: ['Cormack, Clarke &amp; Büttcher 2009', 'Cormack, G. V., Clarke, C. L. A., &amp; Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. <i>Proceedings of SIGIR 2009</i>, 758–759.', 'https://doi.org/10.1145/1571941.1572114'],
    nogueira2019: ['Nogueira &amp; Cho 2019', 'Nogueira, R., &amp; Cho, K. (2019). Passage re-ranking with BERT. <i>arXiv preprint arXiv:1901.04085</i>.', 'https://arxiv.org/abs/1901.04085'],
    khattab2020: ['Khattab &amp; Zaharia 2020', 'Khattab, O., &amp; Zaharia, M. (2020). ColBERT: Efficient and effective passage search via contextualized late interaction over BERT. <i>Proceedings of SIGIR 2020</i>, 39–48.', 'https://doi.org/10.1145/3397271.3401075'],
    lewis2020: ['Lewis et al. 2020', 'Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., &amp; Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. <i>Advances in Neural Information Processing Systems 33</i>, 9459–9474.', 'https://arxiv.org/abs/2005.11401'],
    thakur2021: ['Thakur et al. 2021', 'Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., &amp; Gurevych, I. (2021). BEIR: A heterogeneous benchmark for zero-shot evaluation of information retrieval models. <i>NeurIPS 2021 Datasets and Benchmarks Track</i>.', 'https://arxiv.org/abs/2104.08663'],
    khodak2018: ['Khodak et al. 2018', 'Khodak, M., Saunshi, N., Liang, Y., Ma, T., Stewart, B., &amp; Arora, S. (2018). A la carte embedding: Cheap but effective induction of semantic feature vectors. <i>Proceedings of ACL 2018</i>, 12–22.', 'https://doi.org/10.18653/v1/P18-1002'],
    manning2008: ['Manning, Raghavan &amp; Schütze 2008', 'Manning, C. D., Raghavan, P., &amp; Schütze, H. (2008). <i>Introduction to information retrieval</i>. Cambridge University Press.', 'https://doi.org/10.1017/CBO9780511809071'],
  };
  const c = key => '<a href="' + REFS[key][2] + '" target="_blank" rel="noopener">' + REFS[key][0] + '</a>';

  let corpus, engine, vmeta, sample = null;
  const state = { era: 'e1960', query: PRESETS[0].q, result: null, track: -1, pinned: false, ms: 0, touring: false, timer: 0 };

  const doc = d => corpus.docs[d];
  const chap = d => corpus.chapters[doc(d).c];
  const loc = d => { const n = chap(d).n; return n ? n.replace('Chapter ', 'Ch ').replace('Appendix ', 'App ') : 'Coda'; };
  const url = d => corpus.book.url + '#' + doc(d).id;
  const acc = d => String(d + 1).padStart(4, '0');
  const hcls = d => ' hit' + (d === state.track ? ' tracked' : '');
  const hattr = d => ' data-d="' + d + '" tabindex="0" role="button" aria-label="Follow this section through the decades: ' + esc(doc(d).t) + '"';
  const hit = (d, cls) => 'class="' + cls + hcls(d) + '"' + hattr(d);
  const subjects = (d, n) => engine.docTerms[d].slice(0, n).map(t => (t.major ? '*' : '') + engine.terms[t.t].head);

  const ERAS = [
    { key: 'e1960', yr: '1960s', nm: 'Batch run', title: 'The search analyst', who: 'A person, then a thesaurus',
      reads: 'Index terms assigned to each section by an indexer. Here the thesaurus is the book’s glossary.',
      admits: 'Sections carrying every chosen term.', orders: 'Accession order. Nothing is ranked.',
      story: () => 'You did not search. You handed over a request, a trained analyst translated it into approved index terms, and a computer matched those terms in a batch run. The printout came back later. Coordinate indexing with unit terms dates from ' + c('taube1952') + '. MEDLARS ran this way at the US National Library of Medicine from 1964, and ' + c('lancaster1969') + ' evaluated why its searches failed. ' + c('cleverdon1967') + ' tested index languages at Cranfield in the same decade.',
      gained: 'One concept, one agreed term, whatever words the author used.',
      missing: 'Anything the thesaurus has no term for is unaskable, and you cannot try again until the next run.', book: 'boolean-admission' },
    { key: 'e1970', yr: '1970s', nm: 'Online Boolean', title: 'The online terminal', who: 'Your logic',
      reads: 'Every word of the full text, exactly as written. No stemming: paper is not papers.',
      admits: 'Records that satisfy the Boolean statement.', orders: 'Newest record first. Nothing is ranked.',
      story: () => 'Searching went interactive. NLM put MEDLINE online in 1971, Lockheed offered DIALOG commercially from 1972, and searchers built sets with AND, OR and NOT while watching the posting counts (' + c('bourne2003') + '; an early Lockheed system is described by ' + c('drew1966') + '). Services charged by connect time, so strategies were planned on paper first.',
      gained: 'Control and transparency. The same statement returns the same set, which is why systematic reviewers still write Boolean.',
      missing: 'A record is in or out. You get nothing or a flood, with no sign of which records matter most.', book: 'boolean-admission' },
    { key: 'e1980', yr: '1980s', nm: 'The catalogue', title: 'The online catalogue', who: 'The catalogue record',
      reads: 'Only what is on the record: section title, chapter title and subject headings. Never the text.',
      admits: 'Records containing all of your words.', orders: 'Alphabetically by title.',
      story: () => 'Online public access catalogues let library users search for themselves, against brief records designed for card catalogues. ' + c('borgman1986') + ' asked why they were hard to use, and ten years later asked why they were still hard to use (' + c('borgman1996') + '). One experimental catalogue of the period was Okapi, at the Polytechnic of Central London. The ranking function later developed for it is still called Okapi BM25 (' + c('robertson1997') + ').',
      gained: 'Self-service, from a terminal in the library.',
      missing: 'If the record does not say it, the catalogue cannot find it. A natural question matches almost nothing.', book: 'beyond-boolean' },
    { key: 'e1990', yr: '1990s', nm: 'Ranked web', title: 'The first web engines', who: 'Word statistics',
      reads: 'The full text, with words reduced to stems.',
      admits: 'Any section sharing at least one word with you.', orders: 'By tf-idf cosine similarity: rare words count more, and long sections are normalised.',
      story: () => 'Ranking by term statistics was already old in the laboratory. ' + c('sparckjones1972') + ' proposed weighting terms by their rarity, and ' + c('salton1975') + ' set out the vector space model. TREC began in 1992 and gave researchers shared large test collections (' + c('harman1993') + '). The web then made best-first lists the public default: type words, no syntax, read from the top. Stemming here follows ' + c('porter1980') + '.',
      gained: 'No query language, partial matches, and an order to read in.',
      missing: 'Repeating a word looks like relevance, nothing knows which pages are trusted, and the summary is only the first lines of the page.', book: 'bm25-ranking' },
    { key: 'e2000', yr: '2000s', nm: 'Links & snippets', title: 'Links and snippets', who: 'Word statistics, plus everyone else’s links',
      reads: 'Full text with the title weighted more, plus the graph of who links to whom.',
      admits: 'Any section sharing a word. Sections with all of your words are favoured.', orders: 'BM25, lifted by a link-analysis prior.',
      story: () => c('brin1998') + ' ranked pages partly by the links pointing at them, an idea with roots in citation analysis (' + c('franceschet2011') + '). Here the links are the book’s own ' + state.links + ' cross-references. Term weighting had matured into BM25 (' + c('robertson1995') + '; ' + c('robertson2009') + '), summaries became query-biased snippets (' + c('tombros1998') + '), and engines began correcting spelling and learning from clicks (' + c('joachims2002') + ').',
      gained: 'A signal of authority, summaries that show why a result matched, and recovery from typos.',
      missing: 'Still only your words. A section that explains your problem in other words stays buried.', book: 'bm25-ranking' },
    { key: 'e2010', yr: '2010s', nm: 'Word vectors', title: 'Meaning as geometry', who: 'Geometry',
      reads: () => 'Each paragraph as one point in ' + vmeta.dims + '-dimensional space, averaged from its word vectors.',
      admits: 'Everything. Every section has a distance, so the list is never empty.', orders: 'By closeness to the query point.',
      story: () => c('mikolov2013') + ' and ' + c('pennington2014') + ' placed words in a space where neighbours tend to share meaning, so a search could match physician to doctor with no thesaurus. This stop uses GloVe vectors. One vector per word is also the weakness: here the nearest neighbours of “miss” are ' + engine.neighbours('miss', 3).map(n => n.w).join(', ') + '. Contextual models (' + c('devlin2019') + ') and trained dense retrievers (' + c('karpukhin2020') + ') addressed that, and are too large to run in this page.',
      gained: 'Vocabulary mismatch shrinks: related wording can match.',
      missing: 'It cannot say no, cannot show which words matched, and blurs exact names and identifiers. A word with no vector is invisible.', book: 'embeddings' },
    { key: 'e2020', yr: '2020s', nm: 'Answer engine', title: 'The answer engine', who: 'A pipeline, then a writer',
      reads: 'Words and vectors together.',
      admits: 'The top 40 sections by BM25 and the top 40 by vectors.', orders: 'Reciprocal rank fusion, then a reranker over the best 24. An answer is composed from the top passages.',
      story: () => 'Hybrid systems run lexical and dense retrieval side by side and fuse the lists, often with reciprocal rank fusion (' + c('cormack2009') + '). A reranker rereads the shortlist (' + c('nogueira2019') + '; the soft matching here borrows from ' + c('khattab2020') + '), and a language model writes from what was retrieved: retrieval-augmented generation (' + c('lewis2020') + '). BM25 remains a strong zero-shot baseline (' + c('thakur2021') + '), which is why it is still in the pipeline.',
      gained: 'A direct answer with its sources, and two retrieval routes covering for each other.',
      missing: 'You read three sentences, not the list. What the pipeline never retrieved, the answer cannot know is missing.', book: 'hybrid-and-fusion' },
  ];
  const eraOf = key => ERAS.find(e => e.key === key);

  // ---------------------------------------------------------------- 1960s
  const HOLE = { '&': [12], '-': [11], '/': [0, 1], '.': [12, 3, 8], '(': [12, 5, 8], '+': [12, 6, 8], '!': [11, 2, 8], '$': [11, 3, 8],
    '*': [11, 4, 8], ')': [11, 5, 8], ';': [11, 6, 8], ',': [0, 3, 8], '%': [0, 4, 8], '?': [0, 7, 8], ':': [2, 8], '#': [3, 8], '@': [4, 8],
    "'": [5, 8], '=': [6, 8], '"': [7, 8] };
  function punches(ch) {
    const k = ch.charCodeAt(0);
    if (ch >= '0' && ch <= '9') return [+ch];
    if (ch >= 'A' && ch <= 'I') return [12, k - 64];
    if (ch >= 'J' && ch <= 'R') return [11, k - 73];
    if (ch >= 'S' && ch <= 'Z') return [0, k - 81];
    return HOLE[ch] || [];
  }
  function punchedCard(query) {
    // 80 columns, 12 rows (12, 11, 0-9), IBM 029 keypunch code.
    const text = query.toUpperCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[^A-Z0-9 &\-\/.()+!$*;,%?:#@'="]/g, ' ').slice(0, 80);
    const W = 740, H = 326, x0 = 26, dx = (W - 52) / 80, y0 = 46, dy = 22.6;
    const rowY = r => y0 + (r === 12 ? 0 : r === 11 ? 1 : r + 2) * dy;
    let holes = '', print = '';
    for (let i = 0; i < text.length; i++) {
      const x = x0 + i * dx;
      for (const r of punches(text[i])) holes += '<rect x="' + (x + dx * 0.2).toFixed(1) + '" y="' + (rowY(r) - 8).toFixed(1) + '" width="' + (dx * 0.6).toFixed(1) + '" height="16" fill="#1d2129"/>';
      if (text[i] !== ' ') print += '<text x="' + (x + dx / 2).toFixed(1) + '" y="24" text-anchor="middle">' + esc(text[i]) + '</text>';
    }
    let digits = '';
    for (let r = 0; r <= 9; r++) {
      digits += '<text x="' + x0 + '" y="' + (rowY(r) + 4.5).toFixed(1) + '" textLength="' + (80 * dx).toFixed(1) + '" lengthAdjust="spacing" style="white-space:pre">' + String(r).repeat(80).split('').join(' ') + '</text>';
    }
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Punched card carrying the request in Hollerith code">' +
      '<path d="M22 0H' + W + 'V' + H + 'H0V20Z" fill="#eadfbf"/>' +
      '<g font-family="IBM Plex Mono,monospace" font-size="6.6" fill="#b3a27c">' + digits + '</g>' +
      '<g font-family="IBM Plex Mono,monospace" font-size="9.5" font-weight="600" fill="#3a3324">' + print + '</g>' + holes +
      '<text x="' + (W - 12) + '" y="' + (H - 8) + '" text-anchor="end" font-family="IBM Plex Mono,monospace" font-size="7" fill="#9c8c66">SEARCH REQUEST CARD 5081</text></svg>';
  }
  function runNo(q) { let h = 7; for (const ch of q) h = (h * 31 + ch.charCodeAt(0)) % 9000; return String(1000 + h); }

  function render1960(r) {
    const e = r.e1960, L = [];
    const ln = (html, cls, d) => L.push('<div class="ln ' + (cls || '') + (d === undefined ? '"' : hcls(d) + '"' + hattr(d)) + ' style="--i:' + L.length + '">' + html + '</div>');
    ln('<span>LITERATURE SEARCH SERVICE</span><span>BATCH RUN ' + runNo(r.q.text) + '</span>', 'hd');
    ln('', 'rule');
    ln('REQUEST AS RECEIVED');
    ln('   ' + up(r.q.text));
    ln('ANALYST’S FORMULATION, FROM A THESAURUS OF ' + engine.terms.length + ' TERMS');
    if (e.descriptors.length) for (const t of e.descriptors) ln('   ' + up(t.label) + '  <span class="dim">(' + t.postings + ' SECTIONS INDEXED)</span>');
    else ln('   NO THESAURUS TERM MATCHES THIS REQUEST.');
    if (e.ignored.length) ln('   <span class="dim">NOT IN THESAURUS, SO NOT SEARCHED: ' + up(e.ignored.join(', ')) + '</span>');
    if (e.mode !== 'NONE') {
      ln('SEARCH STATEMENT');
      ln('   ' + up(e.descriptors.map(t => t.label).join(e.mode === 'OR' ? ' OR ' : ' AND ')) + (e.mode === 'OR' ? '  <span class="dim">(NO SECTION CARRIES ALL TERMS. BROADENED TO OR.)</span>' : ''));
    }
    ln('<span>CITATIONS RETRIEVED: ' + e.total + ' OF ' + engine.N + '</span><span>' + (e.total ? 'PRINTED IN ACCESSION ORDER' : '') + '</span>', 'hd');
    ln('', 'rule');
    if (!e.total) {
      ln('REQUEST RETURNED TO REQUESTER. RESTATE IT USING THESAURUS TERMS, SUCH AS:');
      const pop = engine.terms.slice().sort((a, b) => b.docs.length - a.docs.length).slice(0, 8);
      ln('   ' + pop.map(t => '<button type="button" class="sug" data-q="' + esc(t.head) + '">' + up(t.head) + '</button>').join('   '));
    }
    for (const d of e.list.slice(0, 9)) {
      ln('<span>' + acc(d) + '</span><span>' + up(loc(d)) + '</span><span>' + up(doc(d).t) + '</span><span class="ix">INDEXED: ' + up(subjects(d, 5).join('. ')) + '.</span>', 'cit', d);
    }
    if (e.total > 9) ln('   ... AND ' + (e.total - 9) + ' MORE CITATIONS ON THE FOLLOWING SHEETS.', 'dim');
    ln('', 'rule');
    ln('*** END OF RUN ***   PRINTOUT RETURNED TO REQUESTER');
    return '<div class="s60"><figure>' + punchedCard(r.q.text) +
      '<figcaption>The request, punched in Hollerith code. Each column of holes is one character.</figcaption></figure>' +
      '<div class="paper">' + L.join('') + '</div></div>';
  }

  // ---------------------------------------------------------------- 1970s
  function render1970(r) {
    const e = r.e1970, L = [];
    let i = 0;
    const tl = (html, cls, d) => { L.push('<div class="tl ' + (cls || '') + (d === undefined ? '"' : hcls(d) + '"' + hattr(d)) + ' style="--i:' + i + '">' + html + '</div>'); i++; };
    const cmd = text => { L.push('<div class="tl cmd" style="--i:' + i + '"><span>?</span><span class="ty" style="--n:' + text.length + ';--i:' + i + '">' + esc(text) + '</span></div>'); i += 2 + Math.ceil(text.length / 6); };
    const typeSet = (name, list, total) => {
      const n = Math.min(5, list.length);
      cmd('TYPE ' + name + '/TITLE/1-' + n);
      list.slice(0, n).forEach((d, k) => tl('<span>' + (k + 1) + '/' + total + '</span><span>ACCESSION ' + acc(d) + ' · ' + up(loc(d)) + '<br>' + up(doc(d).t) + '</span>', 'rec', d));
      if (total > n) tl((total - n) + (total - n === 1 ? ' MORE RECORD IN ' : ' MORE RECORDS IN ') + name + '. NO RANKING: NEWEST RECORD PRINTS FIRST.', 'dimt');
    };
    tl('** ONLINE RETRIEVAL SERVICE **   LINE SPEED 300 BAUD');
    tl('FILE 1: HOW SEARCH DECIDES WHAT YOU SEE. ' + engine.N + ' RECORDS, FULL TEXT.', 'dimt');
    if (!e.statement) {
      cmd('SELECT');
      tl('NOTHING TO SELECT. EVERY WORD ENTERED IS A STOP WORD.');
    } else {
      cmd('SELECT ' + e.statement);
      if (!e.explicit) {
        const stops = r.q.all.filter(w => STM.STOP.has(w));
        if (stops.length) tl('STOP WORDS NOT SEARCHED: ' + up([...new Set(stops)].join(' ')), 'dimt');
      }
      for (const t of e.terms) tl('<span></span><span class="num">' + t.postings + '</span><span>' + esc(t.label) + '</span>', 'row');
      tl('<span>S1</span><span class="num">' + e.total + '</span><span>' + esc(e.statement) + '</span>', 'set');
      if (e.total) typeSet('S1', e.list, e.total);
      else if (e.broadened) {
        tl('NO RECORD CONTAINS ALL OF THESE WORDS EXACTLY AS TYPED.', 'dimt');
        cmd('SELECT ' + e.broadened.statement);
        tl('<span>S2</span><span class="num">' + e.broadened.list.length + '</span><span>' + esc(e.broadened.statement) + '</span>', 'set');
        if (e.broadened.list.length) typeSet('S2', e.broadened.list, e.broadened.list.length);
      } else tl('NO RECORDS TO TYPE.', 'dimt');
    }
    L.push('<div class="tl cmd" style="--i:' + (i + 1) + '"><span>?</span><span class="cur"></span></div>');
    L.push('<div class="tl dimt" style="--i:' + (i + 2) + '">CONNECT TIME ' + (0.012 + r.q.text.length * 0.0006).toFixed(3) + ' HRS. BILLED BY THE CONNECT HOUR.</div>');
    return '<div class="crt s70"><div class="tube"><div class="text">' + L.join('') + '</div></div>' +
      '<div class="plate"><span>Dataterm 300</span><i></i></div></div>';
  }

  // ---------------------------------------------------------------- 1980s
  function render1980(r) {
    const e = r.e1980;
    const row = (d, n, extra) => '<li ' + hit(d, 'orow') + '><span>' + n + '</span><span>' + up(doc(d).t) + '</span><span>' + up(loc(d)) + '</span>' + (extra || '') + '</li>';
    let body = '<p>YOUR SEARCH: <span class="hl">K=' + up(r.q.content.join(' ') || r.q.text) + '</span></p>' +
      '<p class="dimt">KEYWORD SEARCH READS THE CATALOGUE RECORD ONLY: TITLE, CHAPTER AND SUBJECT HEADINGS.</p>';
    if (e.terms.length) body += '<div class="ocount">' + e.terms.map(t => '<span>' + up(t.w) + '</span><span>' + t.postings + (t.postings === 1 ? ' ENTRY' : ' ENTRIES') + '</span>').join('') + '</div>';
    if (e.total) {
      body += '<p class="hl">' + e.total + (e.total === 1 ? ' RECORD CONTAINS' : ' RECORDS CONTAIN') + ' ALL OF YOUR WORDS. FILED ALPHABETICALLY.</p><ol>' +
        e.list.slice(0, 7).map((d, k) => row(d, k + 1, '<span class="os">SUBJECTS: ' + up(subjects(d, 3).join(' -- ').replace(/\*/g, '')) + '</span>')).join('') + '</ol>';
      if (e.total > 7) body += '<p class="dimt">' + (e.total - 7) + ' MORE. PRESS F8 FOR THE NEXT SCREEN.</p>';
    } else if (e.browse) {
      body += '<p class="hl">NO RECORD CONTAINS ALL OF YOUR WORDS.</p><p>NEAREST TITLES IN THE ALPHABETICAL INDEX:</p><ol>' +
        e.browse.before.map((d, k) => row(d, k + 1)).join('') +
        '<li class="here">&gt;&gt; ' + up(e.browse.key) + ' WOULD FILE HERE &lt;&lt;</li>' +
        e.browse.after.map((d, k) => row(d, e.browse.before.length + k + 1)).join('') + '</ol>';
    } else body += '<p class="hl">ENTER ONE OR MORE WORDS.</p>';
    return '<div class="crt pc s80"><div class="tube"><div class="text">' +
      '<div class="ohead"><span>ONLINE PUBLIC ACCESS CATALOGUE</span><span>TERMINAL 04</span></div>' +
      '<div class="obody">' + body + '</div>' +
      '<div class="okeys"><span><b>F1</b> HELP</span><span><b>F2</b> NEW SEARCH</span><span><b>F5</b> BROWSE</span><span><b>F8</b> NEXT SCREEN</span><span><b>F10</b> QUIT</span></div>' +
      '</div></div><div class="plate"><span>Catalogue terminal</span><i></i></div></div>';
  }

  // ---------------------------------------------------------------- 1990s
  function render1990(r) {
    const e = r.e1990;
    const items = e.hits.slice(0, 8).map(h => {
      const d = h.d, size = Math.max(1, Math.round(doc(d).ch.join(' ').length / 1024));
      return '<li ' + hit(d, '') + '><button type="button" class="it" tabindex="-1">' + esc(doc(d).t) + '</button> <span class="isc">[score ' + h.score.toFixed(3) + ']</span><br>' +
        esc(STM.cut(doc(d).ch[0], 170)) + ' ...<br><span class="iurl">http://the.book/' + esc(doc(d).id) + '.html (' + size + 'K)</span></li>';
    }).join('');
    return '<div class="win s90">' +
      '<div class="wtitle"><span>InfoBahn Index - Web Navigator</span><span aria-hidden="true">_□×</span></div>' +
      '<div class="wmenu" aria-hidden="true"><span>File</span><span>Edit</span><span>View</span><span>Go</span><span>Bookmarks</span><span>Options</span><span>Help</span></div>' +
      '<div class="wbar" aria-hidden="true"><span>Back</span><span>Forward</span><span>Home</span><span>Reload</span><span>Stop</span></div>' +
      '<div class="wloc"><span>Location:</span><span class="wurl">http://www.infobahn-index.example/cgi-bin/find?words=' + esc(encodeURIComponent(r.q.text)) + '</span></div>' +
      '<div class="wpage"><h3 class="ilogo"><span>Info</span><span>Bahn</span> <span>Index</span></h3>' +
      '<p class="itag">Your on-ramp to all ' + engine.N + ' pages of the book!</p><hr>' +
      (e.total ? '<p><b>' + e.total + '</b> pages contain at least one of your words. Best matches first.<br>Words searched, after stemming: <tt>' + esc(r.q.stems.join(' ')) + '</tt></p><ol>' + items + '</ol>'
        : '<p><b>No pages</b> contain any of your words: <tt>' + esc(r.q.stems.join(' ')) + '</tt></p><p>Check your spelling. This index matches words, not ideas.</p>') +
      '<hr><p class="ifoot">' + (e.total > 8 ? '[ Next 8 matches ] &nbsp; ' : '') + 'You are visitor <span class="cnt">' + String(engine.N * 517 + r.q.text.length).padStart(6, '0') + '</span> &nbsp; <span class="blink">NEW!</span> Now with relevance ranking</p>' +
      '</div></div>';
  }

  // ---------------------------------------------------------------- 2000s
  function render2000(r) {
    const e = r.e2000;
    const items = e.hits.slice(0, 7).map(h => {
      const d = h.d, s = engine.snippet(d, r.q.stems, 30);
      let html = '', at = 0;
      for (const [a, b] of s.marks) { html += esc(s.text.slice(at, a)) + '<b>' + esc(s.text.slice(a, b)) + '</b>'; at = b; }
      html += esc(s.text.slice(at));
      const size = Math.max(1, Math.round(doc(d).ch.join(' ').length / 1024));
      return '<li ' + hit(d, '') + '><button type="button" class="gt" tabindex="-1">' + esc(doc(d).t) + '</button>' +
        '<p class="gs">' + (s.lead ? '<b>...</b> ' : '') + html + (s.tail ? ' <b>...</b>' : '') + '</p>' +
        '<p class="gu">the.book/' + esc(doc(d).id) + ' - ' + size + 'k' + (engine.inlinks[d] ? ' <span>- linked from ' + engine.inlinks[d] + (engine.inlinks[d] === 1 ? ' other section' : ' other sections') + '</span>' : '') + '</p></li>';
    }).join('');
    return '<div class="s00"><div class="gtop"><span class="glogo">tenbluelinks<sup>BETA</sup></span><span class="gbox">' + esc(r.q.text) + '</span><span class="gbtn">Search</span></div>' +
      '<div class="gstat">Results <b>1 - ' + Math.min(7, e.total) + '</b> of <b>' + e.total + '</b> for <b>' + esc(r.q.text) + '</b>. (<b>' + (state.ms / 1000).toFixed(3) + '</b> seconds)</div>' +
      (e.suggestion ? '<p class="gdym">Did you mean: <button type="button" class="redo" data-q="' + esc(e.suggestion) + '"><b><i>' + esc(e.suggestion) + '</i></b></button></p>' : '') +
      '<div class="gcols">' + (e.total ? '<ol>' + items + '</ol>' : '<p>Your search did not match any sections. Try different words.</p>') +
      '<aside class="gads"><h4>Sponsored Links</h4><p>Nobody has bid on these words. From this decade on, an auction can also decide what you see.</p></aside></div></div>';
  }

  // ---------------------------------------------------------------- 2010s
  function excerpt(h) {
    const ch = engine.chunks[h.ci], text = doc(h.d).ch[ch.k];
    const js = (h.pairs || []).filter(p => p.j >= 0).map(p => p.j).sort((a, b) => a - b);
    const from = Math.max(0, (js.length ? js[0] : 0) - 5), to = Math.min(ch.toks.length, from + 32);
    const marks = new Set(js);
    let html = from > 0 ? '... ' : '', at = ch.toks[from] ? ch.toks[from].s : 0;
    for (let j = from; j < to; j++) {
      const t = ch.toks[j];
      html += esc(text.slice(at, t.s)) + (marks.has(j) ? '<mark>' + esc(text.slice(t.s, t.e)) + '</mark>' : esc(text.slice(t.s, t.e)));
      at = t.e;
    }
    return html + (to < ch.toks.length ? ' ...' : esc(text.slice(at)));
  }
  function render2010(r) {
    const e = r.e2010;
    const cards = e.hits.slice(0, 5).map(h => {
      const chips = (h.pairs || []).map(p => p.w === null ? '<span class="none">' + esc(p.q) + ': no match</span>'
        : STM.stem(p.w) === STM.stem(p.q) ? '<span class="same">' + esc(p.q) + ' = ' + esc(p.w) + '</span>'
          : '<span>' + esc(p.q) + ' ≈ ' + esc(p.w) + ' ' + p.s.toFixed(2) + '</span>').join('');
      return '<li ' + hit(h.d, 'pcard') + '><p class="pk">' + esc(loc(h.d)) + ' · similarity ' + h.score.toFixed(2) + '</p><h4>' + esc(doc(h.d).t) + '</h4>' +
        '<p class="px">' + excerpt(h) + '</p><p class="pm">' + chips + '</p></li>';
    }).join('');
    const panel = e.panel ? '<div class="pcard kpanel"><p class="pk">Glossary</p><h4>' + esc(e.panel.label) + '</h4><p class="px">' + esc(e.panel.def) + '</p></div>' : '';
    const hear = r.q.content.slice(0, 6).map(w => {
      const nb = engine.neighbours(w, 4);
      return nb.length ? '<li><b>' + esc(w) + '</b><span>' + nb.map(n => esc(n.w) + ' <em>' + n.s.toFixed(2) + '</em>').join(' · ') + '</span></li>'
        : '<li class="oov"><b>' + esc(w) + '</b><span>has no vector. This engine cannot see it.</span></li>';
    }).join('');
    return '<div class="s10"><div class="phone"><div class="pstat"><span>10:10</span><span>4G ▮▮▮</span></div>' +
      '<div class="pbar"><span>' + esc(r.q.text) + '</span><i></i></div><div class="ptabs"><span>All</span><span>Images</span><span>News</span></div>' +
      '<div class="pscroll">' + panel + (cards ? '<ol>' + cards + '</ol>' : '<div class="pcard"><p class="px">None of these words has a vector, so there is nothing to measure.</p></div>') + '</div></div>' +
      '<div class="hear"><h4>How this decade hears your words</h4><p>Each word is a point in space. These are its nearest neighbours among ' + vmeta.count.toLocaleString('en-GB') + ' words, with cosine similarity. A match is whatever lies close.</p><ul>' + hear + '</ul></div></div>';
  }

  // ---------------------------------------------------------------- 2020s
  function render2020(r) {
    const e = r.e2020, st = e.stages, steps = [];
    if (e.rewritten) steps.push('Rewrote the query to “' + esc(e.rewritten) + '”.');
    steps.push('Searched two ways: ' + st.sparse + ' sections by words (BM25) and ' + st.dense + ' by meaning (vectors).');
    steps.push('Fused them into ' + st.fused + ' candidates with reciprocal rank fusion. ' + e.both + ' of the best ' + st.pool + ' were found both ways.');
    steps.push('Reranked the best ' + st.pool + ' with a soft word-matching score.');
    steps.push(e.answer.length ? 'Quoted the ' + e.answer.length + ' strongest sentence' + (e.answer.length === 1 ? '' : 's') + ' from the top passages.' : 'Found no sentence that addresses the question closely enough to quote.');
    const rank = d => e.hits.findIndex(h => h.d === d) + 1;
    const ans = e.answer.length
      ? '<p class="cans">' + e.answer.map(a => esc(a.text) + '<span class="cref hit" data-d="' + a.d + '" tabindex="0" role="button" aria-label="Source ' + rank(a.d) + '">' + rank(a.d) + '</span>').join(' ') + '</p>' +
        '<p class="cnote">Every sentence is quoted from the book, so nothing here is invented, and nothing is synthesised either. No language model runs in this page.</p>'
      : '<p class="cans">The book has passages near this question, but none answers it in a sentence I can quote. The closest sections are below.</p>' +
        '<p class="cnote">A generative system would write something fluent here anyway. That is the risk this stop leaves out.</p>';
    const src = e.hits.slice(0, 6).map((h, k) => '<li ' + hit(h.d, 'csrc') + '><span class="cn">' + (k + 1) + '</span><div><b>' + esc(doc(h.d).t) + '</b><span>' + esc(loc(h.d)) + ' · ' +
      (h.sr && h.dr ? 'words #' + h.sr + ' and meaning #' + h.dr : h.sr ? 'found by words only, #' + h.sr : 'found by meaning only, #' + h.dr) + '</span></div></li>').join('');
    const live = sample && e.hits.length ? '<button type="button" class="live" id="live">Have Claude write an answer from these passages</button><div class="liveout" id="liveout" hidden></div>' : '';
    return '<div class="s20"><div class="chead"><i></i>Ask the book</div><div class="cu"><p>' + esc(r.q.text) + '</p></div>' +
      '<ol class="csteps">' + steps.map((s, k) => '<li class="ln" style="--i:' + k + '">' + s + '</li>').join('') + '</ol>' +
      '<div>' + ans + '</div>' + live + (src ? '<h4>Sources</h4><ol class="clist">' + src + '</ol>' : '') + '</div>';
  }

  async function liveAnswer() {
    const btn = $('live'), out = $('liveout'), e = state.result.e2020;
    if (!btn || !sample) return;
    btn.disabled = true;
    out.hidden = false;
    out.textContent = 'Thinking...';
    const passages = e.hits.slice(0, 4).map((h, k) => '[' + (k + 1) + '] ' + doc(h.d).t + '\n' + (h.ci >= 0 ? doc(h.d).ch[engine.chunks[h.ci].k] : doc(h.d).ch[0]).slice(0, 1200)).join('\n\n');
    const prompt = 'You are the answer stage of a retrieval-augmented search over one textbook about search systems, written for librarians.\n' +
      'Answer the question using only the numbered passages. Cite them inline as [1], [2]. If the passages do not answer the question, say so plainly rather than guessing. ' +
      'Use UK spelling and plain prose with no headings or bullets. At most 110 words.\n\nQuestion: ' + state.result.q.text + '\n\nPassages:\n' + passages;
    try {
      const res = await sample(prompt, { modelTier: 'quick', onText: u => { out.textContent = u.text; } });
      out.textContent = res.text + '\n\nWritten live by Claude from the four passages listed first below. This part is generated, so check it against them.';
      btn.textContent = 'Write it again';
      btn.disabled = false;
    } catch (err) {
      const code = err && err.code;
      out.textContent = (err && err.text ? err.text + '\n\n' : '') + (code === 'not_granted' || code === 'sampling_disabled' ? 'Live answers are switched off for this view. The quoted answer above still stands.'
        : code === 'rate_limited' ? 'Claude is busy or your usage limit was reached. Try again later.' : 'The live answer could not be written just now. Try again in a moment.');
      btn.disabled = code === 'not_granted' || code === 'sampling_disabled';
    }
  }

  const RENDER = { e1960: render1960, e1970: render1970, e1980: render1980, e1990: render1990, e2000: render2000, e2010: render2010, e2020: render2020 };

  // ---------------------------------------------------------------- chrome
  function nowText(key, r) {
    const e = r[key], N = engine.N, n = k => k + (k === 1 ? ' section' : ' sections');
    if (key === 'e1960') {
      if (e.mode === 'NONE') return 'No thesaurus term matches, so the request comes back unanswered.';
      const names = e.descriptors.map(t => t.label).join(', ');
      return 'The analyst found ' + e.descriptors.length + ' thesaurus term' + (e.descriptors.length === 1 ? '' : 's') + ' (' + names + ')' +
        (e.mode === 'OR' ? ', no section carried them all, and ORing them gives ' : ': ') + n(e.total) + ' of ' + N + '.' + (e.ignored.length ? ' The words ' + e.ignored.join(', ') + ' were dropped.' : '');
    }
    if (key === 'e1970') {
      if (e.total) return (e.total === 1 ? '1 record of ' + N + ' satisfies the statement. It prints' : e.total + ' records of ' + N + ' satisfy the statement. They print') + ' newest first, and nothing says which is best.';
      if (e.broadened) return 'No record contains all ' + e.terms.length + ' words exactly as typed. ORing them returns ' + e.broadened.list.length + ' of ' + N + ': nothing, or a flood.';
      return 'No record satisfies the statement.';
    }
    if (key === 'e1980') return e.total ? (e.total === 1 ? '1 record carries' : e.total + ' records carry') + ' all of your words in the title, chapter or subject headings, filed alphabetically.' : 'No catalogue record carries all of your words, so the catalogue shows where your entry would file.';
    if (key === 'e1990') return e.total ? n(e.total) + ' of ' + N + ' share at least one word stem with you. The closest by cosine comes first.' : 'No section shares a single word with you.';
    if (key === 'e2000') return (e.total ? n(e.total) + ' scored by BM25 and link analysis.' : 'No section shares a word with you.') + (e.suggestion ? ' The engine suggests “' + e.suggestion + '”.' : '');
    if (key === 'e2010') return e.total ? 'All ' + N + ' sections receive a score, because every point has a distance.' + (e.oov.length ? ' No vector for: ' + e.oov.join(', ') + '.' : '') : 'None of your words has a vector.';
    return e.stages.sparse + ' by words and ' + e.stages.dense + ' by meaning became ' + e.stages.fused + ' candidates, ' + e.stages.pool + ' reranked, ' + e.answer.length + ' quoted sentence' + (e.answer.length === 1 ? '' : 's') + '.';
  }

  function renderPlacard() {
    const e = eraOf(state.era), ch = corpus.chapters.find(x => x.id === e.book);
    const val = v => (typeof v === 'function' ? v() : v);
    $('placard').innerHTML = '<p class="decade">' + e.yr + '</p><h2>' + esc(e.title) + '</h2>' +
      '<p class="who"><span>Who decides what you see</span><strong>' + esc(e.who) + '</strong></p>' +
      '<dl class="rules"><dt>Reads</dt><dd>' + esc(val(e.reads)) + '</dd><dt>Admits</dt><dd>' + esc(e.admits) + '</dd><dt>Orders</dt><dd>' + esc(e.orders) + '</dd></dl>' +
      '<p class="now"><span>On this query</span>' + esc(nowText(e.key, state.result)) + '</p>' +
      '<p class="story">' + e.story() + '</p>' +
      '<p class="gl"><b>Gained</b><span>' + esc(e.gained) + '</span><b>Missing</b><span>' + esc(e.missing) + '</span></p>' +
      (ch ? '<p class="src">In the book: <a href="' + corpus.book.url + '#' + ch.id + '" target="_blank" rel="noopener">' + esc((ch.n ? ch.n + ', ' : '') + ch.t) + '</a></p>' : '');
  }

  function renderDial() {
    const r = state.result;
    for (const b of $('eras').querySelectorAll('.era')) {
      const key = b.dataset.era, rk = b.querySelector('.rk');
      b.setAttribute('aria-pressed', key === state.era ? 'true' : 'false');
      if (state.track < 0) { rk.className = 'rk'; rk.textContent = r[key].total ? r[key].total + ' found' : 'nothing'; continue; }
      const n = engine.rankOf(r, key, state.track);
      const broadened = key === 'e1970' && !r.e1970.total && r.e1970.broadened;
      const total = broadened ? r.e1970.broadened.list.length : r[key].total;
      rk.className = 'rk ' + (n === 0 ? 'miss' : n === 1 ? 'top' : 'hit');
      rk.textContent = n === 0 ? 'not found' : '#' + n + ' of ' + total;
      rk.title = n === 0 ? 'This decade did not retrieve the followed section.' : 'Position ' + n + ' of ' + total + (key < 'e1990' ? ' in an unranked list' : '') + (broadened ? ', after broadening to OR' : '') + '.';
    }
    const f = $('follow');
    if (state.track < 0) f.textContent = 'No decade retrieved anything for this query.';
    else f.innerHTML = 'Following <b>' + esc(doc(state.track).t) + '</b> (' + esc(loc(state.track)) + '), ' + (state.pinned ? 'your pick' : 'the 2020s pipeline’s first choice') +
      '. Each decade below shows where it ranked that section. Click any result to follow it instead. <a href="' + url(state.track) + '" target="_blank" rel="noopener">Read it in the book</a>';
  }

  function renderScreen() {
    const s = $('screen');
    s.innerHTML = RENDER[state.era](state.result);
    s.scrollTop = 0;
    s.setAttribute('aria-label', eraOf(state.era).yr + ' search screen');
  }
  function renderAll() { renderDial(); renderScreen(); renderPlacard(); }

  function setEra(key, user) {
    if (user) stopTour();
    state.era = key;
    renderAll();
  }
  function search(q, user) {
    if (user) stopTour();
    q = q.trim();
    if (!q) return;
    state.query = q;
    $('q').value = q;
    const t0 = performance.now();
    state.result = engine.run(q);
    state.ms = performance.now() - t0;
    state.track = state.result.track;
    state.pinned = false;
    for (const b of $('chips').querySelectorAll('.chip')) b.setAttribute('aria-pressed', b.dataset.q === q ? 'true' : 'false');
    renderAll();
  }
  function follow(d) {
    stopTour();
    state.track = d;
    state.pinned = true;
    renderDial();
    for (const el of $('screen').querySelectorAll('[data-d]')) el.classList.toggle('tracked', +el.dataset.d === d);
  }

  const DWELL = { e1960: 5600, e1970: 6600, e1980: 4400, e1990: 4400, e2000: 4600, e2010: 5200, e2020: 6500 };
  function stopTour() {
    if (!state.touring) return;
    state.touring = false;
    clearTimeout(state.timer);
    $('play').textContent = 'Play the seven decades';
  }
  function startTour(from) {
    state.touring = true;
    $('play').textContent = 'Pause the tour';
    let i = from || 0;
    const step = () => {
      if (!state.touring) return;
      state.era = ERAS[i].key;
      renderAll();
      state.timer = setTimeout(() => { i++; if (i >= ERAS.length) { stopTour(); return; } step(); }, DWELL[ERAS[i].key]);
    };
    step();
  }

  function init() {
    corpus = JSON.parse($('stm-corpus').textContent);
    vmeta = JSON.parse($('stm-vmeta').textContent);
    engine = STM.create(corpus, vmeta, $('stm-vectors').textContent.trim());
    state.links = corpus.docs.reduce((a, d) => a + (d.ln ? d.ln.length : 0), 0);

    $('eras').innerHTML = ERAS.map(e => '<li><button type="button" class="era" data-era="' + e.key + '" aria-pressed="false"><span class="yr">' + e.yr + '</span><span class="nm">' + esc(e.nm) + '</span><span class="rk"></span></button></li>').join('');
    $('chips').insertAdjacentHTML('beforeend', PRESETS.map(p => '<button type="button" class="chip" data-q="' + esc(p.q) + '" aria-pressed="false"><b>' + esc(p.tag) + '</b>' + esc(p.q) + '</button>').join(''));
    REFS.book = ['Tay 2026', 'Tay, A. C. H. (2026). <i>How search decides what you see: A librarian’s guide to Boolean search, BM25, embeddings, reranking, and the retrieval pipelines behind hybrid and agentic search</i> (Version ' + esc(corpus.book.version) + '). The collection searched on this page. CC BY 4.0.', 'https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/'];
    $('reflist').innerHTML = Object.keys(REFS).map(k => REFS[k]).sort((a, b) => a[1].localeCompare(b[1])).map(x => '<li>' + x[1] + ' <a href="' + x[2] + '" target="_blank" rel="noopener">' + esc(x[2].replace('https://', '')) + '</a></li>').join('');
    $('buildnote').textContent = 'This page indexed ' + engine.N + ' sections, ' + engine.chunks.length + ' paragraphs, ' + state.links + ' cross-references and ' + engine.rawVocab.length.toLocaleString('en-GB') +
      ' distinct words in ' + engine.buildMs + ' ms on your device, and holds ' + vmeta.count.toLocaleString('en-GB') + ' word vectors of ' + vmeta.dims + ' dimensions. The vectors derive from GloVe (Public Domain Dedication and License) through the wink-embeddings-sg-100d package (MIT), reduced from 100 dimensions; ' + vmeta.induced + ' book-specific words were placed from their context in the book, after ' + REFS.khodak2018[0].replace('&amp;', '&') + '.';

    $('eras').addEventListener('click', ev => { const b = ev.target.closest('.era'); if (b) setEra(b.dataset.era, true); });
    $('eras').addEventListener('keydown', ev => {
      if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
      const i = ERAS.findIndex(e => e.key === state.era), j = Math.max(0, Math.min(ERAS.length - 1, i + (ev.key === 'ArrowRight' ? 1 : -1)));
      setEra(ERAS[j].key, true);
      $('eras').querySelector('[data-era="' + ERAS[j].key + '"]').focus();
      ev.preventDefault();
    });
    $('chips').addEventListener('click', ev => { const b = ev.target.closest('.chip'); if (b) search(b.dataset.q, true); });
    $('qform').addEventListener('submit', ev => { ev.preventDefault(); search($('q').value, true); });
    $('play').addEventListener('click', () => { if (state.touring) stopTour(); else startTour(state.era === 'e2020' ? 0 : ERAS.findIndex(e => e.key === state.era)); });
    const act = ev => {
      const t = ev.target;
      if (t.closest('#live')) { liveAnswer(); return; }
      const redo = t.closest('.redo, .sug');
      if (redo) { search(redo.dataset.q, true); return; }
      const h = t.closest('[data-d]');
      if (h) follow(+h.dataset.d);
    };
    $('screen').addEventListener('click', act);
    $('screen').addEventListener('keydown', ev => { if ((ev.key === 'Enter' || ev.key === ' ') && ev.target.matches('[data-d]')) { ev.preventDefault(); act(ev); } });
    $('q').addEventListener('input', stopTour);
    $('q').addEventListener('focus', stopTour);

    search(state.query, false);
    if (window.claude && typeof window.claude.use === 'function') {
      window.claude.use('sample').then(fn => { if (fn) { sample = fn; if (state.era === 'e2020') renderScreen(); } }).catch(() => {});
    }
    const still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!still && !/[?&#]still\b/.test(location.search + location.hash)) startTour(0);
    window.STMApp = { state, engine, search, setEra, startTour, stopTour, follow };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(init, 30));
  else setTimeout(init, 30);
})();
