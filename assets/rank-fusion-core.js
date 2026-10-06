/* Pure, offline RRF calculation. Shared by the browser and Node regression tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.RankFusion = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const BOOK = {a:'A\nB\nC', b:'C\nA\nD', c:60, depthA:3, depthB:3, output:4};
  const STEPS = [
    {title:'1. Agreement', state:BOOK,
      prompt:'Predict the fused order. Can a record present in both lists outrank a record supplied by only one?',
      change:{}, action:'Reveal the explanation',
      explanation:'A, C, B, D is the book’s order. A and C each receive two contributions; B and D receive one. Shared letters mean the same record, not two copies. Agreement is evidence from two rankings, not a human relevance judgement.'},
    {title:'2. The constant', state:{a:'A\nB\nC',b:'D\nE\nC',c:0,depthA:3,depthB:3,output:5},
      prompt:'At c = 0, A and D each rank first in one list; C ranks third in both. Predict whether changing c to 60 will change who leads.',
      change:{c:60}, action:'Set c to 60 and explain',
      explanation:'At c = 0, A and D each score 1, above C’s 2/3. At c = 60, C scores 2/63, above their 1/61. At c = 1 they tie. A larger constant softens position differences; it does not guarantee better retrieval. Equal scores remain ties even though identifiers determine their display order.'},
    {title:'3. Candidate boundaries', state:BOOK,
      prompt:'Keep c = 60. Predict what happens if list B supplies only its first record, C. Which contributions disappear?',
      change:{depthB:1}, action:'Reduce list B depth to 1',
      explanation:'A loses its list-B contribution, and D disappears from the candidate union. C still receives two contributions and leads. A and B retain their list-A contributions. A result beyond an input cutoff contributes nothing; fusion cannot recover a record absent from both supplied lists.'},
    {title:'4. Scores are not relevance', state:BOOK,
      prompt:'A has the highest fused score. Does keeping only A establish that it is relevant, or that fusion improved the search?',
      change:{output:1}, action:'Keep one output and explain',
      explanation:'No. Output depth only hides lower-ranked fused records; it leaves all scores unchanged. These schematic identifiers have no relevance judgements. Evaluate against a written information need and human judgements before claiming an improvement.'}
  ];
  function integer(value, min, max, label) {
    if (String(value).trim() === '') throw new Error(`${label}: enter a whole number from ${min} to ${max}.`);
    const n = Number(value);
    if (!Number.isInteger(n) || n < min || n > max) throw new Error(`${label}: enter a whole number from ${min} to ${max}.`);
    return n;
  }
  function parseList(text, label) {
    const ids=[], seen=new Set();
    String(text).split(/\r?\n/).forEach((line,i)=>{
      const id=line.trim(); if (!id) return;
      if (id.length > 80) throw new Error(`${label}, line ${i+1}: use an identifier of at most 80 characters.`);
      if (seen.has(id)) throw new Error(`${label}, line ${i+1}: duplicate identifier “${id}”. Keep each identifier once within a list.`);
      seen.add(id);ids.push(id);
    });
    if(ids.length>20)throw new Error(`${label}: at most 20 records are supported.`);
    return ids;
  }
  function compareScore(a,b) {
    const difference=a.n*b.d-b.n*a.d;
    return difference>0n?-1:difference<0n?1:0;
  }
  function calculate(input) {
    const a=parseList(input.a,'List A'),b=parseList(input.b,'List B');
    const c=integer(input.c,0,100,'Fusion constant c');
    const depthA=integer(input.depthA,0,20,'List A input depth');
    const depthB=integer(input.depthB,0,20,'List B input depth');
    const output=integer(input.output,1,40,'Output depth');
    const suppliedA=a.slice(0,depthA),suppliedB=b.slice(0,depthB);
    const rows=[...new Set([...suppliedA,...suppliedB])].map(id=>{
      const rankA=suppliedA.indexOf(id)+1,rankB=suppliedB.indexOf(id)+1;
      const da=rankA?BigInt(c+rankA):1n,db=rankB?BigInt(c+rankB):1n;
      const n=(rankA?db:0n)+(rankB?da:0n),d=da*db;
      return {id,rankA,rankB,n,d,score:Number(n)/Number(d),a:rankA?1/(c+rankA):0,b:rankB?1/(c+rankB):0};
    }).sort((x,y)=>compareScore(x,y)||(x.id<y.id?-1:x.id>y.id?1:0));
    rows.forEach((row,i)=>{
      row.rank=i && compareScore(row,rows[i-1])===0?rows[i-1].rank:i+1;
      row.tied=(i>0 && compareScore(row,rows[i-1])===0)||(i+1<rows.length && compareScore(row,rows[i+1])===0);
    });
    return {a,b,c,depthA,depthB,output,suppliedA,suppliedB,rows,visible:rows.slice(0,output),
      splitTie:rows.length>output && compareScore(rows[output-1],rows[output])===0};
  }
  return {BOOK,STEPS,calculate,parseList,compareScore};
});
