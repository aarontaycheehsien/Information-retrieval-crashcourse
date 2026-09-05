// Run with node tools/test-labs.cjs. No third-party packages required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
for (const name of ['search-textbook.html','teaching-notes.html','bm25-evidence-lab.html','vector-similarity-lab.html']) {
  for (const m of read(name).matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)) {
    if (m[1].trim()) new Function(m[1]);
  }
}
const bm = read('bm25-evidence-lab.html');
const bcode = bm.slice(bm.indexOf('const RECORDS'),bm.indexOf('const SERIES'))
  + bm.slice(bm.indexOf('const DEFAULTS'),bm.indexOf('/* colour follows'))
  + bm.slice(bm.indexOf('function tok'),bm.indexOf('/* ============================== helpers'))
  + bm.slice(bm.indexOf('const STEPS'),bm.indexOf('let tourStep'))
  + bm.slice(bm.indexOf('function renderSaturation'),bm.indexOf('function chart'))
  + '\nglobalThis.api={state,DEFAULTS,STEPS,analyse,renderSaturation,setAnalysis:value=>A=value};';
const charts=[];
const bctx=vm.createContext({A:null,$:()=>({style:{display:''},innerHTML:''}),chart:(caption,xs,ys)=>{charts.push({caption,xs,ys});return '';}});
vm.runInContext(bcode,bctx);
const b=bctx.api;
const reset=()=>Object.assign(b.state,b.DEFAULTS,{off:[]});
const doc=(a,id)=>a.docs.find(d=>d.id===id);
reset();b.STEPS[0].apply();assert.equal(b.analyse().ranked.map(d=>d.id).join(','),'A');
b.state.strict=false;assert.equal(b.analyse().ranked.length,6);
reset();let a=b.analyse();const first=doc(a,'D').parts.delulu;
assert.ok(Math.abs(first-1.882)<.002);
b.state.repeat=20;a=b.analyse();assert.ok(Math.abs(doc(a,'D').parts.delulu/first-1.143)<.003);
reset();b.state.pad=6;a=b.analyse();assert.equal(a.ranked[0].id,'D');assert.ok(doc(a,'D').total>doc(a,'A').total);
// The chart must represent the same changing collection as the slider.
for(const repeat of [1,3,10,20]){
  reset();b.state.repeat=repeat;a=b.analyse();b.setAnalysis(a);charts.length=0;b.renderSaturation();
  assert.ok(Math.abs(charts[1].ys[repeat-1]-doc(a,'D').parts.delulu)<1e-12);
}
reset();b.STEPS[5].apply();a=b.analyse();assert.equal(doc(a,'B').matched.join(','),'about,a,job');
for(const [term,winner] of [['unrealistic','B'],['foolish','F']]){
  reset();b.STEPS[5].apply();b.state.query+=' '+term;assert.equal(b.analyse().ranked[0].id,winner);
}
reset();b.state.query='unrealistic foolish';a=b.analyse();assert.equal(a.stats.unrealistic.idf,a.stats.foolish.idf);
reset();b.state.b=0;const score=doc(b.analyse(),'A').total;b.state.pad=8;assert.equal(doc(b.analyse(),'A').total,score);
const vector=read('vector-similarity-lab.html');
const controls={angle:{min:'-170',max:'170'},magnitude:{min:'.25',max:'2.5'}};
const vctx=vm.createContext({document:{getElementById:id=>controls[id]||{},querySelectorAll:()=>[]}});
const vcode=vector.slice(vector.indexOf('const COLOURS'),vector.indexOf('function setMetric'))
  +vector.slice(vector.indexOf('function barStyle'),vector.indexOf('function renderRanking'))
  + '\nglobalThis.api={values,ranked,barStyle,set:(m,n)=>{metric=m;normalised=n;},candidates};';
vm.runInContext(vcode,vctx);const v=vctx.api;
assert.equal(v.ranked()[0],'A');v.set('dot',false);assert.equal(v.ranked()[0],'B');
v.set('dot',true);for(const id of ['A','B','C'])assert.equal(v.values(id).dot,v.values(id).cosine);
assert.ok(v.values('C').cosine<0);
v.set('dot',false);v.candidates.A.angle=0;v.candidates.A.magnitude=2.5;
assert.ok(Math.abs(v.values('A').dot-4.75)<1e-12);
const width=value=>Number(/width:([0-9.]+)%/.exec(v.barStyle(value))[1]);
assert.ok(width(4.75)>width(4));assert.equal(width(4.75),50);
console.log('PASS: script syntax, BM25 admission/ranking and all tour examples, chart/slider agreement, cosine/dot ranking, normalisation and unclipped bars.');
