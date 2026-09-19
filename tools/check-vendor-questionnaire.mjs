// Browser behaviour, layout and four print variants for visual QA.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const modules=process.env.QUESTIONNAIRE_NODE_MODULES;
if (!modules) throw new Error('Set QUESTIONNAIRE_NODE_MODULES to bundled node_modules.');
const require=createRequire(path.join(path.resolve(modules),'../package.json'));
const {chromium}=require('playwright');
const out=path.join(root,'outputs/vendor-questionnaire');
await fs.mkdir(out,{recursive:true});
const server=http.createServer(async (req,res)=>{
  try {
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const file=path.resolve(root,'.'+pathname);
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const bytes=await fs.readFile(file);
    res.writeHead(200,{'Content-Type':file.endsWith('.html')?'text/html; charset=utf-8':'text/plain'});res.end(bytes);
  } catch {res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try {
  browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1280,height:960}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const url=`http://127.0.0.1:${server.address().port}/vendor-questionnaire.html`;
  await page.goto(url);
  assert.equal(await page.locator('.question:visible').count(),19);
  assert.equal(await page.locator('input:not([type=checkbox]),textarea').count(),0);
  await page.screenshot({path:path.join(out,'desktop.png')});
  await page.locator('#q01').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'desktop-question.png')});
  await page.evaluate(()=>{window.print=()=>{window.printInvoked=true;};});
  await page.getByRole('button',{name:'Print selected sections'}).click();
  assert.equal(await page.evaluate(()=>window.printInvoked),true);
  const variants=[['core',false,false,19],['ranking',true,false,23],['rag',false,true,26],['both',true,true,30]];
  for (const [name,e,g,count] of variants) {
    await page.locator('#include-e').setChecked(e);
    await page.locator('#include-g').setChecked(g);
    assert.equal(await page.locator('.question:visible').count(),count);
    const summary=await page.locator('#selection-summary').innerText();
    assert.equal(summary.includes('Ranking methods'),e);
    assert.equal(summary.includes('Generated answers'),g);
    await page.emulateMedia({media:'print'});
    assert.equal(await page.locator('.question:visible').count(),count);
    await page.pdf({path:path.join(out,`${name}.pdf`),preferCSSPageSize:true,printBackground:true});
    await page.emulateMedia({media:'screen'});
  }
  // Keyboard toggles must work, and disabling optional sections must restore core.
  await page.locator('#include-e').focus();await page.keyboard.press('Space');
  await page.locator('#include-g').focus();await page.keyboard.press('Space');
  assert.equal(await page.locator('.question:visible').count(),19);
  await page.setViewportSize({width:390,height:844});
  await page.goto(url);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile page overflows');
  await page.screenshot({path:path.join(out,'mobile.png')});
  await page.locator('#q01').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'mobile-question.png')});
  await page.locator('#include-g').check();
  await page.locator('#g01').scrollIntoViewIfNeeded();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Optional section overflows');
  await page.screenshot({path:path.join(out,'mobile-rag.png')});
  const noJS=await browser.newPage({javaScriptEnabled:false});await noJS.goto(url);
  assert.equal(await noJS.locator('.question:visible').count(),19);await noJS.close();
  assert.deepEqual(errors,[]);
  console.log('PASS: all four section selections, keyboard controls, print button, no-JS core and desktop/mobile layout.');
} finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
