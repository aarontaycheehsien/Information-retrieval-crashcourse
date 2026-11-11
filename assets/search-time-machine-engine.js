/* Search Time Machine engine.
 *
 * Seven generations of retrieval over one small collection (the sections of
 * "How Search Decides What You See"). Everything runs in the browser; there is
 * no server and no language model. The same file is loaded by Node for
 * tools/check-search-time-machine.mjs.
 *
 * Method sources, by era:
 *   1960s  coordinate indexing with a controlled vocabulary (Taube et al. 1952)
 *   1970s  Boolean set retrieval over an inverted file
 *   1980s  keyword-in-record catalogue search with an alphabetical browse
 *   1990s  tf-idf vector-space ranking (Sparck Jones 1972; Salton et al. 1975)
 *   2000s  BM25 (Robertson et al. 1995) with field weights, a link-analysis
 *          prior (Brin & Page 1998) and query-biased snippets (Tombros &
 *          Sanderson 1998)
 *   2010s  dense retrieval over averaged static word vectors (Pennington et
 *          al. 2014)
 *   2020s  hybrid retrieval fused with reciprocal rank fusion (Cormack et al.
 *          2009), a soft-match reranker and an extractive answer
 * Stemming is Porter (1980).
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.STM = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const STOP = new Set(('a about above after again against all am an and any are arent as at be because been before ' +
    'being below between both but by can cannot cant could couldnt did didnt do does doesnt doing dont down during each ' +
    'few for from further had hadnt has hasnt have havent having he her here hers herself him himself his how i if im in ' +
    'into is isnt it its itself ive just let me more most my myself no nor not of off on once only or other ought our ours ' +
    'ourselves out over own same she should shouldnt so some such than that thats the their theirs them themselves then ' +
    'there these they this those through to too under until up very was wasnt we were werent what whats when where which ' +
    'while who whom why will with wont would wouldnt you your youre yours yourself yourselves s t ll re ve d m').split(' '));

  // ---- text analysis -------------------------------------------------------
  const TOKEN_RE = /[A-Za-z0-9À-ɏ]+(?:['’][A-Za-zÀ-ɏ]+)*/g;
  function fold(t) {
    return t.toLowerCase().replace(/['’]/g, '').normalize('NFD').replace(/[̀-ͯ]/g, '');
  }
  function tokenize(text) {
    const out = [];
    let m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(text))) out.push({ w: fold(m[0]), s: m.index, e: m.index + m[0].length });
    return out;
  }
  function words(text) { return tokenize(text).map(t => t.w); }

  // Porter (1980) suffix stripping.
  const step2list = { ational: 'ate', tional: 'tion', enci: 'ence', anci: 'ance', izer: 'ize', bli: 'ble', alli: 'al',
    entli: 'ent', eli: 'e', ousli: 'ous', ization: 'ize', ation: 'ate', ator: 'ate', alism: 'al', iveness: 'ive',
    fulness: 'ful', ousness: 'ous', aliti: 'al', iviti: 'ive', biliti: 'ble', logi: 'log' };
  const step3list = { icate: 'ic', ative: '', alize: 'al', iciti: 'ic', ical: 'ic', ful: '', ness: '' };
  const cC = '[^aeiou]', vV = '[aeiouy]', CC = cC + '[^aeiouy]*', VV = vV + '[aeiou]*';
  const mgr0 = new RegExp('^(' + CC + ')?' + VV + CC);
  const meq1 = new RegExp('^(' + CC + ')?' + VV + CC + '(' + VV + ')?$');
  const mgr1 = new RegExp('^(' + CC + ')?' + VV + CC + VV + CC);
  const sV = new RegExp('^(' + CC + ')?' + vV);
  const reDouble = /([^aeiouylsz])\1$/;
  const reCvc = new RegExp('^' + CC + vV + '[^aeiouwxy]$');
  function porter(w) {
    let fp, st;
    const first = w.charAt(0);
    if (first === 'y') w = 'Y' + w.substr(1);
    if (/^(.+?)(ss|i)es$/.test(w)) w = w.replace(/^(.+?)(ss|i)es$/, '$1$2');
    else if (/^(.+?)([^s])s$/.test(w)) w = w.replace(/^(.+?)([^s])s$/, '$1$2');
    if ((fp = /^(.+?)eed$/.exec(w))) { if (mgr0.test(fp[1])) w = w.slice(0, -1); }
    else if ((fp = /^(.+?)(ed|ing)$/.exec(w))) {
      st = fp[1];
      if (sV.test(st)) {
        w = st;
        if (/(at|bl|iz)$/.test(w)) w += 'e';
        else if (reDouble.test(w)) w = w.slice(0, -1);
        else if (reCvc.test(w)) w += 'e';
      }
    }
    if ((fp = /^(.+?)y$/.exec(w))) { if (sV.test(fp[1])) w = fp[1] + 'i'; }
    if ((fp = /^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$/.exec(w))) {
      if (mgr0.test(fp[1])) w = fp[1] + step2list[fp[2]];
    }
    if ((fp = /^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$/.exec(w))) {
      if (mgr0.test(fp[1])) w = fp[1] + step3list[fp[2]];
    }
    if ((fp = /^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$/.exec(w))) {
      if (mgr1.test(fp[1])) w = fp[1];
    } else if ((fp = /^(.+?)(s|t)(ion)$/.exec(w))) {
      st = fp[1] + fp[2];
      if (mgr1.test(st)) w = st;
    }
    if ((fp = /^(.+?)e$/.exec(w))) {
      st = fp[1];
      if (mgr1.test(st) || (meq1.test(st) && !reCvc.test(st))) w = st;
    }
    if (/ll$/.test(w) && mgr1.test(w)) w = w.slice(0, -1);
    if (first === 'y') w = 'y' + w.substr(1);
    return w;
  }
  const stemCache = new Map();
  function stem(w) {
    if (w.length < 3 || /\d/.test(w)) return w;
    let s = stemCache.get(w);
    if (s === undefined) { s = porter(w); stemCache.set(w, s); }
    return s;
  }

  function plural(w) {
    if (w.length > 4 && w.endsWith('ies')) return w.slice(0, -3) + 'y';
    if (w.length > 4 && /(ss|x|ch|sh)es$/.test(w)) return w.slice(0, -2);
    if (w.length > 3 && w.endsWith('s') && !w.endsWith('ss') && !w.endsWith('us') && !w.endsWith('is')) return w.slice(0, -1);
    return w;
  }

  const UK_US = [['isation', 'ization'], ['isations', 'izations'], ['ising', 'izing'], ['ised', 'ized'], ['ises', 'izes'],
    ['ise', 'ize'], ['iser', 'izer'], ['ours', 'ors'], ['our', 'or'], ['ogue', 'og'], ['tre', 'ter'], ['lled', 'led'],
    ['lling', 'ling'], ['yse', 'yze'], ['ysed', 'yzed']];

  function editDistance(a, b, max) {
    const la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    let prev2 = null, prev = new Array(lb + 1), cur = new Array(lb + 1);
    for (let j = 0; j <= lb; j++) prev[j] = j;
    for (let i = 1; i <= la; i++) {
      cur[0] = i;
      let best = cur[0];
      for (let j = 1; j <= lb; j++) {
        const cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        let v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (prev2 && i > 1 && j > 1 && a.charCodeAt(i - 1) === b.charCodeAt(j - 2) && a.charCodeAt(i - 2) === b.charCodeAt(j - 1)) {
          v = Math.min(v, prev2[j - 2] + 1);
        }
        cur[j] = v;
        if (v < best) best = v;
      }
      if (best > max) return max + 1;
      prev2 = prev; prev = cur; cur = new Array(lb + 1);
    }
    return prev[lb];
  }

  function splitSentences(text) {
    const out = [];
    let start = 0;
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      if ((ch === '.' || ch === '?' || ch === '!') && i + 2 < text.length && text[i + 1] === ' ') {
        const next = text[i + 2];
        const before = text.slice(Math.max(0, i - 5), i);
        if (/[A-Z“"(\[]/.test(next) && !/(?:^|[\s(])(?:e\.g|i\.e|cf|vs|al|Fig|No|pp)$/.test(before)) {
          out.push(text.slice(start, i + 1).trim());
          start = i + 2;
        }
      }
    }
    const tail = text.slice(start).trim();
    if (tail) out.push(tail);
    return out;
  }

  // ---- engine --------------------------------------------------------------
  class Engine {
    constructor(corpus, vmeta, vbytes) {
      const t0 = Date.now();
      this.corpus = corpus;
      this.docs = corpus.docs;
      this.chapters = corpus.chapters;
      this.N = this.docs.length;
      this._analyse();
      this._thesaurus();
      this._pagerank();
      this._vectors(vmeta, vbytes);
      this.buildMs = Date.now() - t0;
    }

    _analyse() {
      const N = this.N;
      this.raw = new Map();          // exact word -> sorted doc ids (full text)
      this.cat = new Map();          // exact word -> doc ids (catalogue record only)
      this.post = new Map();         // stem -> Map(doc -> [bodyTf, titleTf])
      this.wordFreq = new Map();     // exact word -> collection frequency
      this.len = new Float32Array(N);
      this.chunks = [];              // {doc, k, toks, rows(Int32Array later)}
      this.docChunks = [];
      this.docToks = [];             // per doc: [title toks, ...chunk toks, extra toks] as word arrays
      this.stemSeq = [];             // per doc: ' stem stem stem ' string for phrase lookups
      this.termSeq = [];             // same with plural folding only, for glossary terms
      const addRaw = (map, w, d) => {
        let a = map.get(w);
        if (!a) map.set(w, (a = []));
        if (a[a.length - 1] !== d) a.push(d);
      };
      for (let d = 0; d < N; d++) {
        const doc = this.docs[d];
        const chapter = this.chapters[doc.c];
        const titleW = words(doc.t), parentW = words(doc.pt || ''), chapW = words(chapter.t);
        const extraW = words(doc.x || '');
        const seqs = [titleW];
        const tfBody = new Map(), tfTitle = new Map();
        const bump = (m, s, n) => m.set(s, (m.get(s) || 0) + n);
        for (const w of titleW) { addRaw(this.raw, w, d); addRaw(this.cat, w, d); if (!STOP.has(w)) bump(tfTitle, stem(w), 1); }
        for (const w of parentW) { addRaw(this.cat, w, d); if (!STOP.has(w)) bump(tfTitle, stem(w), 0.5); }
        for (const w of chapW) { addRaw(this.cat, w, d); if (!STOP.has(w)) bump(tfTitle, stem(w), 0.35); }
        const mine = [];
        let length = 0;
        doc.ch.forEach((text, k) => {
          const toks = tokenize(text);
          const ws = toks.map(t => t.w);
          seqs.push(ws);
          for (const w of ws) {
            addRaw(this.raw, w, d);
            this.wordFreq.set(w, (this.wordFreq.get(w) || 0) + 1);
            if (!STOP.has(w)) { bump(tfBody, stem(w), 1); length++; }
          }
          mine.push(this.chunks.length);
          this.chunks.push({ doc: d, k, toks, ws });
        });
        for (const w of extraW) {
          addRaw(this.raw, w, d);
          if (!STOP.has(w)) { bump(tfBody, stem(w), 0.5); length += 0.5; }
        }
        seqs.push(extraW);
        this.docChunks.push(mine);
        this.docToks.push(seqs);
        this.len[d] = length;
        this.stemSeq.push(seqs.map(s => ' ' + s.map(stem).join(' ') + ' ').join('|'));
        this.termSeq.push(seqs.map(s => ' ' + s.map(plural).join(' ') + ' ').join('|'));
        const stems = new Set([...tfBody.keys(), ...tfTitle.keys()]);
        for (const s of stems) {
          let m = this.post.get(s);
          if (!m) this.post.set(s, (m = new Map()));
          m.set(d, [tfBody.get(s) || 0, tfTitle.get(s) || 0]);
        }
      }
      this.avgLen = this.len.reduce((a, b) => a + b, 0) / N;
      this.idf = s => { const m = this.post.get(s); const df = m ? m.size : 0; return Math.log(1 + (N - df + 0.5) / (df + 0.5)); };
      // tf-idf document norms for the 1990s cosine
      this.norm = new Float32Array(N);
      for (const [s, m] of this.post) {
        const idf = Math.log(N / m.size) + 0.01;
        for (const [d, tf] of m) { const w = (1 + Math.log(tf[0] + tf[1] + 1e-9 < 1 ? 1 : tf[0] + tf[1])) * idf; this.norm[d] += w * w; }
      }
      for (let d = 0; d < N; d++) this.norm[d] = Math.sqrt(this.norm[d]) || 1;
      this.rawVocab = [...this.raw.keys()].sort();
      this.titleOrder = this.docs.map((doc, i) => i).sort((a, b) => this._sortKey(a).localeCompare(this._sortKey(b)));
    }

    _sortKey(d) { return this.docs[d].t.toUpperCase().replace(/^(THE|A|AN) /, '').replace(/[^A-Z0-9 ]/g, ''); }

    _thesaurus() {
      // The glossary is the controlled vocabulary: 1960s descriptors, 1980s
      // subject headings and the 2010s knowledge panel.
      this.terms = this.corpus.glossary.map((g, i) => {
        const variants = new Set();
        const main = g.label.replace(/\(([^)]*)\)/g, ' / $1 ');
        for (const part of main.split('/').concat(g.aliases || [])) {
          const ws = words(part).filter(w => w.length);
          if (ws.length) variants.add(ws.map(plural).join(' '));
        }
        const head = g.label.replace(/\s*\(.*$/, '').replace(/\s*\/.*$/, '').trim();
        return { i, id: g.id, label: g.label, head, def: g.def, targets: g.targets || [], related: g.related || [],
          variants: [...variants].sort((a, b) => b.length - a.length), docs: [] };
      });
      this.docTerms = this.docs.map(() => []);
      for (let d = 0; d < this.N; d++) {
        const seq = this.termSeq[d];
        const titleSeq = seq.split('|')[0];
        const found = [];
        for (const term of this.terms) {
          let count = 0, inTitle = false;
          for (const v of term.variants) {
            const needle = ' ' + v + ' ';
            let at = seq.indexOf(needle);
            while (at !== -1) { count++; at = seq.indexOf(needle, at + needle.length - 1); }
            if (titleSeq.indexOf(needle) !== -1) inTitle = true;
          }
          const major = inTitle || term.targets.indexOf(d) !== -1;
          if (major || count >= 2) found.push({ t: term.i, count, major });
        }
        found.sort((a, b) => (b.major - a.major) || (b.count - a.count));
        const kept = found.slice(0, 10);
        this.docTerms[d] = kept;
        for (const f of kept) {
          this.terms[f.t].docs.push(d);
          for (const w of words(this.terms[f.t].head)) {
            let a = this.cat.get(w);
            if (!a) this.cat.set(w, (a = []));
            if (a.indexOf(d) === -1) a.push(d);
          }
        }
      }
      for (const a of this.cat.values()) a.sort((x, y) => x - y);
    }

    _pagerank() {
      const N = this.N, out = this.docs.map(d => d.ln || []);
      let pr = new Float64Array(N).fill(1 / N);
      this.inlinks = new Int32Array(N);
      for (const l of out) for (const j of l) this.inlinks[j]++;
      for (let it = 0; it < 50; it++) {
        const next = new Float64Array(N).fill(0);
        let dangling = 0;
        for (let i = 0; i < N; i++) {
          if (!out[i].length) { dangling += pr[i]; continue; }
          const share = pr[i] / out[i].length;
          for (const j of out[i]) next[j] += share;
        }
        for (let i = 0; i < N; i++) next[i] = 0.15 / N + 0.85 * (next[i] + dangling / N);
        pr = next;
      }
      const logs = Array.from(pr, v => Math.log(v));
      const lo = Math.min(...logs), hi = Math.max(...logs);
      this.pagerank = pr;
      this.prn = Float32Array.from(logs, v => (v - lo) / (hi - lo || 1));
    }

    _vectors(vmeta, vbytes) {
      this.hasVectors = !!(vmeta && vbytes && vbytes.length);
      if (!this.hasVectors) return;
      const D = (this.D = vmeta.dims), V = (this.V = vmeta.words.length);
      this.vwords = vmeta.words;
      this.vix = new Map();
      for (let i = 0; i < V; i++) this.vix.set(vmeta.words[i], i);
      const M = (this.M = new Float32Array(V * D));
      for (let i = 0; i < V; i++) {
        let n = 0;
        for (let j = 0; j < D; j++) { const x = vbytes[i * D + j]; const s = x > 127 ? x - 256 : x; M[i * D + j] = s; n += s * s; }
        n = Math.sqrt(n) || 1;
        for (let j = 0; j < D; j++) M[i * D + j] /= n;
      }
      // chunk-level idf for word weighting
      const nC = this.chunks.length, cdf = new Map();
      for (const c of this.chunks) for (const w of new Set(c.ws)) cdf.set(w, (cdf.get(w) || 0) + 1);
      this.widf = w => Math.log(1 + nC / (cdf.get(w) || 0.5));
      // chunk and title vectors: idf-weighted mean, centred, unit length
      const sum = new Float32Array(D);
      const build = ws => {
        const v = new Float32Array(D);
        let any = false;
        for (const w of ws) {
          if (STOP.has(w)) continue;
          const r = this.row(w);
          if (r < 0) continue;
          const g = this.widf(w), o = r * D;
          for (let j = 0; j < D; j++) v[j] += g * M[o + j];
          any = true;
        }
        return any ? unit(v) : null;
      };
      for (const c of this.chunks) {
        c.rows = Int32Array.from(c.ws, w => (STOP.has(w) ? -1 : this.row(w)));
        c.vec = build(c.ws);
        if (c.vec) for (let j = 0; j < D; j++) sum[j] += c.vec[j];
      }
      this.mu = sum.map(x => x / nC);
      const centre = v => { if (!v) return null; const o = new Float32Array(D); for (let j = 0; j < D; j++) o[j] = v[j] - this.mu[j]; return unit(o); };
      for (const c of this.chunks) c.vec = centre(c.vec);
      this.titleVec = this.docs.map(doc => centre(build(words(doc.t + ' ' + (doc.pt || '')))));
      this._embed = ws => centre(build(ws));
    }

    row(w) {
      let r = this.vix.get(w);
      if (r !== undefined) return r;
      if (w.length > 3 && w.endsWith('s')) { r = this.vix.get(w.slice(0, -1)); if (r !== undefined) return r; }
      for (const [uk, us] of UK_US) {
        if (w.endsWith(uk)) { r = this.vix.get(w.slice(0, -uk.length) + us); if (r !== undefined) return r; }
        if (w.endsWith(us)) { r = this.vix.get(w.slice(0, -us.length) + uk); if (r !== undefined) return r; }
      }
      return -1;
    }

    simRow(r) {
      const D = this.D, V = this.V, M = this.M, out = new Float32Array(V), o = r * D;
      for (let i = 0; i < V; i++) {
        let s = 0;
        const p = i * D;
        for (let j = 0; j < D; j++) s += M[o + j] * M[p + j];
        out[i] = s;
      }
      return out;
    }

    neighbours(word, k) {
      const r = this.hasVectors ? this.row(word) : -1;
      if (r < 0) return [];
      const sims = this.simRow(r), st = stem(word), best = [];
      for (let i = 0; i < this.V; i++) {
        if (i === r || stem(this.vwords[i]) === st || /^\d+$/.test(this.vwords[i])) continue;
        if (best.length < k || sims[i] > best[best.length - 1].s) {
          best.push({ w: this.vwords[i], s: sims[i] });
          best.sort((a, b) => b.s - a.s);
          if (best.length > k) best.pop();
        }
      }
      return best;
    }

    // ---- query analysis shared by the eras ---------------------------------
    analyse(query) {
      const toks = tokenize(query);
      const all = toks.map(t => t.w);
      const content = [];
      for (const w of all) if (!STOP.has(w) && content.indexOf(w) === -1) content.push(w);
      const stems = [];
      for (const w of content) { const s = stem(w); if (stems.indexOf(s) === -1) stems.push(s); }
      return { text: query, all, content, stems };
    }

    matchTerms(q) {
      // Longest-first phrase match of glossary terms against the stemmed query.
      const seq = ' ' + q.all.map(plural).join(' ') + ' ';
      const hits = [];
      const taken = [];
      const cands = [];
      for (const term of this.terms) for (const v of term.variants) cands.push({ term, v });
      cands.sort((a, b) => b.v.length - a.v.length);
      for (const { term, v } of cands) {
        const at = seq.indexOf(' ' + v + ' ');
        if (at === -1) continue;
        const span = [at, at + v.length + 1];
        if (taken.some(t => span[0] < t[1] && t[0] < span[1])) continue;
        if (hits.some(h => h.term === term)) continue;
        taken.push(span);
        hits.push({ term, at, stems: v.split(' ') });  // plural-folded words
      }
      hits.sort((a, b) => a.at - b.at);
      return hits;
    }

    // ---- 1960s: batch search on index terms --------------------------------
    era1960(q) {
      const matched = this.matchTerms(q);
      const covered = new Set();
      for (const m of matched) for (const s of m.stems) covered.add(s);
      const ignored = q.content.filter(w => !covered.has(plural(w)));
      let hits = [], mode = 'NONE';
      if (matched.length) {
        const sets = matched.map(m => new Set(m.term.docs));
        hits = [...sets[0]].filter(d => sets.every(s => s.has(d))).sort((a, b) => a - b);
        mode = 'AND';
        if (!hits.length && matched.length > 1) {
          const u = new Set();
          for (const s of sets) for (const d of s) u.add(d);
          hits = [...u].sort((a, b) => a - b);
          mode = 'OR';
        }
      }
      return { key: 'e1960', list: hits, total: hits.length, mode, ignored,
        descriptors: matched.map(m => ({ label: m.term.head, id: m.term.id, postings: m.term.docs.length })) };
    }

    // ---- 1970s: online Boolean on the full text ----------------------------
    _termDocs(spec) {
      const N = this.N, bits = new Uint8Array(N);
      if (spec.type === 'word') {
        for (const d of this.raw.get(spec.w) || []) bits[d] = 1;
      } else if (spec.type === 'trunc') {
        const p = spec.w;
        let lo = 0, hi = this.rawVocab.length;
        while (lo < hi) { const mid = (lo + hi) >> 1; if (this.rawVocab[mid] < p) lo = mid + 1; else hi = mid; }
        for (let i = lo; i < this.rawVocab.length && this.rawVocab[i].startsWith(p); i++) {
          for (const d of this.raw.get(this.rawVocab[i])) bits[d] = 1;
        }
      } else if (spec.type === 'phrase') {
        const ws = spec.ws;
        if (!ws.length) return bits;
        let cand = (this.raw.get(ws[0]) || []).slice();
        for (const w of ws.slice(1)) { const s = new Set(this.raw.get(w) || []); cand = cand.filter(d => s.has(d)); }
        for (const d of cand) {
          outer: for (const seq of this.docToks[d]) {
            for (let i = 0; i + ws.length <= seq.length; i++) {
              let ok = true;
              for (let j = 0; j < ws.length; j++) if (seq[i + j] !== ws[j]) { ok = false; break; }
              if (ok) { bits[d] = 1; break outer; }
            }
          }
        }
      }
      return bits;
    }

    parseBoolean(text) {
      const lex = [];
      const re = /"([^"]*)"|“([^”]*)”|\(|\)|[A-Za-z0-9À-ɏ'’-]+[*?]?/g;
      let m;
      while ((m = re.exec(text))) {
        const t = m[0];
        if (t === '(' || t === ')') lex.push({ k: t });
        else if (m[1] !== undefined || m[2] !== undefined) lex.push({ k: 'term', spec: { type: 'phrase', ws: words(m[1] !== undefined ? m[1] : m[2]) }, label: '"' + (m[1] !== undefined ? m[1] : m[2]).toUpperCase() + '"' });
        else if (t === 'AND' || t === 'OR' || t === 'NOT') lex.push({ k: t });
        else {
          const trunc = /[*?]$/.test(t);
          for (const w of words(trunc ? t.slice(0, -1) : t)) {
            if (STOP.has(w) && !trunc) continue;
            lex.push({ k: 'term', spec: { type: trunc ? 'trunc' : 'word', w }, label: w.toUpperCase() + (trunc ? '?' : '') });
          }
        }
      }
      let pos = 0;
      const leaves = [];
      const peek = () => lex[pos];
      const primary = () => {
        const t = peek();
        if (!t) return null;
        if (t.k === '(') { pos++; const e = orExpr(); if (peek() && peek().k === ')') pos++; return e ? { op: 'grp', a: e } : null; }
        if (t.k === 'term') { pos++; leaves.push(t); return { op: 'term', leaf: t }; }
        return null;
      };
      const notExpr = () => {
        if (peek() && peek().k === 'NOT') { pos++; const a = notExpr(); return a ? { op: 'NOT', a } : null; }
        return primary();
      };
      const andExpr = () => {
        let left = notExpr();
        for (;;) {
          const t = peek();
          if (!t || t.k === 'OR' || t.k === ')') break;
          if (t.k === 'AND') pos++;
          const right = notExpr();
          if (!right) break;
          left = left ? { op: 'AND', a: left, b: right } : right;
        }
        return left;
      };
      const orExpr = () => {
        let left = andExpr();
        while (peek() && peek().k === 'OR') { pos++; const right = andExpr(); if (!right) break; left = left ? { op: 'OR', a: left, b: right } : right; }
        return left;
      };
      const tree = orExpr();
      return { tree, leaves };
    }

    _evalBool(node) {
      const N = this.N;
      if (node.op === 'term') return node.leaf.bits || (node.leaf.bits = this._termDocs(node.leaf.spec));
      if (node.op === 'grp') return this._evalBool(node.a);
      const out = new Uint8Array(N);
      if (node.op === 'NOT') { const a = this._evalBool(node.a); for (let i = 0; i < N; i++) out[i] = a[i] ? 0 : 1; return out; }
      const a = this._evalBool(node.a), b = this._evalBool(node.b);
      if (node.op === 'AND') for (let i = 0; i < N; i++) out[i] = a[i] & b[i];
      else for (let i = 0; i < N; i++) out[i] = a[i] | b[i];
      return out;
    }

    _showBool(node, top) {
      if (node.op === 'term') return node.leaf.label;
      if (node.op === 'grp') return '(' + this._showBool(node.a) + ')';
      if (node.op === 'NOT') return 'NOT ' + this._showBool(node.a);
      return this._showBool(node.a) + ' ' + node.op + ' ' + this._showBool(node.b);
    }

    era1970(q) {
      const text = q.text.trim();
      const explicit = /\b(AND|OR|NOT)\b/.test(text) || /["“()]/.test(text) || /[A-Za-z0-9][*]/.test(text) || /[A-Za-z0-9]\?(?=\s*\S)/.test(text);
      const source = explicit ? text : text.replace(/[?!.]+\s*$/, '');
      const { tree, leaves } = this.parseBoolean(source);
      const bitsToList = bits => { const l = []; for (let i = this.N - 1; i >= 0; i--) if (bits[i]) l.push(i); return l; };
      if (!tree) return { key: 'e1970', list: [], total: 0, explicit, statement: '', terms: [], broadened: null };
      const list = bitsToList(this._evalBool(tree));
      const seen = new Set(), terms = [];
      for (const leaf of leaves) {
        if (seen.has(leaf.label)) continue;
        seen.add(leaf.label);
        let n = 0;
        const b = leaf.bits || this._termDocs(leaf.spec);
        for (let i = 0; i < this.N; i++) n += b[i];
        terms.push({ label: leaf.label, postings: n });
      }
      let broadened = null;
      if (!list.length && !explicit && leaves.length > 1) {
        const u = new Uint8Array(this.N);
        for (const leaf of leaves) { const b = leaf.bits; for (let i = 0; i < this.N; i++) u[i] |= b[i]; }
        broadened = { statement: terms.map(t => t.label).join(' OR '), list: bitsToList(u) };
      }
      return { key: 'e1970', list, total: list.length, explicit, statement: this._showBool(tree, true), terms, broadened };
    }

    // ---- 1980s: the online catalogue ---------------------------------------
    era1980(q) {
      const terms = q.content.map(w => ({ w, postings: (this.cat.get(w) || []).length }));
      let list = [];
      if (terms.length) {
        const sets = q.content.map(w => new Set(this.cat.get(w) || []));
        list = this.titleOrder.filter(d => sets.every(s => s.has(d)));
      }
      let browse = null;
      if (!list.length && q.content.length) {
        const key = q.content.join(' ').toUpperCase();
        let at = 0;
        while (at < this.titleOrder.length && this._sortKey(this.titleOrder[at]) < key) at++;
        browse = { key, before: this.titleOrder.slice(Math.max(0, at - 3), at), after: this.titleOrder.slice(at, at + 3) };
      }
      return { key: 'e1980', list, total: list.length, terms, browse };
    }

    // ---- 1990s: tf-idf vector space, any word counts -----------------------
    era1990(q) {
      const acc = new Float32Array(this.N), N = this.N;
      let qn = 0;
      const matched = new Set();
      for (const s of q.stems) {
        const m = this.post.get(s);
        if (!m) continue;
        const idf = Math.log(N / m.size) + 0.01;
        qn += idf * idf;
        for (const [d, tf] of m) { const t = tf[0] + tf[1]; acc[d] += (1 + Math.log(t < 1 ? 1 : t)) * idf * idf; matched.add(d); }
      }
      qn = Math.sqrt(qn) || 1;
      const hits = [...matched].map(d => ({ d, score: acc[d] / (this.norm[d] * qn) })).sort((a, b) => b.score - a.score || a.d - b.d);
      return { key: 'e1990', hits, list: hits.map(h => h.d), total: hits.length };
    }

    // ---- shared BM25 with field weights ------------------------------------
    _bm25(q, opts) {
      const k1 = 1.2, b = 0.75, N = this.N, acc = new Float32Array(N), cov = new Uint8Array(N);
      const wTitle = opts && opts.title !== undefined ? opts.title : 3;
      for (const s of q.stems) {
        const m = this.post.get(s);
        if (!m) continue;
        const idf = this.idf(s);
        for (const [d, tf] of m) {
          const t = tf[0] + wTitle * tf[1];
          acc[d] += idf * (t * (k1 + 1)) / (t + k1 * (1 - b + b * this.len[d] / this.avgLen));
          cov[d]++;
        }
      }
      return { acc, cov };
    }

    didYouMean(q) {
      let changed = false;
      const out = q.content.map(w => {
        if (this.raw.has(w) || this.post.has(stem(w)) || w.length < 4 || /\d/.test(w)) return w;
        if (this.hasVectors && this.row(w) >= 0) return w;
        const max = w.length <= 5 ? 1 : 2;
        let best = null;
        for (const cand of this.rawVocab) {
          if (cand[0] !== w[0] || Math.abs(cand.length - w.length) > max) continue;
          const dist = editDistance(w, cand, max);
          if (dist > max) continue;
          const f = this.wordFreq.get(cand) || 0;
          if (f < 2) continue;
          if (!best || dist < best.dist || (dist === best.dist && f > best.f)) best = { w: cand, dist, f };
        }
        if (best) { changed = true; return best.w; }
        return w;
      });
      return changed ? out.join(' ') : null;
    }

    snippet(d, stems, width) {
      const want = new Set(stems), max = width || 30;
      let best = null;
      for (const ci of this.docChunks[d]) {
        const c = this.chunks[ci];
        const flags = c.ws.map(w => (STOP.has(w) ? null : stem(w)));
        for (let i = 0; i < c.ws.length; i += 4) {
          const seen = new Set();
          let n = 0;
          for (let j = i; j < Math.min(c.ws.length, i + max); j++) if (flags[j] && want.has(flags[j])) { seen.add(flags[j]); n++; }
          let sc = 0;
          for (const s of seen) sc += this.idf(s);
          sc += 0.05 * n;
          if (!best || sc > best.sc) best = { sc, ci, i };
        }
      }
      if (!best || best.sc <= 0) {
        const c = this.chunks[this.docChunks[d][0]];
        return { text: c ? cut(this.docs[d].ch[0], 190) : '', marks: [], lead: false, tail: true };
      }
      const c = this.chunks[best.ci], text = this.docs[d].ch[c.k];
      const a = best.i, z = Math.min(c.toks.length, best.i + max) - 1;
      const s = c.toks[a].s, e = c.toks[z].e;
      const marks = [];
      for (let j = a; j <= z; j++) {
        const w = c.ws[j];
        if (!STOP.has(w) && want.has(stem(w))) marks.push([c.toks[j].s - s, c.toks[j].e - s]);
      }
      return { text: text.slice(s, e), marks, lead: a > 0, tail: z < c.toks.length - 1, chunk: c.k };
    }

    // ---- 2000s: BM25 + fields + links + snippets ---------------------------
    era2000(q) {
      const { acc, cov } = this._bm25(q, { title: 3 });
      const nq = q.stems.filter(s => this.post.has(s)).length || 1;
      const hits = [];
      const phrase = q.content.length > 1 ? ' ' + q.content.map(stem).join(' ') + ' ' : null;
      for (let d = 0; d < this.N; d++) {
        if (!cov[d]) continue;
        const coord = cov[d] / nq;
        let score = acc[d] * (0.35 + 0.65 * coord * coord) * (1 + 0.3 * this.prn[d]);
        if (phrase && this.stemSeq[d].indexOf(phrase) !== -1) score *= 1.25;
        hits.push({ d, score, coord });
      }
      hits.sort((a, b) => b.score - a.score || a.d - b.d);
      return { key: 'e2000', hits, list: hits.map(h => h.d), total: hits.length, suggestion: this.didYouMean(q) };
    }

    // ---- 2010s: meaning as geometry ----------------------------------------
    _softQuery(q) {
      // For each content word: its vector row and its similarity to every word.
      const out = [];
      for (const w of q.content) {
        const r = this.hasVectors ? this.row(w) : -1;
        out.push({ w, st: stem(w), r, sims: r >= 0 ? this.simRow(r) : null, g: this.hasVectors ? this.widf(w) : 1 });
      }
      return out;
    }

    _softScore(sq, c, floor) {
      // Soft lexical match: each query word is credited with its best partner
      // in the passage. An identical stem scores 1; otherwise word-vector cosine.
      let total = 0, weight = 0;
      const pairs = [];
      for (const qw of sq) {
        weight += qw.g;
        let best = 0, bj = -1;
        for (let j = 0; j < c.ws.length; j++) {
          const w = c.ws[j];
          if (STOP.has(w)) continue;
          let s = 0;
          if (stem(w) === qw.st) s = 1;
          else if (qw.sims && c.rows && c.rows[j] >= 0) s = qw.sims[c.rows[j]];
          if (s > best) { best = s; bj = j; }
        }
        if (best >= (floor || 0.5)) { total += qw.g * best; pairs.push({ q: qw.w, w: c.ws[bj], s: best, j: bj }); }
        else pairs.push({ q: qw.w, w: null, s: best, j: -1 });
      }
      return { score: weight ? total / weight : 0, pairs };
    }

    era2010(q) {
      if (!this.hasVectors) return { key: 'e2010', hits: [], list: [], total: 0, oov: q.content, panel: null };
      const sq = this._softQuery(q);
      const oov = sq.filter(x => x.r < 0).map(x => x.w);
      const qv = this._embed(q.content);
      const hits = [];
      if (qv) {
        const D = this.D;
        const best = new Float32Array(this.N).fill(-1), bestC = new Int32Array(this.N).fill(-1);
        this.chunks.forEach((c, ci) => {
          if (!c.vec) return;
          let s = 0;
          for (let j = 0; j < D; j++) s += qv[j] * c.vec[j];
          if (s > best[c.doc]) { best[c.doc] = s; bestC[c.doc] = ci; }
        });
        for (let d = 0; d < this.N; d++) {
          if (bestC[d] < 0) continue;
          let ts = 0;
          const tv = this.titleVec[d];
          if (tv) for (let j = 0; j < D; j++) ts += qv[j] * tv[j];
          hits.push({ d, score: 0.72 * best[d] + 0.28 * ts, ci: bestC[d] });
        }
        hits.sort((a, b) => b.score - a.score || a.d - b.d);
        for (const h of hits.slice(0, 12)) h.pairs = this._softScore(sq, this.chunks[h.ci], 0.45).pairs;
      }
      const tm = this.matchTerms(q);
      const panel = tm.length ? tm[0].term : null;
      return { key: 'e2010', hits, list: hits.map(h => h.d), total: hits.length, oov, panel, sq };
    }

    // ---- 2020s: hybrid retrieval, fusion, rerank, answer -------------------
    era2020(q, dense) {
      const K = 40, RRF = 60;
      const { acc, cov } = this._bm25(q, { title: 2 });
      const sparse = [];
      for (let d = 0; d < this.N; d++) if (cov[d]) sparse.push({ d, score: acc[d] });
      sparse.sort((a, b) => b.score - a.score || a.d - b.d);
      const sTop = sparse.slice(0, K), dTop = (dense ? dense.hits : []).slice(0, K);
      const fused = new Map();
      sTop.forEach((h, i) => { fused.set(h.d, { d: h.d, rrf: 1 / (RRF + i + 1), sr: i + 1, dr: 0, bm25: h.score }); });
      dTop.forEach((h, i) => {
        const f = fused.get(h.d) || { d: h.d, rrf: 0, sr: 0, dr: 0, bm25: 0 };
        f.rrf += 1 / (RRF + i + 1); f.dr = i + 1; f.cos = h.score;
        fused.set(h.d, f);
      });
      const pool = [...fused.values()].sort((a, b) => b.rrf - a.rrf || a.d - b.d).slice(0, 24);
      const sq = dense && dense.sq ? dense.sq : this._softQuery(q);
      const topBm = sTop.length ? sTop[0].score : 1;
      const topCos = dTop.length ? dTop[0].score : 1;
      for (const f of pool) {
        let best = null;
        for (const ci of this.docChunks[f.d]) {
          const r = this._softScore(sq, this.chunks[ci], 0.5);
          if (!best || r.score > best.score) best = { score: r.score, pairs: r.pairs, ci };
        }
        const title = this._softScore(sq, { ws: words(this.docs[f.d].t), rows: null }, 0.99).score;
        f.soft = best ? best.score : 0;
        f.ci = best ? best.ci : -1;
        f.pairs = best ? best.pairs : [];
        f.title = title;
        f.score = 0.36 * f.soft + 0.24 * (f.bm25 / topBm) + 0.2 * title + 0.2 * Math.max(0, (f.cos || 0) / topCos);
      }
      const reranked = pool.slice().sort((a, b) => b.score - a.score || a.d - b.d);
      const hits = reranked.slice(0, 8);
      // Extractive answer: best sentences from the top passages, no generation.
      const cands = [];
      hits.slice(0, 4).forEach((h, rank) => {
        const order = this.docChunks[h.d].map(ci => ({ ci, s: this._softScore(sq, this.chunks[ci], 0.5).score })).sort((a, b) => b.s - a.s).slice(0, 2);
        for (const o of order) {
          const text = this.docs[h.d].ch[this.chunks[o.ci].k];
          for (const sent of splitSentences(text)) {
            if (sent.length < 60 || sent.length > 330 || /[:;]$/.test(sent) || /[\u2192\u2190=]/.test(sent)) continue;
            if (/^(This|That|These|Those|It|They|He|She|But|And|So|Here|There|Both|Neither|Each|Its|Their|Such)\b/.test(sent)) continue;
            if (/\b(Chapters?|Appendix|Figure|Table|Puzzle|above|below|earlier|previous|following)\b/.test(sent)) continue;
            const ws = words(sent);
            const c = { ws, rows: this.hasVectors ? Int32Array.from(ws, w => (STOP.has(w) ? -1 : this.row(w))) : null };
            const r = this._softScore(sq, c, 0.5);
            cands.push({ text: sent, d: h.d, ref: rank + 1, score: r.score * (1 - 0.06 * rank) * (sent.length > 250 ? 0.9 : 1), set: new Set(ws.filter(w => !STOP.has(w)).map(stem)) });
          }
        }
      });
      cands.sort((a, b) => b.score - a.score);
      const answer = [];
      for (const c of cands) {
        if (answer.length >= 3) break;
        if (c.score < 0.34) break;
        let dup = false;
        for (const a of answer) {
          let inter = 0;
          for (const s of c.set) if (a.set.has(s)) inter++;
          if (inter / Math.min(c.set.size, a.set.size) > 0.6 || (a.d === c.d && answer.length >= 2)) dup = true;
        }
        if (!dup) answer.push(c);
      }
      return { key: 'e2020', hits, list: reranked.map(h => h.d), total: reranked.length,
        stages: { sparse: sTop.length, dense: dTop.length, fused: fused.size, pool: pool.length, shown: hits.length },
        both: pool.filter(f => f.sr && f.dr).length, answer };
    }

    run(query) {
      const q = this.analyse(query);
      const r = { q };
      r.e1960 = this.era1960(q);
      r.e1970 = this.era1970(q);
      r.e1980 = this.era1980(q);
      r.e1990 = this.era1990(q);
      r.e2000 = this.era2000(q);
      r.e2010 = this.era2010(q);
      if (r.e2000.suggestion) {
        // A modern pipeline rewrites the query before retrieval.
        const q2 = this.analyse(r.e2000.suggestion);
        r.e2020 = this.era2020(q2, this.era2010(q2));
        r.e2020.rewritten = r.e2000.suggestion;
      } else r.e2020 = this.era2020(q, r.e2010);
      r.track = r.e2020.hits.length ? r.e2020.hits[0].d : (r.e2000.list.length ? r.e2000.list[0] : -1);
      return r;
    }

    rankOf(result, era, d) {
      const res = result[era];
      let list = res.list;
      if (era === 'e1970' && !list.length && res.broadened) list = res.broadened.list;
      const i = list.indexOf(d);
      return i === -1 ? 0 : i + 1;
    }
  }

  function unit(v) {
    let n = 0;
    for (let j = 0; j < v.length; j++) n += v[j] * v[j];
    n = Math.sqrt(n);
    if (!n) return null;
    for (let j = 0; j < v.length; j++) v[j] /= n;
    return v;
  }
  function cut(text, n) {
    if (text.length <= n) return text;
    const s = text.slice(0, n);
    return s.slice(0, Math.max(s.lastIndexOf(' '), n - 30));
  }
  function decodeBase64(b64) {
    if (typeof Buffer !== 'undefined') return new Uint8Array(Buffer.from(b64, 'base64'));
    const bin = atob(b64), out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  return {
    ERAS: ['e1960', 'e1970', 'e1980', 'e1990', 'e2000', 'e2010', 'e2020'],
    Engine, tokenize, words, stem, STOP, cut, splitSentences, decodeBase64,
    create: (corpus, vmeta, vdata) => new Engine(corpus, vmeta, typeof vdata === 'string' ? decodeBase64(vdata) : vdata),
  };
});
