"""Produce an original pop-song demo, instrumental, MIDI score and lyric player."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import subprocess
import wave

import imageio_ffmpeg
import numpy as np
import parselmouth
from scipy.signal import butter,sosfilt

import instruments
import vocals

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT/"outputs"/"textbook-pop-song"
NAME = "follow-the-evidence"
SR = instruments.SR


def run(command,log):
    result = subprocess.run(command,capture_output=True,text=True,encoding="utf-8",errors="replace")
    log.write_text(result.stdout+result.stderr,encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Command failed: {log}")
    return result.stderr


def wave_write(path,x):
    assert x.ndim==2 and x.shape[1]==2 and np.all(np.isfinite(x))
    assert np.max(np.abs(x))<=1, f"Stem would clip: {path.name}"
    with wave.open(str(path),"wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((x*32767).astype("<i2").tobytes())


def config_check(config):
    assert config["bpm"]==120 and config["key"]=="C major"
    book = (ROOT/"search-textbook.html").read_text(encoding="utf-8")
    for ref in config["sources"]:
        assert f'id="{ref.partition("#")[2]}"' in book, f"Missing source: {ref}"
    for name,phrase in config["phrases"].items():
        assert abs(sum(t[1] for t in phrase["tokens"])-7.5)<1e-8, f"Phrase does not fit: {name}"
        assert all(t[1]>0 and all(48<=n<=76 and n%12 in [0,2,4,5,7,9,11] for n in (t[2] if isinstance(t[2],list) else [t[2]])) for t in phrase["tokens"])
    for section in config["sections"]:
        assert not section["phrases"] or len(section["phrases"])*2==section["bars"]
        assert all(p in config["phrases"] for p in section["phrases"])


def timeline_for(config):
    sections = []
    cursor = 0.
    beat = 60/config["bpm"]
    for section in config["sections"]:
        length = section["bars"]*4*beat
        sections.append({**section,"start":cursor,"end":cursor+length,
                         "vocals":[{"phrase":name,"start":cursor+i*8*beat,"end":cursor+(i+1)*8*beat} for i,name in enumerate(section["phrases"])]})
        cursor += length
    return {"duration":cursor+2,"bpm":config["bpm"],"key":config["key"],"sections":sections,"bars":sum(s["bars"] for s in sections)}


def vocal_bus(config,timeline,manifest,out):
    lookup = {p["phrase"]:p for p in manifest}
    count = round(timeline["duration"]*SR)
    bus = np.zeros((count,2),np.float32)
    dry = np.zeros_like(bus)
    cues = []
    for section in timeline["sections"]:
        chorus = section["id"].startswith("chorus") or section["id"]=="final"
        for occurrence in section["vocals"]:
            report = lookup[occurrence["phrase"]]
            data = np.load(out/"sung-cache"/report["file"])
            lead = data["lead"]
            harmony = data["harmony"]
            at = occurrence["start"]
            instruments.add(dry,at,lead,1.0)
            instruments.add(bus,at,lead,1.0)
            if chorus:
                harmony_gain = .30 if section["id"]=="final" else .20
                instruments.add(bus,at+.022,harmony,harmony_gain,-.55)
                instruments.add(bus,at+.037,harmony,harmony_gain*.75,.6)
                instruments.add(bus,at+.015,lead,.10,.45)
            # Stereo dotted-eighth delays and a restrained diffuse room.
            beat = 60/config["bpm"]
            for delay,gain,pan in [(beat*.75,.13,-.65),(beat*1.5,.075,.65),(.071,.045,-.5),(.117,.04,.5)]:
                instruments.add(bus,at+delay,lead,gain,pan)
            cues.append({"start":at+report["tokens"][0]["start"],"end":at+report["tokens"][-1]["end"],
                         "section":section["id"],"phrase":occurrence["phrase"],"text":report["text"]})
    # Remove subsonic energy; tame sibilants while retaining intelligible consonants.
    bus = sosfilt(butter(2,110,btype="highpass",fs=SR,output="sos"),bus,axis=0).astype(np.float32)
    return bus,dry,cues


def stamp(seconds,separator="."):
    ms = round(seconds*1000)
    hour,ms = divmod(ms,3600000)
    minute,ms = divmod(ms,60000)
    sec,ms = divmod(ms,1000)
    return f"{hour:02d}:{minute:02d}:{sec:02d}{separator}{ms:03d}"


def player(config,timeline,cues,out):
    lyric_sections = []
    text_sections = []
    for section in timeline["sections"]:
        if not section["phrases"]:
            continue
        lines = [vocals.phrase_text(config["phrases"][p]) for p in section["phrases"]]
        text_sections.append(section["title"]+"\n"+"\n".join(lines))
        relevant = [c for c in cues if c["section"]==section["id"]]
        lyric_sections.append(f'<section><h2>{html.escape(section["title"])}</h2>'+''.join(
            f'<button class="line" data-time="{c["start"]:.3f}" data-end="{c["end"]:.3f}">{html.escape(c["text"])}</button>' for c in relevant)+"</section>")
    credits = "Original lyrics, melody and synthesized instrumental arrangement. Electronic singing synthesized from Microsoft Jenny speech using Praat PSOLA; no voice cloning."
    (out/"lyrics.txt").write_text(config["title"]+"\n\n"+"\n\n".join(text_sections)+
        f"\n\n{credits}\nCompanion to Aaron Tay's How Search Decides What You See.\n{config['book_url']}\n",encoding="utf-8")
    (out/f"{NAME}.vtt").write_text("WEBVTT\n\n"+"\n".join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n" for c in cues),encoding="utf-8")
    (out/f"{NAME}.srt").write_text("\n".join(f"{i}\n{stamp(c['start'],',')} --> {stamp(c['end'],',')}\n{c['text']}\n" for i,c in enumerate(cues,1)),encoding="utf-8")
    (out/"lyrics-timing.json").write_text(json.dumps(cues,indent=2),encoding="utf-8")
    duration = round(timeline["duration"])
    (out/"preview.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Follow the Evidence · Textbook pop song</title><style>*{{box-sizing:border-box}}body{{background:#121136;color:#f8f4df;margin:0;font:17px/1.6 system-ui}}main{{max-width:1050px;margin:auto;padding:44px 24px}}
.tag{{font-size:12px;letter-spacing:.18em;color:#63dfd0;font-weight:750}}h1{{font-size:clamp(40px,7vw,76px);line-height:1.05;letter-spacing:-.04em;margin:20px 0}}p{{color:#c3beda}}a{{color:#63dfd0}}
.deck{{padding:25px;border:1px solid #594e93;border-radius:18px;background:#24204d}}audio{{width:100%;margin-top:12px}}#play{{border:0;border-radius:30px;background:#63dfd0;color:#121136;padding:12px 28px;font:700 18px system-ui;cursor:pointer}}
.links{{display:flex;gap:17px;flex-wrap:wrap;font-size:15px}}.lyrics{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:25px}}.lyrics section{{background:#24204d;border-radius:14px;padding:20px}}h2{{font-size:15px;color:#faCA62;margin-top:0;text-transform:uppercase;letter-spacing:.1em}}
.line{{display:block;width:100%;border:0;background:transparent;color:#c3beda;font:inherit;text-align:left;padding:7px 10px;border-radius:7px;cursor:pointer}}.line:hover,.line:focus-visible{{background:#353068}}.line.active{{background:#5c45a4;color:white}}.credit{{font-size:13px}}@media(max-width:650px){{.lyrics{{grid-template-columns:1fr}}main{{padding:28px 16px}}}}</style></head>
<body><main><div class="tag">AN ORIGINAL TEXTBOOK COMPANION · SYNTH-POP DEMO</div><h1>Follow the Evidence</h1>
<p>A catchy search anthem for librarians, inspired by Aaron Tay’s <em>How Search Decides What You See</em>.</p>
<div class="deck"><button id="play">Play song</button><p>{duration//60}:{duration%60:02d} · 120 BPM · C major · Electronic sung vocals</p>
<audio id="song" controls preload="metadata" src="{NAME}.mp3"></audio>
<p class="links"><a href="{NAME}.mp3" download>Download song</a><a href="{NAME}-instrumental.mp3" download>Instrumental</a><a href="{NAME}.wav" download>WAV master</a><a href="{NAME}.mid" download>MIDI score</a><a href="lyrics.txt">Lyrics</a></p></div>
<p>Click any lyric line to hear that part. <a href="{config['book_url']}">Read the free textbook</a> · <a href="{config['intro_url']}">Start with Read This First</a></p>
<div class="lyrics">{''.join(lyric_sections)}</div><p class="credit">{credits} This is a locally produced synthetic vocal demo, with an intentionally electronic sound.
The composition accompanies the textbook and does not promise complete search coverage.</p></main>
<script>const song=document.getElementById('song'),button=document.getElementById('play'),lines=[...document.querySelectorAll('.line')];button.onclick=()=>song.paused?song.play().catch(()=>{{}}):song.pause();
song.onplay=()=>button.textContent='Pause song';song.onpause=()=>button.textContent='Play song';song.ontimeupdate=()=>lines.forEach(l=>l.classList.toggle('active',song.currentTime>=Number(l.dataset.time)&&song.currentTime<Number(l.dataset.end)));
lines.forEach(l=>l.onclick=()=>{{song.currentTime=Number(l.dataset.time);song.play().catch(()=>{{}})}});</script></body></html>''',encoding="utf-8")


def pitch_check(manifest,out):
    """Measure the rendered lead against its written melody, excluding note transitions."""
    records = []
    for record in manifest:
        values = np.load(out/"sung-cache"/record["file"])["lead"]
        sound = parselmouth.Sound(values,sampling_frequency=SR)
        pitch = sound.to_pitch_ac(time_step=.01,pitch_floor=100,pitch_ceiling=650,voicing_threshold=.35)
        errors = []
        for token in record["tokens"]:
            notes = token["notes"] if isinstance(token["notes"],list) else [token["notes"]]
            length = token["end"]-token["start"]
            edges = np.linspace(token["start"],token["end"],len(notes)+1)
            for at in np.arange(token["start"]+.055,token["end"]-.04,.01):
                if min(abs(at-edge) for edge in edges)<.055:
                    continue
                f0 = pitch.get_value_at_time(float(at))
                if not np.isfinite(f0) or f0<=0:
                    continue
                index = min(len(notes)-1,int((at-token["start"])/length*len(notes)))
                error = abs(1200*math.log2(f0/vocals.frequency(notes[index])))
                errors.append(error)
        assert len(errors)>10, f"No usable sung pitch: {record['phrase']}"
        median = float(np.median(errors))
        within = float(np.mean(np.asarray(errors)<100))
        assert median<65 and within>.65, f"Lead missed its written tune: {record['phrase']} ({median:.1f} cents, {within:.1%})"
        records.append({"phrase":record["phrase"],"median_absolute_cents_error":median,"voiced_frames_within_one_semitone":within,"measured_frames":len(errors)})
    (out/"pitch-verification.json").write_text(json.dumps({"passed":True,"phrases":records},indent=2),encoding="utf-8")
    print(f"Pitch checked: {len(records)} sung phrases match the written tune",flush=True)


def verify(path,timeline,out,ff):
    log = run([ff,"-hide_banner","-xerror","-i",str(path),"-af","ebur128=peak=true","-f","null","-"],out/f"verify-{path.stem}-{path.suffix[1:]}.log")
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS",log)[-1])
    peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",log)[-1])
    match = re.search(r"Duration: (\d+):(\d+):([\d.]+)",log)
    seconds = int(match[1])*3600+int(match[2])*60+float(match[3])
    assert abs(seconds-timeline["duration"])<.15
    assert -15<=lufs<=-13 and peak<=-1, f"Master levels failed: {lufs} LUFS; {peak} dBTP"
    assert "44100 Hz" in log and "stereo" in log
    return {"file":path.name,"duration":seconds,"integrated_lufs":lufs,"true_peak_dbfs":peak,
            "sample_rate":SR,"channels":2,"full_decode_passed":True,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=OUT)
    parser.add_argument("--prepare-only",action="store_true")
    parser.add_argument("--render-only",action="store_true")
    args = parser.parse_args()
    assert not (args.prepare_only and args.render_only)
    out = args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    config = json.loads((HERE/"song.json").read_text(encoding="utf-8"))
    config_check(config)
    ff = os.environ.get("SONG_FFMPEG") or imageio_ffmpeg.get_ffmpeg_exe()
    if args.render_only:
        manifest = json.loads((out/"singing-manifest.json").read_text(encoding="utf-8"))
        # Cached singing must match current composition and synthesis settings.
        expected = set(config["phrases"])
        assert {m["phrase"] for m in manifest}==expected
        for entry in manifest:
            phrase = config["phrases"][entry["phrase"]]
            assert entry["text"]==vocals.phrase_text(phrase)
            request = vocals.speech.request_for({"text":entry["text"]},config["voice"])
            source_key = vocals.speech.cache_dir(out,request).name
            assert entry["source_voice_cache"]==source_key, "Voice settings changed; prepare again"
            fingerprint = hashlib.sha256((json.dumps(phrase,sort_keys=True)+str(60/config["bpm"])+source_key+(HERE/"vocals.py").read_text()).encode()).hexdigest()[:20]
            assert entry["file"]==f"{entry['phrase']}-{fingerprint}.npz", "Singing code changed; prepare again"
            assert [(t["word"],t["notes"],round((t["end"]-t["start"]+.028)/(60/config["bpm"]),6)) for t in entry["tokens"]]==[(t[0],t[2],t[1]) for t in phrase["tokens"]]
    else:
        manifest = vocals.prepare(config,out,ff)
    pitch_check(manifest,out)
    if args.prepare_only:
        return
    timeline = timeline_for(config)
    print(f"Arranging {timeline['bars']} bars; {timeline['duration']:.1f}s",flush=True)
    rhythm,bass,music,events = instruments.arrange(config,timeline)
    voice,dry,cues = vocal_bus(config,timeline,manifest,out)
    assert all(0<=c["start"]<c["end"]<=timeline["duration"] for c in cues)
    assert all(a["end"]<b["start"] for a,b in zip(cues,cues[1:]))
    fade = np.minimum(np.arange(len(music))/(SR*.08),1)*np.minimum((len(music)-np.arange(len(music)))/(SR*1.7),1)
    for label,x in [("drums",rhythm),("bass",bass),("synths",music),("electronic-vocals",voice),("dry-lead",dry)]:
        wave_write(out/f"{label}.wav",x*fade[:,None])
    instrumental = rhythm+bass+music
    mix = instrumental+voice
    gain = min(1,.88/float(np.max(np.abs(mix))))
    records = []
    for suffix,track in [("",mix),("-instrumental",instrumental)]:
        raw = out/f"{NAME}{suffix}-unmastered.wav"
        master = out/f"{NAME}{suffix}.wav"
        mp3 = out/f"{NAME}{suffix}.mp3"
        wave_write(raw,(track*fade[:,None]*gain).astype(np.float32))
        run([ff,"-y","-i",str(raw),"-af","loudnorm=I=-14:TP=-2.0:LRA=7","-ar",str(SR),"-c:a","pcm_s16le",str(master)],out/f"master{suffix}.log")
        run([ff,"-y","-i",str(master),"-c:a","libmp3lame","-b:a","320k","-id3v2_version","3","-metadata",f"title={config['title']}{' (Instrumental)' if suffix else ''}",
             "-metadata","artist=Original textbook companion demo","-metadata","genre=Synth-pop","-metadata",f"comment={config['subtitle']}; synthetic electronic vocals",str(mp3)],out/f"encode{suffix}.log")
        records.extend([verify(master,timeline,out,ff),verify(mp3,timeline,out,ff)])
    instruments.midi(out/f"{NAME}.mid",config,timeline,events)
    midi_info = instruments.verify_midi(out/f"{NAME}.mid")
    (out/"midi-verification.json").write_text(json.dumps(midi_info,indent=2),encoding="utf-8")
    player(config,timeline,cues,out)
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/"song.json",HERE/"render.py",HERE/"instruments.py",HERE/"vocals.py"]}
    timeline["production_hashes"] = hashes
    (out/"timeline.json").write_text(json.dumps(timeline,indent=2),encoding="utf-8")
    (out/"verification.json").write_text(json.dumps({"passed":True,"files":records,"bpm":config["bpm"],"key":config["key"],"timed_lyric_lines":len(cues),
        "synthetic_voice":config["voice"]["name"],"singing_method":"Praat PSOLA pitch and vowel-duration manipulation","original_lyrics_melody_and_instruments":True,"midi_verified":True,"production_hashes":hashes},indent=2),encoding="utf-8")
    print(f"Completed: {out/f'{NAME}.mp3'}",flush=True)


if __name__=="__main__":
    main()
