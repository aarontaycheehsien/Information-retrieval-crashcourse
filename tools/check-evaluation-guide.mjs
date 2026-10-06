// Headless browser smoke check and layout previews; uses bundled Playwright.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const out=path.join(root,'outputs','evaluation-kit');
const require=createRequire(path.join(out,'package.json'));
const { chromium }=require('playwright');
const server=http.createServer(async (req,res)=>{
  try {
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const file=path.resolve(root,'.'+pathname);
    if (!file.startsWith(root+path.sep)) { res.writeHead(403);res.end();return; }
    const bytes=await fs.readFile(file);
    const type=file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.xlsx')?'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':'text/plain';
    res.writeHead(200,{'Content-Type':type});res.end(bytes);
  } catch {res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try {
  browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage();
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  const base=`http://127.0.0.1:${server.address().port}`;
  for (const [label,width,height] of [['desktop',1280,900],['mobile',390,844]]) {
    await page.setViewportSize({width,height});
    await page.goto(`${base}/evaluation-kit.html`);
    assert.equal(await page.locator('h1').innerText(),'Local retrieval evaluation kit');
    assert.equal(await page.locator('a[download]').count(),2);
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${label}: horizontal page overflow`);
    await page.screenshot({path:path.join(out,`guide-${label}.png`)});
    await page.locator('#example').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(out,`guide-${label}-example.png`)});
  }
  for (const file of ['evaluation-template.xlsx','evaluation-worked-example.xlsx']) {
    const response=await page.request.get(`${base}/downloads/${file}`);
    assert.equal(response.status(),200);
    assert.equal((await response.body()).subarray(0,2).toString(),'PK');
  }
  assert.deepEqual(errors,[]);
  console.log('PASS: desktop/mobile layout, both XLSX downloads and no browser errors.');
} finally { if(browser) await browser.close();await new Promise(resolve=>server.close(resolve)); }
