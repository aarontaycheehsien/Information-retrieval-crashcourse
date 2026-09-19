/* Progressive enhancement. No network, dependencies, storage or HTML injection. */
(() => {
  'use strict';
  const glossary = document.getElementById('glossary');
  const panel = document.getElementById('book-lookup');
  const input = document.getElementById('book-lookup-input');
  const data = document.getElementById('book-lookup-index');
  if (!glossary || !panel || !input || !data) return;
  const index = JSON.parse(data.textContent);
  const normalise = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const prepared = index.map((entry, order) => ({...entry, order,
    names: [entry.title, ...entry.aliases].map(normalise),
    words: normalise([entry.title, ...entry.aliases, entry.text, entry.location].join(' '))}));
  panel.hidden = false;
  document.querySelectorAll('.lookup-trigger').forEach(link => link.hidden = false);
  const results = document.getElementById('book-lookup-results');
  const status = document.getElementById('book-lookup-status');
  const more = document.getElementById('book-lookup-more');
  let matches = [], limit = 20;

  function render() {
    results.replaceChildren();
    for (const entry of matches.slice(0, limit)) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + entry.id; a.textContent = entry.title;
      const context = document.createElement('span');
      context.className = 'lookup-context'; context.textContent = entry.kind + ' · ' + entry.location;
      const excerpt = document.createElement('p');
      excerpt.textContent = entry.text.length > 180 ? entry.text.slice(0,177) + '…' : entry.text;
      li.append(a, context, excerpt); results.append(li);
    }
    more.hidden = matches.length <= limit;
    const q = normalise(input.value);
    status.textContent = !q ? 'Type a term, acronym or section title.' : !matches.length
      ? 'No matching terms or sections. Try a shorter term or acronym, or use your browser’s Find command for full text.'
      : `${matches.length} result${matches.length === 1 ? '' : 's'}; showing ${Math.min(limit,matches.length)}. Exact terms and aliases appear first.`;
  }

  function search() {
    limit = 20;
    const q = normalise(input.value);
    const tokens = q.split(' ').filter(Boolean);
    matches = !q ? [] : prepared.map(entry => {
      let score = entry.names.includes(q) ? (entry.kind === 'Term' ? 100 : 90)
        : entry.names.some(name => name.startsWith(q)) ? (entry.kind === 'Term' ? 80 : 70)
        : tokens.every(t => entry.names.some(name => name.split(' ').includes(t))) ? 60
        : tokens.every(t => entry.words.split(' ').some(word => word.startsWith(t))) ? 40 : 0;
      return {...entry, score};
    }).filter(e => e.score).sort((a,b) => b.score-a.score || a.order-b.order);
    render();
  }
  input.addEventListener('input', search);
  panel.querySelector('form').addEventListener('submit', e => { e.preventDefault(); search(); });
  document.getElementById('book-lookup-clear').addEventListener('click', () => {input.value = ''; search(); input.focus();});
  more.addEventListener('click', () => {
    const previous = limit; limit += 20; render();
    // Keep keyboard focus in the results when the activating button disappears.
    results.children[previous]?.querySelector('a')?.focus();
  });

  function targetFor(hash) {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch { return null; }
  }
  function reveal(target) {
    if (!target) return;
    if (target.matches('details')) target.open = true;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.matches('details')) parent.open = true;
    }
  }
  const initial = targetFor(location.hash);
  // Open in source markup for no-JS links; collapse only after enhancement loads.
  if (!initial || !(initial === glossary || glossary.contains(initial))) glossary.open = false;
  reveal(initial);
  if (initial && (initial === glossary || glossary.contains(initial))) {
    requestAnimationFrame(() => initial.scrollIntoView({behavior: 'instant', block: 'start'}));
  }
  function navigate() {
    const target = targetFor(location.hash); reveal(target);
    if (!target) return;
    if (target === panel) { input.focus({preventScroll:true}); }
    else if (target.id.startsWith('term-')) target.focus({preventScroll:true});
    target.scrollIntoView({behavior:'instant',block:'start'});
  }
  addEventListener('hashchange', navigate);
  document.addEventListener('click', event => {
    const a = event.target.closest('a[href^="#"]');
    if (!a || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const target = targetFor(a.hash); reveal(target);
    // Repeated clicks on the current fragment do not fire hashchange.
    if (a.hash === location.hash) navigate();
  });
  addEventListener('beforeprint', () => glossary.open = true);
  if (initial === panel) requestAnimationFrame(navigate);
})();
