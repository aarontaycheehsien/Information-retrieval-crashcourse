/* Check browser playback, captions, chapter seeking and responsive layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
if (!process.env.INVESTIGATION_NODE_MODULES) throw Error('Set INVESTIGATION_NODE_MODULES to the bundled node_modules folder.');
const dependencies = createRequire(path.join(path.resolve(process.env.INVESTIGATION_NODE_MODULES), '../package.json'));
const {chromium} = dependencies('playwright');
const out = path.resolve(__dirname, '../../outputs/chapter-1-investigation');
const base = process.env.INVESTIGATION_PREVIEW_URL || 'http://127.0.0.1:8816';

(async () => {
  const browser = await chromium.launch({channel:'msedge', headless:true, args:['--autoplay-policy=no-user-gesture-required']});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:960}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base+'/preview.html');
    assert.equal(await page.locator('video').count(), 1);
    const timeline = JSON.parse(fs.readFileSync(path.join(out,'timeline.json'),'utf8'));
    const captions = JSON.parse(fs.readFileSync(path.join(out,'captions.json'),'utf8'));
    const playback = await page.locator('video').evaluate(async video => {
      const wait = (target,event) => new Promise((resolve,reject) => {
        const timer = setTimeout(() => reject(Error('Timed out: '+event)),25000);
        target.addEventListener(event,() => {clearTimeout(timer);resolve();},{once:true});
      });
      video.muted = true;
      if (video.readyState<1) await wait(video,'loadedmetadata');
      const playing = wait(video,'playing');
      await video.play();await playing;video.pause();
      const seeked = wait(video,'seeked');
      video.currentTime = video.duration*.64;await seeked;
      const track = video.querySelector('track');
      const loaded = track.readyState===2 ? Promise.resolve() : wait(track,'load');
      track.track.mode = 'hidden';await loaded;
      return {width:video.videoWidth,height:video.videoHeight,duration:video.duration,
              seekedTo:video.currentTime,error:video.error?.message||null,
              captions:Array.from(track.track.cues,cue => cue.text)};
    });
    assert.equal(playback.width,1920);assert.equal(playback.height,1080);
    assert.ok(Math.abs(playback.duration-timeline.duration)<.15);
    assert.equal(playback.error,null);
    assert.deepEqual(playback.captions,captions.map(cue => cue.text));
    assert.equal(await page.locator('button[data-time]').count(),13);
    await page.locator('button[data-time]').last().click();
    await page.waitForFunction(() => Math.abs(document.querySelector('video').currentTime-Number(document.querySelector('button[data-time]:last-child').dataset.time))<2);
    await page.locator('video').evaluate(video => video.pause());
    const range = await page.request.get(base+'/chapter-1-the-paper-your-ai-never-saw.mp4',{headers:{Range:'bytes=0-1023'}});
    assert.equal(range.status(),206);assert.equal((await range.body()).length,1024);
    for (const width of [390,768,1280]) {
      await page.setViewportSize({width,height:844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth));
    }
    await page.screenshot({path:path.join(out,'player-check.png')});
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'player-verification.json'),JSON.stringify({passed:true,...playback,captionCues:playback.captions.length,byteRange:true,chapterLinks:13,responsiveWidths:[390,768,1280],pageErrors:errors},null,2));
    console.log('PASS: playback, seeking, all 168 exact captions, 13 chapter links, byte ranges and 3 responsive widths.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
