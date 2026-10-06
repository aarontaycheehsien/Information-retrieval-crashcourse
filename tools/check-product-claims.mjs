// No-JavaScript, keyboard, mobile and print-media QA. No external requests needed.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const modules=process.env.CLAIMS_NODE_MODULES;
if(!modules) throw new Error('Set CLAIMS_NODE_MODULES to bundled node_modules.');
const require=createRequire(path.join(path.resolve(modules),'../package.json'));
const {chromium}=require('playwright');
const out=path.join(root,'outputs/product-claims');
await fs.mkdir(out,{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(root,'data/product-claims.json'),'utf8'));
const server=http.createServer(async(req,res)=>{
  try {
    const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const bytes=await fs.readFile(file);
    res.writeHead(200,{'Content-Type':file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.json')?'application/json':'application/octet-stream'});
    res.end(bytes);
  } catch {res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try {
  browser=await chromium.launch({channel:'msedge',headless:true});
  const base=`http://127.0.0.1:${server.address().port}`;
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  await page.route('**/*',route=>route.request().url().startsWith(base)?route.continue():route.abort());
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/search-textbook.html#product-evidence-currency');
  assert.equal(await page.locator('.claim-entry').count(),data.claims.length);
  await page.locator('#product-evidence-currency').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'register-desktop.png')});
  const claim=page.locator('#claim-primo-candidate-budget');
  await claim.locator('summary').focus(); await page.keyboard.press('Enter');
  assert.ok(await claim.locator('details').getAttribute('open')!==null);
  await claim.scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'claim-desktop.png')});
  assert.equal((await page.request.get(base+'/data/product-claims.json')).status(),200);
  await page.emulateMedia({media:'print'});
  await claim.scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'claim-print.png')});
  // Closed disclosure content must also be exposed by print styling in this renderer.
  await claim.locator('details').evaluate(e=>e.open=false);
  assert.ok(await claim.locator('details p').first().evaluate(e=>e.getBoundingClientRect().height>0));
  await page.emulateMedia({media:'screen'});
  await page.setViewportSize({width:390,height:844});
  await page.goto(base+'/search-textbook.html#claim-primo-candidate-budget');
  await claim.locator('summary').click(); await claim.scrollIntoViewIfNeeded();
  assert.ok(await claim.evaluate(e=>e.getBoundingClientRect().right<=innerWidth),'Register overflows on mobile');
  await page.screenshot({path:path.join(out,'claim-mobile.png')});
  await page.goto(base+'/teaching-notes.html#currency');
  assert.equal(await page.locator('.claim-teaching-groups details').count(),9);
  await page.locator('#claims-group-pipeline summary').click();
  await page.locator('#claims-group-pipeline').scrollIntoViewIfNeeded();
  assert.ok(await page.locator('.claim-teaching-groups').evaluate(e=>e.scrollWidth<=e.clientWidth),'Notes overflow');
  await page.screenshot({path:path.join(out,'teaching-mobile.png')});
  await page.setViewportSize({width:1280,height:960});
  await page.locator('#currency').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'teaching-desktop.png')});
  await page.locator('#claims-group-pipeline').evaluate(e=>e.open=false);
  await page.emulateMedia({media:'print'});
  assert.ok(await page.locator('#claims-group-pipeline li').first().evaluate(e=>e.getBoundingClientRect().height>0));
  await page.locator('#claims-group-pipeline').evaluate(e=>e.scrollIntoView({behavior:'instant',block:'start'}));
  await page.screenshot({path:path.join(out,'teaching-print.png')});
  await page.emulateMedia({media:'screen'});
  const noJS=await browser.newPage({javaScriptEnabled:false,viewport:{width:1280,height:960}});
  await noJS.route('**/*',route=>route.request().url().startsWith(base)?route.continue():route.abort());
  await noJS.goto(base+'/search-textbook.html#claim-primo-candidate-budget');
  const staticClaim=noJS.locator('#claim-primo-candidate-budget');
  await staticClaim.locator('summary').focus(); await noJS.keyboard.press('Enter');
  assert.ok(await staticClaim.locator('details').getAttribute('open')!==null);
  // Avoid smooth-scroll stability polling across the long book in no-JS mode.
  await staticClaim.evaluate(e=>e.scrollIntoView({behavior:'instant',block:'start'}));
  await noJS.screenshot({path:path.join(out,'claim-nojs.png')});
  assert.deepEqual(errors,[]);
  console.log('PASS: register, nine teaching groups, keyboard, JSON download, desktop/mobile, print media and no-JS.');
} finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
