// Regression check for search-time-machine.html.
//
//   node tools/check-search-time-machine.mjs            engine checks only
//   node tools/check-search-time-machine.mjs --browser  also load the page in Chromium (needs Playwright)
//
// The engine checks read the corpus and vectors out of the built page, so they
// test what ships. Run tools/build-search-time-machine.py first.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pagePath = path.join(root, 'search-time-machine.html');
const html = readFileSync(pagePath, 'utf8');
const STM = require(path.join(root, 'assets', 'search-time-machine-engine.js'));

const block = id => {
  const m = html.match(new RegExp('<script type="[^"]+" id="' + id + '">([\\s\\S]*?)</script>'));
  if (!m) throw new Error('missing data block ' + id);
  return m[1];
};
const corpus = JSON.parse(block('stm-corpus'));
const vmeta = JSON.parse(block('stm-vmeta'));
const engine = STM.create(corpus, vmeta, block('stm-vectors').trim());

let failed = 0;
const check = (name, ok, detail) => {
  if (!ok) failed++;
  console.log((ok ? 'ok   ' : 'FAIL ') + name + (ok || detail === undefined ? '' : '  -> ' + detail));
};
const title = d => corpus.docs[d].t;

check('corpus has the book’s sections', engine.N >= 150, engine.N);
check('glossary supplies the thesaurus', engine.terms.length >= 80, engine.terms.length);
check('word vectors loaded', engine.hasVectors && engine.V === vmeta.count && engine.D === vmeta.dims);
check('page embeds the same engine source', html.includes(readFileSync(path.join(root, 'assets', 'search-time-machine-engine.js'), 'utf8')));
check('Porter stems relevant to relev', STM.stem('relevant') === 'relev', STM.stem('relevant'));
check('Porter conflates retrieval forms', STM.stem('retrieved') === STM.stem('retrieves'));

let r = engine.run('why did my search miss a relevant paper');
check('1960s: a plain question has no thesaurus term', r.e1960.mode === 'NONE' && r.e1960.total === 0, r.e1960.mode);
check('1980s: the catalogue finds nothing and offers a browse', r.e1980.total === 0 && r.e1980.browse && r.e1980.browse.after.length > 0);
check('1990s: any-word ranking returns many sections', r.e1990.total > 100, r.e1990.total);
check('2010s: every section gets a distance', r.e2010.total === engine.N, r.e2010.total);
check('2020s: an extractive answer is quoted from retrieved sections', r.e2020.answer.length >= 1 && r.e2020.answer.every(a => corpus.docs[a.d].ch.some(c => c.includes(a.text))));
check('2020s: fusion pool draws on both routes', r.e2020.stages.sparse === 40 && r.e2020.stages.dense === 40 && r.e2020.both > 0);

r = engine.run('BM25');
check('1960s: BM25 is a thesaurus term', r.e1960.mode === 'AND' && r.e1960.descriptors[0].label === 'BM25' && r.e1960.total > 0);
check('1970s: exact word has postings, newest first', r.e1970.total > 20 && r.e1970.list[0] > r.e1970.list[r.e1970.list.length - 1]);
check('1980s: catalogue list is alphabetical', r.e1980.total > 0 && r.e1980.list.every((d, i, a) => i === 0 || engine._sortKey(a[i - 1]).localeCompare(engine._sortKey(d)) <= 0));
check('ranked eras put a BM25 section first', ['e1990', 'e2000', 'e2010', 'e2020'].every(k => /BM25/.test(title(r[k].list[0]))), ['e1990', 'e2000', 'e2010', 'e2020'].map(k => title(r[k].list[0])).join(' | '));

r = engine.run('retreival augmented genration');
check('2000s: spelling suggestion', r.e2000.suggestion === 'retrieval augmented generation', r.e2000.suggestion);
check('2020s: query rewritten before retrieval', r.e2020.rewritten === 'retrieval augmented generation' && /Retrieval-augmented generation/.test(title(r.e2020.hits[0].d)), r.e2020.hits.length && title(r.e2020.hits[0].d));
check('2010s: misspelt words have no vector', r.e2010.oov.includes('retreival') && r.e2010.oov.includes('genration'), r.e2010.oov.join(','));

r = engine.run('hybrid AND NOT dense');
const has = (w, d) => (engine.raw.get(w) || []).includes(d);
check('1970s: Boolean statement parsed as written', r.e1970.explicit && r.e1970.statement === 'HYBRID AND NOT DENSE', r.e1970.statement);
check('1970s: NOT is honoured', r.e1970.total > 0 && r.e1970.list.every(d => has('hybrid', d) && !has('dense', d)), r.e1970.total);
check('2000s: later engines ignore NOT', r.e2000.list.slice(0, 5).some(d => has('dense', d)));

r = engine.run('"rank fusion" OR librar*');
check('1970s: phrases and truncation', r.e1970.terms.length === 2 && r.e1970.terms.every(t => t.postings > 0), JSON.stringify(r.e1970.terms));

r = engine.run('doctors hunting for clinical trials');
check('no shared words: lexical eras return nothing', r.e1970.total === 0 && r.e1990.total === 0 && r.e2000.total === 0 && !r.e2000.suggestion, [r.e1970.total, r.e1990.total, r.e2000.total, r.e2000.suggestion].join(','));
check('no shared words: vectors still rank everything', r.e2010.total === engine.N && r.e2020.hits.length > 0);

r = engine.run('   ');
check('empty query is harmless', r.e1990.total === 0 && r.track === -1);
r = engine.run('the of and');
check('stop-word-only query is harmless', r.e1970.total === 0 && r.e2020.hits.length === 0);

if (process.argv.includes('--browser')) {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const errors = [];
  for (const width of [1280, 400]) {
    const page = await (await browser.newContext({ viewport: { width, height: 860 } })).newPage();
    page.on('pageerror', e => errors.push(width + 'px: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(width + 'px console: ' + m.text()); });
    await page.goto(pathToFileURL(pagePath).href + '#still');
    await page.waitForFunction(() => window.STMApp && window.STMApp.state.result, null, { timeout: 30000 });
    const queries = await page.$$eval('.chip', els => els.map(e => e.dataset.q));
    let overflow = 0, empty = 0;
    for (const q of queries) {
      for (const era of STM.ERAS) {
        const m = await page.evaluate(([qq, k]) => {
          window.STMApp.search(qq, true); window.STMApp.setEra(k, true);
          return { over: document.documentElement.scrollWidth - document.documentElement.clientWidth, len: document.getElementById('screen').textContent.length };
        }, [q, era]);
        if (m.over > 0) overflow++;
        if (m.len < 80) empty++;
      }
    }
    check(width + 'px: ' + queries.length + ' presets x 7 decades render', empty === 0, empty + ' empty screens');
    check(width + 'px: no horizontal page scroll', overflow === 0, overflow + ' overflowing states');
    await page.evaluate(() => { window.STMApp.search('BM25', true); window.STMApp.setEra('e2000', true); });
    await page.click('#screen [data-d]:nth-of-type(1), #screen li[data-d]');
    check(width + 'px: clicking a result follows it', await page.evaluate(() => window.STMApp.state.pinned === true));
  }
  check('no page or console errors', errors.length === 0, errors.slice(0, 3).join(' ; '));
  await browser.close();
}

console.log(failed ? '\n' + failed + ' check(s) failed' : '\nall checks passed');
process.exit(failed ? 1 : 0);
