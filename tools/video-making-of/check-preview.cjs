/* Verify the completed retrospective in a real browser. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
if (!process.env.MAKINGOF_NODE_MODULES) throw Error('Set MAKINGOF_NODE_MODULES to the bundled node_modules directory.');
const req = createRequire(path.join(path.resolve(process.env.MAKINGOF_NODE_MODULES), '../package.json'));
const {chromium} = req('playwright');
const out = path.resolve(__dirname, '../../outputs/video-making-of');
const base = process.env.MAKINGOF_PREVIEW_URL || 'http://127.0.0.1:8820';
const episode = JSON.parse(fs.readFileSync(path.join(__dirname, 'script.json'), 'utf8')).episode;

(async () => {
  const browser = await chromium.launch({channel:'msedge', headless:true, args:['--autoplay-policy=no-user-gesture-required']});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:960}});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(base+'/preview.html');
    assert.equal(await page.locator('video').count(), 1);
    const timeline = JSON.parse(fs.readFileSync(path.join(out, episode.id, 'timeline.json'), 'utf8'));
    const playback = await page.locator('video').evaluate(async video => {
      const wait = (target, event) => new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(Error('Timed out: '+event)), 25000);
        target.addEventListener(event, () => {clearTimeout(timer); resolve();}, {once:true});
      });
      video.muted = true;
      if (video.readyState < 1) await wait(video, 'loadedmetadata');
      const playing = wait(video, 'playing');
      await video.play(); await playing; video.pause();
      const seeked = wait(video, 'seeked');
      video.currentTime = video.duration*.64; await seeked;
      const track = video.querySelector('track');
      const loaded = track.readyState === 2 ? Promise.resolve() : wait(track, 'load');
      track.track.mode = 'hidden'; await loaded;
      return {width:video.videoWidth, height:video.videoHeight, duration:video.duration,
              seekedTo:video.currentTime, error:video.error?.message || null,
              captions:Array.from(track.track.cues, c => c.text)};
    });
    assert.equal(playback.width, 1920); assert.equal(playback.height, 1080);
    assert.ok(Math.abs(playback.duration-timeline.duration)<.15);
    assert.ok(playback.seekedTo>timeline.duration*.6);
    assert.equal(playback.error, null);
    assert.deepEqual(playback.captions, timeline.cues.map(c => c.text));
    const range = await page.request.get(`${base}/${episode.id}/${episode.id}.mp4`, {headers:{Range:'bytes=0-1023'}});
    assert.equal(range.status(),206); assert.equal((await range.body()).length,1024);
    await page.locator('video').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(out,'player-desktop.png')});
    for (const width of [390,768,1280]) {
      await page.setViewportSize({width,height:844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth));
    }
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(() => scrollTo(0,0));
    await page.screenshot({path:path.join(out,'player-mobile.png')});
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'player-verification.json'),JSON.stringify({playback,byteRange:'passed',responsiveWidths:[390,768,1280],pageErrors:errors},null,2));
    console.log('PASS: playback, seeking, all caption text, byte ranges, and desktop/mobile layout.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
