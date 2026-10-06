// Build both public workbooks from one definition. See tools/README.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'outputs', 'evaluation-kit');
const modules = process.env.EVALUATION_NODE_MODULES;
if (!modules) throw new Error('Set EVALUATION_NODE_MODULES to the bundled runtime node_modules directory.');
await fs.mkdir(out, { recursive: true });
try { await fs.symlink(path.resolve(modules), path.join(out, 'node_modules'), 'junction'); }
catch (error) { if (error.code !== 'EEXIST') throw error; }
const require = createRequire(path.join(out, 'package.json'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const fixture = JSON.parse(await fs.readFile(path.join(root, 'tools/fixtures/evaluation-kit.json'), 'utf8'));
const QUERY_ROWS = 50;
const RECORD_ROWS = 100;
const first = 6;
const lastQuery = first + QUERY_ROWS - 1;
const lastRecord = first + RECORD_ROWS - 1;
const colour = { ink: '#17201F', header: '#1D5B59', input: '#FFF4D6', calc: '#EDF2F0', error: '#FCE5DF', muted: '#596462' };
const col = n => { let s = ''; for (; n; n = Math.floor((n - 1) / 26)) s = String.fromCharCode(65 + (n - 1) % 26) + s; return s; };
// COUNTIFS criteria must treat identifier punctuation literally, including * and ?.
const exact = ref => `'='&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(${ref},"~","~~"),"*","~*"),"?","~?")`.replace("'='", '"="');
const rc = (q, extra = '') => `COUNTIFS(RecordData[Query ID],${exact(q)}${extra})`;
const sum = (name, q) => `SUMIFS(RecordData[${name}],RecordData[Query ID],${exact(q)})`;
const cleanId = x => `OR(NOT(ISTEXT(${x})),TRIM(${x})<>${x})`;
const invalidRank = x => `IF(${x}="",FALSE,IF(ISNUMBER(${x}),OR(${x}<1,${x}<>INT(${x})),TRUE))`;
const numericCount = x => `IF(ISNUMBER(${x}),OR(${x}<0,${x}<>INT(${x})),TRUE)`;
const queryHeaders = ['Query ID','Information need','Relevance criteria','Probe','Query A','Filters A','Query B','Filters B','Capture depth A','Captured records A','Complete A','Capture depth B','Captured records B','Complete B','Explanation','Alternatives','Next check','Transformed query A or unknown','Transformed query B or unknown','Capture status','Judgement status'];
const recordHeaders = ['Query ID','Record ID','Citation or link','Judgement','Evidence or notes','Seed','Rank A','Rank B','Row status','In A at k','In B at k','Relevant A','Relevant B','Unjudged at k','Seed A','Seed B','Seed total'];
const comparisonHeaders = ['Query ID','Probe','Status','Records A at k','Records B at k','Relevant A','Relevant B','k','Precision A','Precision B','Precision B minus A','Seeds listed','Seeds A at k','Seeds B at k','Seed recovery A','Seed recovery B','Recovery B minus A'];
const runHeaders = ['Run','Product and mode','Run date','Model or unknown','Index or unknown','Change being tested','Saved exports','Unavailable details'];

function makeSheet(wb, name, title, note, headers, count, widths) {
  const sh = wb.worksheets.add(name);
  sh.showGridLines = false;
  sh.getRange(`A1:${col(headers.length)}${first + count - 1}`).format.font = { name: 'Arial', size: 11, color: colour.ink };
  sh.getRange('A2').values = [[title]];
  sh.getRange('A2').format.font = { name: 'Arial', size: 16, bold: true, color: colour.ink };
  sh.getRange('A3').values = [[note]];
  sh.getRange('A3').format.font = { name: 'Arial', size: 10, color: colour.muted };
  sh.getRange(`A5:${col(headers.length)}5`).values = [headers];
  sh.getRange(`A5:${col(headers.length)}5`).format = { fill: colour.header, font: { name: 'Arial', size: 11, color: '#FFFFFF', bold: true }, wrapText: true, rowHeight: 36, verticalAlignment: 'center', horizontalAlignment: 'center' };
  sh.getRange(`A6:${col(headers.length)}${first + count - 1}`).format = { rowHeight: 32, verticalAlignment: 'center' };
  widths.forEach((width, i) => { sh.getRange(`${col(i + 1)}1:${col(i + 1)}${first + count - 1}`).format.columnWidth = width; });
  sh.freezePanes.freezeRows(5);
  sh.freezePanes.freezeColumns(1);
  return sh;
}

export function buildWorkbook(example = false) {
  const wb = Workbook.create();
  const c = makeSheet(wb, 'Comparison', 'Local retrieval evaluation', 'Fixed denominator k. Seed recovery is not complete recall. Inputs are pale yellow; calculations are grey.', comparisonHeaders, QUERY_ROWS, [15,26,45,15,15,14,14,8,15,15,15,13,14,14,19,19,15]);
  const q = makeSheet(wb, 'Queries', 'Define and record each query', 'Use one ID per need. Complete means captured through the stated depth, even for a short or empty result list.', queryHeaders, QUERY_ROWS, [15,45,48,27,35,25,35,25,15,17,14,15,17,14,38,38,38,38,38,45,38]);
  const r = makeSheet(wb, 'Records', 'Pool records and judge once', 'One row per query–record pair. Keep original ranks. Blank rank = absent from the captured list. Blank judgement = unjudged.', recordHeaders, RECORD_ROWS, [15,17,55,19,48,12,12,12,39,13,13,13,13,17,12,12,12]);
  const runs = makeSheet(wb, 'Runs', 'Record the two search runs', 'Use YYYY-MM-DD dates. Save original exports separately. Describe unknown settings explicitly.', runHeaders, 2, [10,36,17,30,30,45,45,45]);
  c.tabColor = colour.header;
  for (const [sh, range] of [[q,`A6:S${lastQuery}`],[r,`A6:H${lastRecord}`],[runs,'A6:H7']]) sh.getRange(range).format.fill = colour.input;
  for (const [sh, range] of [[c,`A6:Q${lastQuery}`],[q,`T6:U${lastQuery}`],[r,`I6:Q${lastRecord}`]]) sh.getRange(range).format.fill = colour.calc;
  q.getRange(`B6:H${lastQuery}`).format.wrapText = true;
  q.getRange(`O6:U${lastQuery}`).format.wrapText = true;
  q.getRange(`A6:U${lastQuery}`).format.rowHeight = 64;
  r.getRange(`C6:E${lastRecord}`).format.wrapText = true;
  r.getRange(`A6:Q${lastRecord}`).format.rowHeight = 48;
  c.getRange(`B6:C${lastQuery}`).format.wrapText = true;
  c.getRange(`A6:Q${lastQuery}`).format.rowHeight = 48;
  runs.getRange('B6:H7').format.wrapText = true;
  runs.getRange('A6:H7').format.rowHeight = 82;
  runs.getRange('C6:C7').setNumberFormat('yyyy-mm-dd');
  runs.getRange('A4').values = [['Guide: https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/evaluation-kit.html']];
  for (const sh of [q,r]) sh.getRange(`A6:B${sh === q ? lastQuery : lastRecord}`).setNumberFormat('@');
  c.getRange('A4').values = [['Cutoff k']];
  c.getRange('B4').values = [[10]];
  c.getRange('B4').format.fill = colour.input;
  c.getRange('B4').dataValidation = { rule: { type: 'list', values: ['10','20'] } };
  c.getRange('C4').values = [['Choose before collecting; see the guide for setup and extension.']];
  c.getRange('L4').values = [['Unassigned record errors']];
  c.getRange('N4').formulas = [['=COUNTIFS(RecordData[Row status],"Missing query ID")+COUNTIFS(RecordData[Row status],"Unknown query ID")']];
  // Tables exist before formulas that reference them.
  q.tables.add(`A5:U${lastQuery}`, true, 'QueryData');
  r.tables.add(`A5:Q${lastRecord}`, true, 'RecordData');
  c.tables.add(`A5:Q${lastQuery}`, true, 'ComparisonData');
  runs.tables.add('A5:H7', true, 'RunData');
  for (const sh of [c,q,r,runs]) sh.tables.items[0].showFilterButton = true;
  runs.getRange('A6:A7').values = [['A'],['B']];
  for (const range of [`K6:K${lastQuery}`,`N6:N${lastQuery}`]) q.getRange(range).dataValidation = { rule: { type: 'list', values: ['Yes','No'] } };
  r.getRange(`D6:D${lastRecord}`).dataValidation = { rule: { type: 'list', values: ['Relevant','Not relevant','Unjudged'] } };
  r.getRange(`F6:F${lastRecord}`).dataValidation = { rule: { type: 'list', values: ['Yes','No'] } };
  for (const name of ['I','L']) q.getRange(`${name}6:${name}${lastQuery}`).dataValidation = { rule: { type: 'list', values: ['10','20'] } };
  for (const name of ['J','M']) q.dataValidations.add({ range:`${name}6:${name}${lastQuery}`,rule:{type:'whole',operator:'between',formula1:0,formula2:20} });
  for (const name of ['G','H']) r.dataValidations.add({ range:`${name}6:${name}${lastRecord}`,rule:{type:'whole',operator:'between',formula1:1,formula2:20} });
  for (let row = first; row <= lastRecord; row++) {
    const a=`A${row}`, b=`B${row}`, d=`D${row}`, f=`F${row}`, g=`G${row}`, h=`H${row}`;
    const dupRank = (rank,name) => `IF(${rank}="",FALSE,COUNTIFS(RecordData[Query ID],${exact(a)},RecordData[${name}],${rank})>1)`;
    const errors = [
      [`${a}=""`, 'Missing query ID'],
      [`COUNTIFS(QueryData[Query ID],${exact(a)})=0`, 'Unknown query ID'],
      [`${b}=""`, 'Missing record ID'],
      [`OR(${cleanId(a)},${cleanId(b)})`, 'IDs must be text without outer spaces'],
      [`COUNTIFS(RecordData[Query ID],${exact(a)},RecordData[Record ID],${exact(b)})>1`, 'Duplicate record ID'],
      [`OR(${invalidRank(g)},${invalidRank(h)})`, 'Invalid rank'],
      [`OR(${dupRank(g,'Rank A')},${dupRank(h,'Rank B')})`, 'Duplicate rank'],
      [`AND(${f}<>"",${f}<>"Yes",${f}<>"No")`, 'Invalid seed flag'],
      [`AND(${d}<>"",${d}<>"Relevant",${d}<>"Not relevant",${d}<>"Unjudged")`, 'Invalid judgement'],
      [`AND(${f}="Yes",${d}="Not relevant")`, 'Seed marked not relevant'],
      [`AND(${g}="",${h}="",${f}<>"Yes")`, 'Absent record must be a seed']
    ];
    let status='"OK"'; for (const [test,msg] of errors.reverse()) status=`IF(${test},"${msg}",${status})`;
    r.getRange(`I${row}:Q${row}`).formulas = [[
      `=IF(COUNTA(A${row}:H${row})=0,"",${status})`,
      `=IF(AND(ISNUMBER(${g}),${g}>=1,${g}<=Comparison!$B$4),1,0)`,
      `=IF(AND(ISNUMBER(${h}),${h}>=1,${h}<=Comparison!$B$4),1,0)`,
      `=IF(AND(J${row}=1,${d}="Relevant"),1,0)`,
      `=IF(AND(K${row}=1,${d}="Relevant"),1,0)`,
      `=IF(AND(OR(J${row}=1,K${row}=1),${d}<>"Relevant",${d}<>"Not relevant"),1,0)`,
      `=IF(AND(J${row}=1,${f}="Yes"),1,0)`,
      `=IF(AND(K${row}=1,${f}="Yes"),1,0)`,
      `=IF(${f}="Yes",1,0)`
    ]];
  }
  for (let row = first; row <= lastQuery; row++) {
    const id=`A${row}`;
    const errors = [
      [`OR(${cleanId(id)},COUNTIFS(QueryData[Query ID],${exact(id)})<>1)`, 'Fix duplicate or invalid query ID'],
      [`B${row}=""`, 'Write the information need'], [`C${row}=""`, 'Write relevance criteria'],
      [`OR(E${row}="",G${row}="")`, 'Record both exact queries'],
      [`NOT(OR(Comparison!$B$4=10,Comparison!$B$4=20))`, 'Choose cutoff 10 or 20'],
      [`Comparison!$N$4>0`, 'Fix unassigned Records rows'],
      [`${rc(id,',RecordData[Row status],"<>OK"')}>0`, 'Fix Records row errors'],
      [`OR(K${row}<>"Yes",N${row}<>"Yes")`, 'Confirm both captures complete'],
      [`OR(NOT(ISNUMBER(I${row})),NOT(ISNUMBER(L${row})),NOT(OR(I${row}=10,I${row}=20)),NOT(OR(L${row}=10,L${row}=20)))`, 'Record capture depths (10 or 20)'],
      [`OR(I${row}<Comparison!$B$4,L${row}<Comparison!$B$4)`, 'Extend capture to the selected cutoff'],
      [`OR(${numericCount(`J${row}`)},${numericCount(`M${row}`)})`, 'Enter captured counts, including zero'],
      [`OR(${rc(id,',RecordData[Rank A],">0"')}<>J${row},${rc(id,',RecordData[Rank B],">0"')}<>M${row})`, 'Captured counts disagree with Records'],
      [`OR(${rc(id,`,RecordData[Rank A],">"&I${row}`)}>0,${rc(id,`,RecordData[Rank B],">"&L${row}`)}>0)`, 'Rank exceeds recorded capture depth']
    ];
    let status='"Ready"'; for (const [test,msg] of errors.reverse()) status=`IF(${test},"${msg}",${status})`;
    q.getRange(`T${row}:U${row}`).formulas = [[`=IF(${id}="","",${status})`, `=IF(${id}="","",IF(${sum('Unjudged at k',id)}>0,"Judge all pooled records at k","Judged"))`]];
    const qid=`Queries!A${row}`;
    const queryValue = column => `INDEX(QueryData[${column}],MATCH(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(${id},"~","~~"),"*","~*"),"?","~?"),QueryData[Query ID],0))`;
    const captureStatus = queryValue('Capture status');
    const judgementStatus = queryValue('Judgement status');
    c.getRange(`A${row}:Q${row}`).formulas = [[
      `=IF(${qid}="","",${qid})`, `=IF(A${row}="","",${queryValue('Probe')})`,
      `=IF(A${row}="","",IF(${captureStatus}<>"Ready",${captureStatus},IF(${judgementStatus}<>"Judged",${judgementStatus},"Ready")))`,
      `=IF(A${row}="","",${sum('In A at k',id)})`, `=IF(A${row}="","",${sum('In B at k',id)})`,
      `=IF(C${row}<>"Ready","",${sum('Relevant A',id)})`, `=IF(C${row}<>"Ready","",${sum('Relevant B',id)})`,
      `=IF(A${row}="","",$B$4)`,
      `=IF(C${row}<>"Ready","",F${row}/H${row})`, `=IF(C${row}<>"Ready","",G${row}/H${row})`,
      `=IF(C${row}<>"Ready","",J${row}-I${row})`,
      `=IF(A${row}="","",${sum('Seed total',id)})`,
      `=IF(A${row}="","",IF(${captureStatus}<>"Ready","",${sum('Seed A',id)}))`,
      `=IF(A${row}="","",IF(${captureStatus}<>"Ready","",${sum('Seed B',id)}))`,
      `=IF(A${row}="","",IF(${captureStatus}<>"Ready","",IF(L${row}=0,"No seeds specified",M${row}/L${row})))`,
      `=IF(A${row}="","",IF(${captureStatus}<>"Ready","",IF(L${row}=0,"No seeds specified",N${row}/L${row})))`,
      `=IF(A${row}="","",IF(OR(${captureStatus}<>"Ready",L${row}=0),"",P${row}-O${row}))`
    ]];
  }
  c.getRange(`I6:K${lastQuery}`).setNumberFormat('0.00');
  c.getRange(`O6:Q${lastQuery}`).setNumberFormat('0.00');
  for (const range of [`K6:K${lastQuery}`,`Q6:Q${lastQuery}`]) c.getRange(range).conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:colour.error,font:{bold:true,color:'#8A2D20'}}});
  c.getRange(`C6:C${lastQuery}`).conditionalFormats.addCustom('AND($A6<>"",$C6<>"Ready")',{fill:colour.error});
  r.getRange(`I6:I${lastRecord}`).conditionalFormats.addCustom('AND($I6<>"",$I6<>"OK")',{fill:colour.error});
  if (example) {
    q.getRange('A6:S6').values = [[ 'EX01','Recover the stipulated relevant records in Figure 14.1.','Relevant: A–J. Not relevant: K–T. These labels are stipulated.','Controlled ranking example','Same stipulated need','None','Same stipulated need','None',20,20,'Yes',20,20,'Yes','Reranking moves relevant records into the first ten.','No live product or causal diagnosis is claimed.','Try k=20: both lists contain the same records.','Not applicable: controlled example','Not applicable: controlled example' ]];
    r.getRange('A6:H25').values = [...fixture.before].sort().map(id => ['EX01',id,fixture.source,fixture.relevant.includes(id)?'Relevant':'Not relevant','Stipulated label in Figure 14.1',fixture.seeds.includes(id)?'Yes':'No',fixture.before.indexOf(id)+1,fixture.after.indexOf(id)+1]);
    runs.getRange('B6:H7').values = [ ['Controlled example: before','Not a live run','Not applicable','Same stipulated 20 records','Baseline ranking',fixture.source,'No live product observations'], ['Controlled example: after','Not a live run','Not applicable','Same stipulated 20 records','Reranking only; no additional candidates',fixture.source,'Seed subset chosen for the kit: A, C, E, G, J'] ];
    r.getRange('A4').values = [['Source: Figure 14.1. Seed subset A, C, E, G, J is an explicit teaching addition.']];
  } else {
    for (let i=0;i<fixture.probes.length;i++) {
      const [id,need,probe]=fixture.probes[i];
      q.getRange(`A${first+i}:D${first+i}`).values = [[id,need,null,probe]];
    }
    r.getRange('A4').values = [['Seed = Yes only for records selected before inspecting the comparison. Include missed seeds with both ranks blank.']];
  }
  return wb;
}

export async function buildAll() {
  await fs.mkdir(path.join(root,'downloads'),{recursive:true});
  for (const [name,example] of [['evaluation-template',false],['evaluation-worked-example',true]]) {
    const wb=buildWorkbook(example);
    wb.recalculate();
    const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:12},summary:name});
    console.log(scan.ndjson);
    const xlsx=await SpreadsheetFile.exportXlsx(wb);
    await xlsx.save(path.join(out,`${name}.xlsx`));
    await fs.copyFile(path.join(out,`${name}.xlsx`),path.join(root,'downloads',`${name}.xlsx`));
    // Review each sheet, including the scoring columns outside the opening view.
    const previews = [['Comparison','A2:K10'],['Seeds','L5:Q10','Comparison'],['Queries','A2:D10'],['Captures','I5:N10','Queries'],['Records','A2:I12'],['Runs','A2:H7']];
    for (const [label,range,sheet=label] of previews) {
      const preview=await wb.render({sheetName:sheet,range,scale:1,format:'png'});
      await fs.writeFile(path.join(out,`${name}-${label.toLowerCase()}.png`),new Uint8Array(await preview.arrayBuffer()));
    }
    console.log(`Built ${name}.xlsx`);
  }
}
if (process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) await buildAll();
