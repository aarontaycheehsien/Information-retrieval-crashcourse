/* DOM-only presentation: identifiers are always inserted as text, never HTML. */
(() => {
  'use strict';
  const api=globalThis.RankFusion;if(!api)return;
  const $=id=>document.getElementById(id);
  const fields={a:$('list-a'),b:$('list-b'),c:$('constant'),depthA:$('depth-a'),depthB:$('depth-b'),output:$('output-depth')};
  let step=0;
  const read=()=>Object.fromEntries(Object.entries(fields).map(([key,el])=>[key,el.value]));
  const write=value=>Object.entries(fields).forEach(([key,el])=>el.value=value[key]);
  function cell(tag,text){const el=document.createElement(tag);el.textContent=text;return el;}
  function rankedList(ids,depth,key){
    const ol=$('ranks-'+key);ol.replaceChildren();
    ids.forEach((id,i)=>{
      const li=cell('li',id);
      if(i>=depth){li.className='excluded';li.append(cell('span',' — outside supplied depth'));}
      ol.append(li);
    });
    $('count-'+key).textContent=`${ids.length} entered; ${Math.min(ids.length,depth)} supplied for fusion.${ids.length===0?' This list is empty.':''}`;
  }
  function render(){
    $('error').hidden=true;
    let result;
    try{result=api.calculate(read());}
    catch(error){
      $('error').textContent=error.message;$('error').hidden=false;
      $('results').hidden=true;$('result-rows').replaceChildren();
      for(const k of ['a','b']){$('ranks-'+k).replaceChildren();$('count-'+k).textContent='Waiting for valid inputs.';}
      $('status').textContent='Results withheld until the input error is corrected.';return;
    }
    rankedList(result.a,result.depthA,'a');rankedList(result.b,result.depthB,'b');
    $('status').textContent=result.rows.length
      ?`${result.suppliedA.length} supplied by A; ${result.suppliedB.length} supplied by B; ${result.rows.length} distinct candidates. Showing ${result.visible.length} of ${result.rows.length}.`
      :'No supplied candidates. Both lists are empty or their input depths exclude every record; there is nothing to fuse.';
    $('results-caption').textContent=`Equal-weight RRF · c = ${result.c} · input depths ${result.depthA}/${result.depthB} · output depth ${result.output}`;
    const body=$('result-rows');body.replaceChildren();
    for(const row of result.visible){
      const tr=document.createElement('tr');
      tr.append(cell('td',`${row.rank}${row.tied?' (tie)':''}`));
      const name=cell('th',row.id);name.scope='row';tr.append(name);
      for(const key of ['A','B']){
        const rank=row['rank'+key];tr.append(cell('td',rank||'—'));
        const contribution=cell('td',rank?`1 / (${result.c} + ${rank})`:'0');
        contribution.append(cell('small',rank?'= '+row[key.toLowerCase()].toFixed(5):'Absent from supplied list'));
        tr.append(contribution);
      }
      tr.append(cell('td',row.score.toFixed(5)));body.append(tr);
    }
    const tied=result.rows.some(r=>r.tied);
    $('tie-note').hidden=!tied;
    $('tie-note').textContent='Equal scores share a rank. Identifiers are sorted by JavaScript string order only to make display deterministic.'+
      (result.splitTie?' The output cutoff splits a tied group: the displayed identifier order decides which tied records remain visible, not greater relevance.':'');
    $('results').hidden=!result.rows.length;
    document.querySelectorAll('#presets button').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.c)===result.c)));
  }
  function loadStep(index){
    step=index;const chosen=api.STEPS[step];write(chosen.state);
    $('step-title').textContent=chosen.title;$('prediction').textContent=chosen.prompt;
    $('try-change').textContent=chosen.action;$('explanation').hidden=true;
    $('tour-state').textContent='The experiment is at its starting state. Make a prediction before revealing the explanation.';
    document.querySelectorAll('#steps button').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===step)));
    render();
  }
  function edited(){
    $('explanation').hidden=true;
    $('tour-state').textContent='You are exploring custom settings. The experiment action restores its starting lists and controls before applying its prescribed change.';
    render();
  }
  api.STEPS.forEach((s,i)=>{
    const b=cell('button',s.title);b.type='button';b.setAttribute('aria-pressed','false');
    b.addEventListener('click',()=>loadStep(i));$('steps').append(b);
  });
  for(const c of [0,1,10,60,100]){
    const b=cell('button',`c = ${c}`);b.type='button';b.dataset.c=String(c);
    b.addEventListener('click',()=>{fields.c.value=c;edited();});$('presets').append(b);
  }
  Object.values(fields).forEach(el=>el.addEventListener('input',edited));
  $('try-change').addEventListener('click',()=>{
    const s=api.STEPS[step];write({...s.state,...s.change});render();
    $('explanation').textContent=s.explanation;$('explanation').hidden=false;
    $('tour-state').textContent='Prescribed experiment shown. Choose its step button again to restore the starting state.';
  });
  $('reset').addEventListener('click',()=>loadStep(0));
  loadStep(0);$('static-example').hidden=true;$('interactive').hidden=false;
})();
