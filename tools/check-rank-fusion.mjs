import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
if(!process.env.RRF_NODE_MODULES)throw new Error('Set RRF_NODE_MODULES to the Playwright node_modules directory.');
const require=createRequire(path.join(path.resolve(process.env.RRF_NODE_MODULES),'../package.json'));
const {chromium}=require('playwright');
const api=require(path.join(root,'assets/rank-fusion-core.js'));
const out=path.join(root,'outputs/rank-fusion');await fs.mkdir(out,{recursive:true});
const server=http.createServer(async(req,res)=>{
  try{
    const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const bytes=await fs.readFile(file);
    res.writeHead(200,{'Content-Type':{'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript'}[path.extname(file)]||'application/octet-stream'});res.end(bytes);
  }catch{res.writeHead(404);res.end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try{
  browser=await chromium.launch({channel:'msedge',headless:true});
  const base=`http://127.0.0.1:${server.address().port}`;
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',r=>r.request().url().startsWith(base)?r.continue():r.abort());
  await page.goto(base+'/rank-fusion-lab.html');
  const order=()=>page.locator('#result-rows th').allTextContents();
  assert.deepEqual(await order(),['A','C','B','D']);
  await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').textContent(),'Skip to the lab');
  await page.keyboard.press('Enter');assert.equal(new URL(page.url()).hash,'#main');
  await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,'desktop-top.png')});
  const fields={a:'list-a',b:'list-b',c:'constant',depthA:'depth-a',depthB:'depth-b',output:'output-depth'};
  for(let i=0;i<4;i++){
    await page.locator('#list-a').fill('Changed');await page.locator('#constant').fill('99');
    await page.locator('#steps button').nth(i).click();
    for(const [key,id] of Object.entries(fields))assert.equal(await page.locator('#'+id).inputValue(),String(api.STEPS[i].state[key]));
    await page.locator('#try-change').click();
    assert.ok(await page.locator('#explanation').isVisible());
    const wanted=api.calculate({...api.STEPS[i].state,...api.STEPS[i].change});
    assert.deepEqual(await order(),wanted.visible.map(x=>x.id));
    await page.locator('#steps button').nth(i).click();
    assert.ok(await page.locator('#explanation').isHidden());
  }
  await page.locator('#steps button').nth(1).click();
  await page.locator('#constant').fill('1');await page.locator('#output-depth').fill('1');
  assert.match(await page.locator('#tie-note').textContent(),/splits a tied group/);
  await page.locator('#list-a').fill('A\nA');
  assert.match(await page.locator('#error').textContent(),/duplicate identifier/);
  assert.ok(await page.locator('#results').isHidden());
  await page.locator('#reset').click();
  await page.locator('#constant').fill('');assert.ok(await page.locator('#error').isVisible());
  await page.locator('#constant').fill('0.5');assert.ok(await page.locator('#error').isVisible());
  await page.locator('#reset').click();
  await page.locator('#list-a').fill('');await page.locator('#list-b').fill('');
  assert.match(await page.locator('#status').textContent(),/No supplied candidates/);
  await page.locator('#list-a').fill('<img src=x onerror=alert(1)>');
  assert.equal(await page.locator('#interactive img').count(),0);
  assert.equal((await order())[0],'<img src=x onerror=alert(1)>');
  await page.locator('#reset').click();
  await page.locator('#sandbox-title').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'desktop-controls.png')});
  await page.locator('#results-title').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'desktop-results.png')});
  await page.locator('#depth-b').fill('1');
  assert.deepEqual(await order(),['C','A','B']);
  assert.equal(await page.locator('#ranks-b .excluded').count(),2);
  await page.locator('#reset').click();
  for(const [key,id] of Object.entries(fields))assert.equal(await page.locator('#'+id).inputValue(),String(api.BOOK[key]));
  // All local companion URLs and source fragments exist.
  const links=await page.locator('a[href],link[href],script[src]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('href')||n.getAttribute('src')));
  for(const href of links){
    if(/^https?:/.test(href))continue;
    const u=new URL(href,base+'/rank-fusion-lab.html');
    const source=await fs.readFile(path.join(root,decodeURIComponent(u.pathname.slice(1))),'utf8');
    if(u.hash)assert.ok(source.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`),href);
  }
  await page.setViewportSize({width:390,height:844});
  for(const [name,id] of [['mobile-tour','tour-title'],['mobile-controls','sandbox-title'],['mobile-results','results-title']]){
    await page.locator('#'+id).evaluate(e=>e.scrollIntoView({block:'start'}));
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.screenshot({path:path.join(out,name+'.png')});
  }
  const touch=await browser.newPage({hasTouch:true,isMobile:true,viewport:{width:390,height:844}});
  await touch.goto(base+'/rank-fusion-lab.html');
  await touch.locator('#steps button').nth(1).tap();await touch.locator('#try-change').tap();
  assert.equal(await touch.locator('#result-rows th').first().textContent(),'C');
  await page.setViewportSize({width:1100,height:1000});await page.emulateMedia({media:'print'});
  await page.locator('#results-title').evaluate(e=>e.scrollIntoView({block:'start'}));
  assert.ok(await page.locator('#result-rows').isVisible());
  await page.screenshot({path:path.join(out,'print-results.png')});
  const nojs=await browser.newPage({javaScriptEnabled:false});
  await nojs.goto(base+'/rank-fusion-lab.html');
  assert.ok(await nojs.locator('#static-example').isVisible());assert.ok(await nojs.locator('#interactive').isHidden());
  await nojs.locator('#static-title').scrollIntoViewIfNeeded();await nojs.screenshot({path:path.join(out,'nojs.png')});
  const offline=await browser.newPage();
  await offline.route('https://**/*',r=>r.abort());await offline.route('http://**/*',r=>r.abort());
  await offline.goto(pathToFileURL(path.join(root,'rank-fusion-lab.html')).href);
  assert.equal(await offline.locator('#result-rows tr').count(),4);
  await offline.locator('#constant').fill('0');assert.ok(await offline.locator('#error').isHidden());
  assert.deepEqual(errors,[]);
  console.log('PASS: live edits, four experiments/resets, ties, errors, empty lists, text safety, links, keyboard, mobile/touch, print CSS, no-JS and offline.');
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
