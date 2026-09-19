import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
if(!process.env.DIGEST_NODE_MODULES)throw new Error('Set DIGEST_NODE_MODULES to the Playwright node_modules directory.');
const require=createRequire(path.join(path.resolve(process.env.DIGEST_NODE_MODULES),'../package.json'));
const {chromium}=require('playwright');
const out=path.join(root,'outputs/digest');await fs.mkdir(out,{recursive:true});
const server=http.createServer(async(req,res)=>{
  try{
    const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const bytes=await fs.readFile(file);
    res.writeHead(200,{'Content-Type':{'.html':'text/html; charset=utf-8','.css':'text/css'}[path.extname(file)]||'application/octet-stream'});res.end(bytes);
  }catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try{
  browser=await chromium.launch({channel:'msedge',headless:true});
  const base=`http://127.0.0.1:${server.address().port}`;
  const page=await browser.newPage({viewport:{width:1280,height:960},javaScriptEnabled:false});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'/read-this-first.html');
  assert.equal(await page.locator('.excerpt').count(),20);
  assert.equal(await page.locator('.chapter-close').count(),15);
  assert.ok(await page.locator('.skip-link').isVisible());
  await page.keyboard.press('Tab');
  assert.equal(await page.locator(':focus').textContent(),'Skip to the digest');
  await page.keyboard.press('Enter');
  assert.equal(new URL(page.url()).hash,'#main');
  await page.goto(base+'/read-this-first.html');
  await page.screenshot({path:path.join(out,'desktop-top.png')});
  for(const id of ['problem','foundations','mechanisms','practice','next-action']){
    await page.locator('#'+id).evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));
    await page.screenshot({path:path.join(out,`desktop-${id}.png`)});
  }
  await page.locator('.contents a[href="#mechanisms"]').click();
  assert.equal(new URL(page.url()).hash,'#mechanisms');
  await page.locator('#puzzle-verdicts .claim-links summary').click();
  assert.ok(await page.locator('#puzzle-verdicts a[href*="#claim-scite-nonsense-query"]').isVisible());
  await page.setViewportSize({width:390,height:844});
  for(const id of ['problem','mechanisms','next-action']){
    await page.locator('#'+id).evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.screenshot({path:path.join(out,`mobile-${id}.png`)});
  }
  await page.emulateMedia({media:'print'});
  await page.setViewportSize({width:1000,height:1200});
  await page.locator('#foundations').evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));
  await page.screenshot({path:path.join(out,'print.png')});
  assert.ok(await page.locator('#chapter-15').isVisible());
  const offline=await browser.newPage({javaScriptEnabled:false});
  await offline.route('http://**/*',r=>r.abort());await offline.route('https://**/*',r=>r.abort());
  await offline.goto(pathToFileURL(path.join(root,'read-this-first.html')).href);
  assert.equal(await offline.locator('.excerpt').count(),20);
  await offline.locator('.contents a[href="#practice"]').click();
  assert.equal(new URL(offline.url()).hash,'#practice');
  assert.deepEqual(errors,[]);
  console.log('PASS: desktop, mobile, keyboard, source evidence disclosure, print CSS, no-JavaScript and offline digest.');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
