/* Real playback, caption loading, seeking, and responsive gallery checks. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
if (!process.env.CHAPTER13_NODE_MODULES) throw Error('Set CHAPTER13_NODE_MODULES to the bundled node_modules path.');
const dependencyRequire = createRequire(path.join(path.resolve(process.env.CHAPTER13_NODE_MODULES), '../package.json'));
const {chromium} = dependencyRequire('playwright');
const out = path.resolve(__dirname, '../../outputs/chapter-13-videos');
const base = process.env.CHAPTER13_PREVIEW_URL || 'http://127.0.0.1:8813';
const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'episodes.json'), 'utf8'));

(async () => {
  const browser = await chromium.launch({channel:'msedge', headless:true, args:['--autoplay-policy=no-user-gesture-required']});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:960}});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(base+'/preview.html');
    assert.equal(await page.locator('video').count(), 3);
    const results = [];
    for (let i=0; i<3; i++) {
      const element = page.locator('video').nth(i);
      const timeline = JSON.parse(fs.readFileSync(path.join(out, config.episodes[i].id, 'timeline.json'), 'utf8'));
      const playback = await element.evaluate(async video => {
        const wait = (target, event) => new Promise((resolve, reject) => {
          const timer = setTimeout(() => reject(Error('Timed out: '+event)), 25000);
          target.addEventListener(event, () => {clearTimeout(timer); resolve();}, {once:true});
        });
        video.muted = true;
        if (video.readyState < 1) await wait(video, 'loadedmetadata');
        const playing = wait(video, 'playing');
        await video.play(); await playing;
        video.pause();
        const seeked = wait(video, 'seeked');
        video.currentTime = video.duration*.64;
        await seeked;
        const track = video.querySelector('track');
        const loaded = track.readyState===2 ? Promise.resolve() : wait(track, 'load');
        track.track.mode='hidden';
        await loaded;
        const cue = track.track.cues[0];
        return {width:video.videoWidth, height:video.videoHeight, duration:video.duration,
                seekedTo:video.currentTime, error:video.error?.message || null,
                captions:track.track.cues.length, firstCaption:cue.text};
      });
      assert.equal(playback.width, 1920); assert.equal(playback.height, 1080);
      assert.ok(Math.abs(playback.duration-timeline.duration)<.15);
      assert.ok(playback.seekedTo>timeline.duration*.6);
      assert.equal(playback.error, null);
      assert.equal(playback.captions, timeline.cues.length);
      assert.equal(playback.firstCaption, timeline.cues[0].text);
      const url = `${base}/${config.episodes[i].id}/${config.episodes[i].id}.mp4`;
      const range = await page.request.get(url, {headers:{Range:'bytes=0-1023'}});
      assert.equal(range.status(), 206); assert.equal((await range.body()).length,1024);
      await element.scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out, `player-${i+1}.png`)});
      results.push({film:config.episodes[i].id,...playback,byteRange:'passed'});
    }
    for (const width of [390, 768, 1280]) {
      await page.setViewportSize({width,height:844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth<=innerWidth));
    }
    await page.evaluate(() => scrollTo(0,0));
    await page.screenshot({path:path.join(out,'player-gallery.png')});
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(out,'player-verification.json'),JSON.stringify({results,responsiveWidths:[390,768,1280],pageErrors:errors},null,2));
    console.log('PASS: all three videos play, seek, load exact captions, support byte ranges, and fit desktop/mobile widths.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
