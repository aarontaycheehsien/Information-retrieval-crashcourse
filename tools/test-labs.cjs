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
  + '\nglobalThis.api={state,DEFAULTS,STEPS,stepControls,analyse,renderSaturation,setAnalysis:value=>A=value};';
const charts=[];
const bctx=vm.createContext({A:null,$:()=>({style:{display:''},innerHTML:''}),chart:(caption,xs,ys)=>{charts.push({caption,xs,ys});return '';}});
vm.runInContext(bcode,bctx);
const b=bctx.api;
const reset=()=>Object.assign(b.state,b.DEFAULTS,{off:[]});
const step=title=>{const s=b.STEPS.find(x=>x.title===title);assert.ok(s,'no tour step titled '+title);return s;};
const doc=(a,id)=>a.docs.find(d=>d.id===id);
reset();step('From admission rules to weighted clues').apply();assert.equal(b.analyse().ranked.map(d=>d.id).join(','),'A');
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
reset();step('What BM25 cannot understand').apply();a=b.analyse();assert.equal(doc(a,'B').matched.join(','),'about,a,job');
for(const [term,winner] of [['unrealistic','B'],['foolish','F']]){
  reset();step('What BM25 cannot understand').apply();b.state.query+=' '+term;assert.equal(b.analyse().ranked[0].id,winner);
}
// The boundary step must actually cut a record that outscores nothing below it.
reset();step('The boundary that scoring cannot cross').apply();a=b.analyse();
assert.equal(b.state.topk,1);
assert.equal(a.ranked.slice(0,2).map(d=>d.id).join(','),'D,A');
assert.ok(doc(a,'A').total>0,'Record A is scored, just not passed on');
// Every other step restores the full list, so the boundary is only in play at its own step.
for(const st of b.STEPS){reset();st.apply();
  assert.ok(st.title==='The boundary that scoring cannot cross'?b.state.topk===1:b.state.topk===6,
    'topk not reset by step: '+st.title);}
// Each step must show and unlock the controls its own instructions name.
const tourControls=title=>b.stepControls(b.STEPS.indexOf(step(title)),false);
assert.ok(tourControls('What BM25 cannot understand').syn,'synonym buttons hidden at the step that uses them');
assert.ok(tourControls('What BM25 cannot understand').strictOn,'admission toggle locked at the last step');
assert.equal(b.STEPS.filter((s,i)=>b.stepControls(i,false).syn).length,1,'synonym buttons shown at another step');
assert.ok(tourControls('Repetition helps, then stops helping').repeatOn);
assert.ok(tourControls('The boundary that scoring cannot cross').topkOn);
assert.ok(tourControls('BM25 adds the clues together').padOn);
// Step 4 must not reveal step 5's answer: A still leads at the slider's limit there.
{const c=tourControls('The same matches mean more in a short document');assert.ok(c.padOn);
 reset();b.state.pad=c.padMax;assert.equal(b.analyse().ranked[0].id,'A','step 4 slider reaches the point where D overtakes A');
 reset();b.state.pad=tourControls('BM25 adds the clues together').padMax;assert.equal(b.analyse().ranked[0].id,'D');}
for(const s of b.STEPS){assert.ok(s.use&&s.use.target,'no control target for step: '+s.title);}
reset();b.state.query='unrealistic foolish';a=b.analyse();assert.equal(a.stats.unrealistic.idf,a.stats.foolish.idf);
reset();b.state.b=0;const score=doc(b.analyse(),'A').total;b.state.pad=8;assert.equal(doc(b.analyse(),'A').total,score);
const vector=read('vector-similarity-lab.html');
// Slider bounds come from the page, not from this file, so the fixture cannot
// drift away from the lab the way it had.
const bound=(id,attr)=>{
  const m=new RegExp('<input[^>]*id="'+id+'"[^>]*'+attr+'="([^"]*)"').exec(vector);
  assert.ok(m,'no '+attr+' on #'+id);
  return m[1];
};
const controls={
  angle:{min:bound('angle','min'),max:bound('angle','max')},
  magnitude:{min:bound('magnitude','min'),max:bound('magnitude','max')}
};
// Two bounds the page's own prose depends on: the appendix says 180 degrees is
// "exactly opposite, where cosine similarity reaches -1", and the page says it
// avoids a zero-length vector because its cosine is undefined.
assert.equal(Number(controls.angle.max),180);
assert.equal(Number(controls.angle.min),-180);
assert.ok(Number(controls.magnitude.min)>0);
const vctx=vm.createContext({document:{getElementById:id=>controls[id]||{},querySelectorAll:()=>[]}});
const vcode=vector.slice(vector.indexOf('const COLOURS'),vector.indexOf('function setMetric'))
  +vector.slice(vector.indexOf('function barStyle'),vector.indexOf('function renderRanking'))
  +vector.slice(vector.indexOf('const TOURS'),vector.indexOf('function applyTour'))
  + '\nglobalThis.api={values,ranked,excluded,excludedBy,barStyle,set:(m,n)=>{metric=m;normalised=n;},'
  + 'setFilters:f=>{filters=Object.assign({recent:false,empirical:false},f);},candidates,TOURS,stepControls};';
