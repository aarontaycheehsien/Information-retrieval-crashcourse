"""Turn synthetic speech into note-timed electronic singing with Praat PSOLA."""
from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import parselmouth
from parselmouth.praat import call
from scipy.signal import resample_poly

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("song_speech_cache",HERE.parent/"pick-a-card"/"narrate.py")
speech = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = speech
spec.loader.exec_module(speech)
SR = 44100


def phrase_text(phrase):
    return " ".join(token[0] for token in phrase["tokens"])+"."


def frequency(midi):
    return 440*2**((midi-69)/12)


def third(midi):
    scale = [n for n in range(36,96) if n%12 in [0,2,4,5,7,9,11]]
    return scale[scale.index(midi)+2]


def sing_word(samples,seconds,notes,harmony=False):
    """Stretch chiefly voiced portions, then replace the pitch with musical notes."""
    samples = np.pad(samples,(round(.015*SR),round(.015*SR)))
    sound = parselmouth.Sound(samples,sampling_frequency=SR)
    # Praat's duration manipulation clamps individual factors to 0.25–3.
    # Cascaded bounded passes let very short vowels sustain a musical note.
    for attempt in range(6):
        duration = sound.duration
        manipulation = call(sound,"To Manipulation",.005,75,600)
        pitch = sound.to_pitch_ac(time_step=.005,pitch_floor=75,pitch_ceiling=600)
        xs = np.linspace(0,duration,max(9,round(duration/.007)+1))
        voiced = np.array([float(np.isfinite(pitch.get_value_at_time(float(t)))) for t in xs])
        voiced = np.convolve(voiced,np.ones(5)/5,mode="same")
        if seconds <= duration*1.15 or np.trapezoid(voiced,xs) < .012:
            rates = np.full_like(xs,seconds/duration)
        else:
            # Preserve consonants while sustaining the vowels that carry the tune.
            rates = .92+(seconds-.92*duration)/np.trapezoid(voiced,xs)*voiced
        rates *= seconds/np.trapezoid(rates,xs)
        if np.min(rates)>=.26 and np.max(rates)<=2.95:
            break
        temporary = call("Create DurationTier","bounded stretch",0,duration)
        for t,rate in zip(xs,np.clip(rates,.26,2.95)):
            call(temporary,"Add point",float(t),float(rate))
        call([temporary,manipulation],"Replace duration tier")
        sound = call(manipulation,"Get resynthesis (overlap-add)")
    else:
        raise RuntimeError("Could not sustain a word within Praat duration limits")
    warped = np.r_[0,np.cumsum((rates[:-1]+rates[1:])/2*np.diff(xs))]
    assert abs(warped[-1]-seconds)<1e-6 and np.all(rates>0)
    duration_tier = call("Create DurationTier","rhythm",0,duration)
    for t,rate in zip(xs,rates):
        call(duration_tier,"Add point",float(t),float(rate))
    call([duration_tier,manipulation],"Replace duration tier")
    notes = notes if isinstance(notes,list) else [notes]
    if harmony:
        notes = [third(n) for n in notes]
    target_tier = call("Create PitchTier","melody",0,duration)
    events = np.linspace(0,seconds,len(notes)+1)
    tx = np.linspace(0,duration,max(10,round(duration/.004)+1))
    for original_at in tx:
        at = float(np.interp(original_at,xs,warped))
        index = min(len(notes)-1,int(at/max(seconds,1e-9)*len(notes)))
        midi = float(notes[index])
        # Short slides and shallow vibrato avoid discontinuities without losing tuning.
        if index and at-events[index]<.045:
            p = (at-events[index])/.045
            p = p*p*(3-2*p)
            midi = notes[index-1]+(notes[index]-notes[index-1])*p
        midi += .07*np.sin(at*2*np.pi*5.1)*min(1,at/.3)
        call(target_tier,"Add point",float(original_at),frequency(midi))
    call([target_tier,manipulation],"Replace pitch tier")
    sung = call(manipulation,"Get resynthesis (overlap-add)").values[0]
    target_count = round(seconds*SR)
    assert abs(len(sung)-target_count)<SR*.04, f"Duration manipulation drifted: {len(sung)/SR:.4f}s vs {seconds:.4f}s, source {duration:.4f}s, factor {float(np.max(rates)):.2f}"
    sung = np.pad(sung,(0,max(0,target_count-len(sung))))[:target_count].copy()
    fade = min(round(.009*SR),len(sung)//4)
    sung[:fade] *= np.linspace(0,1,fade)
    sung[-fade:] *= np.linspace(1,0,fade)
    return sung.astype(np.float32)


def prepare(config,out,ff):
    lines = [{"id":name,"scene":"song","text":phrase_text(phrase)} for name,phrase in config["phrases"].items()]
    async def synthesize():
        gate = asyncio.Semaphore(3)
        return await asyncio.gather(*(speech.synthesize(out,line,config["voice"],gate) for line in lines))
    directories = asyncio.run(synthesize())
    dest = out/"sung-cache"
    dest.mkdir(exist_ok=True)
    beat = 60/config["bpm"]
    manifest = []
    for line,directory in zip(lines,directories):
        name = line["id"]
        phrase = config["phrases"][name]
        fingerprint = hashlib.sha256((json.dumps(phrase,sort_keys=True)+str(beat)+directory.name+Path(__file__).read_text()).encode()).hexdigest()[:20]
        cache = dest/f"{name}-{fingerprint}.npz"
        if cache.exists():
            manifest.append(json.loads((cache.with_suffix(".json")).read_text(encoding="utf-8")))
            print(f"  cached singing {name}",flush=True)
            continue
        take = speech.prepare(directory,line,ff)
        samples = resample_poly(take.audio,147,160).astype(np.float32)
        # Match written tokens to TTS word events, including split contractions.
        wi = 0
        bounds = []
        for token,_,_ in phrase["tokens"]:
            need,got = speech.normalized(token),""
            start,end = None,None
            while wi<len(take.words) and len(got)<len(need):
                word = take.words[wi]
                start = word["start"] if start is None else start
                end = word["end"]
                got += speech.normalized(word["text"])
                wi += 1
            assert need==got and start is not None, f"Word alignment failed: {token}"
            bounds.append((start,end))
        assert wi==len(take.words)
        lead = np.zeros(round(8*beat*SR),np.float32)
        harmony = np.zeros_like(lead)
        cursor = .25*beat
        token_report = []
        for i,(word,beats,notes) in enumerate(phrase["tokens"]):
            a = 0 if i==0 else (bounds[i-1][1]+bounds[i][0])/2
            b = len(samples)/SR if i==len(bounds)-1 else (bounds[i][1]+bounds[i+1][0])/2
            clip = samples[max(0,round(a*SR)):min(len(samples),round(b*SR))]
            assert len(clip)>SR*.035, f"Too little source audio: {word}"
            seconds = beats*beat-.028
            sung = sing_word(clip,seconds,notes)
            h = sing_word(clip,seconds,notes,harmony=True)
            first = round(cursor*SR)
            lead[first:first+len(sung)] += sung
            harmony[first:first+len(h)] += h
            token_report.append({"word":word,"start":cursor,"end":cursor+seconds,"notes":notes,
                                 "source_duration":len(clip)/SR,"stretch_ratio":seconds/(len(clip)/SR)})
            cursor += beats*beat
        assert abs(sum(t[1] for t in phrase["tokens"])-7.5)<1e-8
        def level(x):
            rms = speech.voiced_rms(resample_poly(x,160,147))
            return np.tanh(x*(.16/max(rms,1e-7))*1.1)/1.1
        lead,harmony = level(lead).astype(np.float32),level(harmony).astype(np.float32)
        np.savez_compressed(cache,lead=lead,harmony=harmony)
        report = {"phrase":name,"file":cache.name,"text":line["text"],"tokens":token_report,"source_voice_cache":directory.name}
        cache.with_suffix(".json").write_text(json.dumps(report,indent=2),encoding="utf-8")
        manifest.append(report)
        print(f"  sung melody    {name} ({len(bounds)} words)",flush=True)
    (out/"singing-manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    return manifest
