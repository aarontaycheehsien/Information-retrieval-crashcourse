// Pure calculation, fixture fidelity, boundaries and validation; no dependencies.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const api=require('../assets/rank-fusion-core.js');
const run=overrides=>api.calculate({...api.BOOK,...overrides});
let r=run({});
assert.deepEqual(r.rows.map(x=>x.id),['A','C','B','D']);
assert.deepEqual(r.rows.map(x=>x.score.toFixed(5)),['0.03252','0.03227','0.01613','0.01587']);
assert.equal(r.rows[2].b,0);
const book=fs.readFileSync(path.join(root,'search-textbook.html'),'utf8');
const table=book.slice(book.indexOf('id="tbl-10-1"'),book.indexOf('</table>',book.indexOf('id="tbl-10-1"')));
const fallback=fs.readFileSync(path.join(root,'rank-fusion-lab.html'),'utf8');
for(const row of r.rows){
  assert.ok(table.includes(`<td>${row.id}</td><td>${row.rankA||'—'}</td><td>${row.rankB||'—'}</td>`));
  assert.ok(table.includes(`${row.score.toFixed(5)}</td><td>${row.rank}</td>`));
  assert.ok(fallback.includes(`<th scope="row">${row.id}</th><td>${row.rankA||'—'}</td><td>${row.rankB||'—'}</td>`));
  assert.ok(fallback.includes(`${row.score.toFixed(5)}</td><td>${row.rank}</td>`));
}
const constant=api.STEPS[1].state;
assert.deepEqual(api.calculate(constant).rows.slice(0,2).map(x=>x.id),['A','D']);
assert.equal(api.calculate({...constant,c:60}).rows[0].id,'C');
assert.deepEqual(api.calculate({...constant,c:1}).rows.slice(0,3).map(x=>x.rank),[1,1,1]);
assert.ok(api.calculate({...constant,c:1,output:1}).splitTie);
assert.equal(run({depthB:1}).rows[0].id,'C');
assert.ok(!run({depthB:1}).rows.some(x=>x.id==='D'));
assert.equal(run({depthB:1}).rows.find(x=>x.id==='A').b,0);
assert.deepEqual(run({output:1}).rows,run({output:40}).rows);
assert.equal(run({a:'',b:''}).rows.length,0);
assert.equal(run({depthA:0,depthB:0}).rows.length,0);
assert.deepEqual(run({b:''}).rows.map(x=>x.id),['A','B','C']);
assert.equal(run({a:'A',b:'B'}).rows[0].rank,run({a:'A',b:'B'}).rows[1].rank);
assert.equal(run({a:'A',b:'A'}).rows.length,1);
assert.equal(run({a:'A',b:'A'}).rows[0].score,2/61);
assert.deepEqual(api.parseList(' A \n\nB\r\n','test'),['A','B']);
assert.deepEqual(api.parseList('A\na','test'),['A','a']);
assert.throws(()=>run({a:'A\n A'}),/List A, line 2: duplicate/);
assert.throws(()=>run({b:'B\nB'}),/List B, line 2: duplicate/);
assert.throws(()=>run({a:'x'.repeat(81)}),/80 characters/);
assert.throws(()=>run({a:Array.from({length:21},(_,i)=>'x'+i).join('\n')}),/at most 20/);
for(const c of ['',-1,101,1.5,Infinity,'no'])assert.throws(()=>run({c}),/Fusion constant/);
for(const depthA of ['',-1,21,.5])assert.throws(()=>run({depthA}),/input depth/);
for(const output of ['',0,41,1.5])assert.throws(()=>run({output}),/Output depth/);
for(const c of [0,1,10,60,100]){
  const a=Array.from({length:20},(_,i)=>'A'+i).join('\n');
  const b=Array.from({length:20},(_,i)=>'B'+i).join('\n');
  assert.equal(run({a,b,depthA:20,depthB:20,c,output:40}).visible.length,40);
}
for(const step of api.STEPS){
  assert.doesNotThrow(()=>api.calculate(step.state));
  assert.doesNotThrow(()=>api.calculate({...step.state,...step.change}));
}
// Identifiers are data even when they resemble markup.
assert.equal(run({a:'<img onerror=alert(1)>',b:''}).rows[0].id,'<img onerror=alert(1)>');
console.log('PASS: book/static fixtures, exact ties, constant change, cutoffs, empty lists, duplicates, validation and all guided states.');