vm.runInContext(vcode,vctx);const v=vctx.api;
assert.equal(v.ranked()[0],'A');v.set('dot',false);assert.equal(v.ranked()[0],'B');
v.set('dot',true);for(const id of ['A','B','C'])assert.equal(v.values(id).dot,v.values(id).cosine);
assert.ok(v.values('C').cosine<0);
v.set('dot',false);v.candidates.A.angle=0;v.candidates.A.magnitude=2.5;
assert.ok(Math.abs(v.values('A').dot-4.75)<1e-12);
const width=value=>Number(/width:([0-9.]+)%/.exec(v.barStyle(value))[1]);
assert.ok(width(4.75)>width(4));assert.equal(width(4.75),50);

// Filters are an admission rule applied before ranking. The date rule alone is the
// point of tour step 6: it removes A and promotes B, which still fails the query.
v.candidates.A={angle:24,magnitude:1};v.candidates.B={angle:55,magnitude:1.9};v.candidates.C={angle:122,magnitude:1.35};
v.set('cosine',false);
v.setFilters({});assert.equal(v.ranked().join(','),'A,B,C');assert.equal(v.excluded().length,0);
v.setFilters({recent:true});
assert.equal(v.ranked()[0],'B','date filter alone must promote the commentary');
assert.equal(v.excluded().join(','),'A');
assert.match(v.excludedBy('A'),/2012/);
v.setFilters({recent:true,empirical:true});
assert.equal(v.ranked().join(','),'C','both criteria leave only C');
assert.equal(v.excluded().join(','),'A,B');
assert.ok(v.values('C').cosine<0,'C wins on eligibility, not on score');
v.setFilters({});
// Each tour step must show and unlock the controls its own text names.
{const at=title=>{const i=v.TOURS.findIndex(s=>s.title===title);assert.ok(i>=0,'no vector tour step titled '+title);return i;};
 const unlocked=name=>v.TOURS.map((s,i)=>v.stepControls(i,false,true).on[name]?s.title:null).filter(Boolean).join('|');
 assert.equal(unlocked('magnitude'),'Dot product also sees magnitude');
 assert.equal(unlocked('normalise'),'Normalisation makes the rules agree');
 assert.equal(unlocked('recent'),'Apply the date criterion');
 assert.equal(unlocked('empirical'),'Apply the study-type criterion');
 assert.equal(unlocked('angle'),'');assert.equal(unlocked('metric'),'');
 // Nothing is unlocked before the prediction, and the sandbox unlocks everything.
 v.TOURS.forEach((s,i)=>{const on=v.stepControls(i,false,false).on;assert.ok(Object.values(on).every(x=>!x),'control unlocked before prediction: '+s.title);
   assert.ok(s.target,'no control target for vector step: '+s.title);});
 assert.ok(Object.values(v.stepControls(0,true,false).on).every(Boolean));
 // A control stays visible from the step that introduces it.
 const shownFrom=name=>v.TOURS.findIndex((s,i)=>v.stepControls(i,false,false).show[name]);
 assert.equal(shownFrom('metric'),at('Cosine turns direction into a score'));
 assert.equal(shownFrom('magnitude'),at('Dot product also sees magnitude'));
 assert.equal(shownFrom('normalise'),at('Normalisation makes the rules agree'));
 assert.equal(shownFrom('filters'),at('Apply the date criterion'));
 for(const name of ['metric','magnitude','normalise','filters'])
   for(let i=shownFrom(name);i<v.TOURS.length;i++)assert.ok(v.stepControls(i,false,false).show[name],name+' hidden again at step '+(i+1));
 // The eligibility warning appears only after a prediction, on the steps that flag it.
 assert.ok(!v.stepControls(at('Apply the date criterion'),false,false).note);
 assert.ok(v.stepControls(at('Apply the date criterion'),false,true).note);
 assert.ok(!v.stepControls(at('Cosine turns direction into a score'),false,true).note);
 // The steps where the learner acts start from the state their text describes.
 assert.equal(v.TOURS[at('Normalisation makes the rules agree')].normalised,false);
 assert.deepEqual({...v.TOURS[at('Apply the study-type criterion')].filters},{recent:true,empirical:false});
 // Step 3's claim: A overtakes B under dot product once B is shorter than about 1.6.
 v.set('dot',false);v.candidates.B.magnitude=1.55;assert.equal(v.ranked()[0],'A');
 v.candidates.B.magnitude=1.65;assert.equal(v.ranked()[0],'B');v.candidates.B.magnitude=1.9;v.set('cosine',false);}
console.log('PASS: script syntax, BM25 admission/ranking and all tour examples, the candidate boundary and its reset across steps, chart/slider agreement, cosine/dot ranking, normalisation, unclipped bars, the vector lab\'s metadata filters and each tour step\'s controls in both labs.');
