// Run the actual page script against a small DOM fixture; no browser dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '..', 'vector-similarity-lab.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function boot(hash = '') {
  const nodes = new Map();
  function node(id) {
    if (!nodes.has(id)) nodes.set(id, {
      hidden: false, disabled: false, checked: false, value: '', dataset: {},
      style: {}, attrs: {}, listeners: {}, textContent: '', innerHTML: '',
      classList: {add(){}, toggle(){}},
      setAttribute(k,v){this.attrs[k]=v;},
      addEventListener(k,fn){this.listeners[k]=fn;},
      closest(selector){return node(id+selector);},
      querySelectorAll(){return [];}
    });
    return nodes.get(id);
  }
  for (const match of html.matchAll(/id="([^"]+)"/g)) node(match[1]);
  Object.assign(node('angle'), {min:'-180',max:'180'});
  Object.assign(node('magnitude'), {min:'.25',max:'2.5'});
  const buttons=['length','metric','filters'].map(id=>Object.assign(node('challenge-'+id),{dataset:{challenge:id}}));
  const location = {hash};
  const context = vm.createContext({
    URLSearchParams,location,
    history:{replaceState(a,b,value){location.hash=value;}},
    document:{getElementById:node,querySelector:node,querySelectorAll:s=>s==='[data-challenge]'?buttons:[]}
  });
  vm.runInContext(script.replace('})();', 'globalThis.lab={applyTour:index=>{tourIndex=index;applyTour(index);},chooseAnswer,ranked,values,TOURS,setMode,render};})();'),context);
  const click=id=>node(id).listeners.click({target:node(id)});
  const change=(id,value)=>{node(id).value=value;node(id).listeners.change({target:node(id)});};
  const check=(id,value)=>{node(id).checked=value;node(id).listeners.change({target:node(id)});};
  return {node,click,change,check,location,api:context.lab};
}
let t=boot();
const expected=['A','A','B','A','A','B','C'];
assert.equal(t.api.TOURS.length,7);
for(let i=0;i<7;i++){
  t.api.applyTour(i);
  assert.equal(t.node('ranking-results').hidden,true);
  assert.equal(t.node('selected-detail').hidden,true);
  assert.equal(t.node('tour-next').disabled,true);
  assert.doesNotMatch(t.node('live-summary').textContent,/ranks first/);
  if(i===5) assert.equal(t.api.ranked()[0],'A');
  if(i===6) assert.equal(t.api.ranked()[0],'B');
  // Even a wrong prediction reveals the correct experiment and permits progress.
  t.api.chooseAnswer({dataset:{value:'wrong'},classList:{add(){}}});
  assert.equal(t.api.ranked()[0],expected[i]);
  assert.equal(t.node('ranking-results').hidden,false);
  assert.equal(t.node('tour-next').disabled,false);
  assert.equal(t.node('filter-recent').disabled,true);
}
t.api.setMode(false);
t.click('cutoff-start');
assert.equal(t.api.ranked().join(','),'C');
t.change('filter-order','after');
assert.equal(t.api.ranked().join(','),'');
assert.match(t.node('rank-list').innerHTML,/Outside the candidate cutoff/);
t.change('top-k','3');
assert.equal(t.api.ranked().join(','),'C');
t.change('top-k','1');
assert.equal(t.api.ranked().join(','),'');
// A shared experiment must restore every control affecting admission and order.
let restored=boot(t.location.hash);
assert.equal(restored.node('filter-recent').checked,true);
assert.equal(restored.node('filter-empirical').checked,true);
assert.equal(restored.node('filter-order').value,'after');
assert.equal(restored.node('top-k').value,'1');
assert.equal(restored.api.ranked().join(','),'');
restored.click('btn-reset');
assert.equal(restored.api.ranked().join(','),'A,B,C');
assert.equal(restored.node('filter-recent').checked,false);
assert.equal(restored.node('filter-empirical').checked,false);
assert.equal(restored.node('filter-order').value,'before');
assert.equal(restored.node('top-k').value,'3');
t=restored;
t.click('challenge-length');
t.node('magnitude').value='2.5';t.node('magnitude').listeners.input();
assert.match(t.node('challenge-status').textContent,/Goal reached/);
assert.ok(Math.abs(t.api.values('B').cosine-Math.cos(55*Math.PI/180))<1e-12);
t.click('challenge-metric');t.click('metric-dot');
assert.match(t.node('challenge-status').textContent,/Goal reached/);
assert.match(t.node('change-note').textContent,/A → B → C/);
assert.match(t.node('change-note').textContent,/B → A → C/);
t.check('normalise',true);
assert.ok(Math.abs(t.api.values('B').cosine-t.api.values('B').dot)<1e-12);
t.click('challenge-filters');t.check('filter-recent',true);
assert.equal(t.api.ranked()[0],'B');
t.check('filter-empirical',true);
assert.match(t.node('challenge-status').textContent,/Goal reached/);
console.log('PASS: seven prediction/reveal states, cutoff order and depths, complete URL restoration/reset, three challenges and comparison feedback.');
