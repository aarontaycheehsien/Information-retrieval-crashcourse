"""Original synth-pop instruments, rhythmic arrangement and MIDI score."""
from __future__ import annotations

import math
import struct

import numpy as np
from scipy.signal import butter,sosfilt

SR = 44100
CHORDS = {"C":[60,64,67,71],"G":[55,59,62,67],"Am":[57,60,64,67],"F":[53,57,60,64]}


def hz(midi):
    return 440*2**((midi-69)/12)


def filter_audio(x,kind,freq):
    return sosfilt(butter(2,freq,btype=kind,fs=SR,output="sos"),x).astype(np.float32)


def synth(notes,duration,kind="keys"):
    notes = notes if isinstance(notes,list) else [notes]
    t = np.arange(round(duration*SR))/SR
    x = np.zeros_like(t)
    for note in notes:
        f = hz(note)
        if kind=="bass":
            for harmonic in range(1,7):
                x += np.sin(2*np.pi*f*harmonic*t)/harmonic**1.7
        elif kind=="pad":
            for detune in [-.002,.002]:
                for harmonic in range(1,9):
                    x += np.sin(2*np.pi*f*(1+detune)*harmonic*t)/harmonic**1.75
        elif kind=="pluck":
            x += np.sin(2*np.pi*f*t)*np.exp(-t*4)+.25*np.sin(2*np.pi*f*2*t)*np.exp(-t*8)
        else:
            x += np.sin(2*np.pi*f*t)*np.exp(-t*1.6)+.24*np.sin(2*np.pi*f*2*t)*np.exp(-t*3)
            x += .1*np.sin(2*np.pi*f*3*t)*np.exp(-t*5)
    if kind=="pad":
        env = np.minimum(t/.35,1)*np.minimum((duration-t)/.4,1)
    else:
        env = np.minimum(t/.006,1)*np.minimum((duration-t)/.04,1)
        if kind=="bass":
            env *= .8+.2*np.exp(-t*9)
    return (x*env/max(1,len(notes))).astype(np.float32)


def drums(rng):
    def time(d):
        return np.arange(round(d*SR))/SR
    t = time(.55)
    freq = 48+100*np.exp(-t*35)
    kick = np.sin(2*np.pi*np.cumsum(freq)/SR)*np.exp(-t*8)
    kick += rng.normal(0,1,len(t))*np.exp(-t*350)*.12
    t = time(.28)
    clap = filter_audio(rng.normal(0,1,len(t)),"bandpass",[900,8000])*np.exp(-t*20)
    for at in [.012,.023]:
        clap += filter_audio(rng.normal(0,1,len(t)),"highpass",1700)*np.exp(-np.maximum(t-at,0)*26)*(t>=at)*.5
    clap += .18*np.sin(2*np.pi*182*t)*np.exp(-t*27)
    t = time(.07)
    hat = filter_audio(rng.normal(0,1,len(t)),"highpass",6500)*np.exp(-t*75)
    t = time(.28)
    open_hat = filter_audio(rng.normal(0,1,len(t)),"highpass",5800)*np.exp(-t*15)
    t = time(1.6)
    crash = filter_audio(rng.normal(0,1,len(t)),"highpass",3500)*np.exp(-t*2.6)
    return [x.astype(np.float32) for x in [kick,clap,hat,open_hat,crash]]


def add(bus,at,sound,gain=1,pan=0):
    first = round(at*SR)
    if first>=len(bus):
        return
    n = min(len(sound),len(bus)-first)
    bus[first:first+n,0] += sound[:n]*gain*math.sqrt((1-pan)/2)
    bus[first:first+n,1] += sound[:n]*gain*math.sqrt((1+pan)/2)


def arrange(config,timeline):
    count = round(timeline["duration"]*SR)
    rhythm = np.zeros((count,2),np.float32)
    bass = np.zeros_like(rhythm)
    music = np.zeros_like(rhythm)
    beat = 60/config["bpm"]
    rng = np.random.default_rng(config["seed"])
    kick,clap,hat,oh,crash = drums(rng)
    events = []
    cache = {}
    def tone(notes,length,kind):
        key = (tuple(notes) if isinstance(notes,list) else notes,length,kind)
        if key not in cache:
            cache[key] = synth(notes,length,kind)
        return cache[key]
    for section in timeline["sections"]:
        energy = section["energy"]
        chorus = section["id"].startswith("chorus") or section["id"]=="final"
        bridge = section["id"]=="bridge"
        intro = section["id"]=="intro"
        outro = section["id"]=="outro"
        for bar in range(section["bars"]):
            at = section["start"]+bar*4*beat
            chord = CHORDS[section["chords"][bar%len(section["chords"])]]
            roots = [n-24 for n in chord[:1]]
            # Warm pads and wide offbeat piano leave the center open for the lead.
            add(music,at,tone([n+12 for n in chord],4*beat+.18,"pad"),.095*energy,-.32)
            for step in [0,.75,1.5,2.5,3.25]:
                add(music,at+step*beat,tone(chord,.63,"keys"),.115*energy,.35)
            for step in ([0,1.5,2,3.5] if chorus else [0,1.5,2.75]):
                length = .42*beat if chorus else .7*beat
                add(bass,at+step*beat,tone(roots[0],length,"bass"),.27*energy)
                events.append((1,at+step*beat,length,roots[0],82))
            for step in range(8):
                note = chord[[0,2,1,3,2,1,3,2][step]]+12
                level = .035 if chorus else .048
                if bridge:
                    level = .014
                add(music,at+step*beat/2,tone(note,.46,"pluck"),level*energy,math.sin(step)*.75)
                events.append((2,at+step*beat/2,min(.28,beat*.47),note,55))
            if not bridge and not outro and (not intro or bar>=2):
                for step in range(4):
                    add(rhythm,at+step*beat,kick,.42*(.7+.3*energy))
                for step in [1,3]:
                    add(rhythm,at+step*beat,clap,.205*energy)
                for step in range(8):
                    add(rhythm,at+step*beat/2,hat,.083*energy*(1 if step%2 else .6),.3)
                if chorus:
                    for step in [.5,2.5]:
                        add(rhythm,at+step*beat,oh,.07,.45)
            elif bridge and bar>=4:
                add(rhythm,at,kick,.22)
                add(rhythm,at+2*beat,clap,.08)
            for note in chord:
                events.append((3,at,3.8*beat,note,65))
        if chorus:
            add(rhythm,section["start"],crash,.085,-.55)
        if section["id"].startswith("pre"):
            finish = section["end"]
            for i in range(8):
                add(rhythm,finish-2*beat+i*beat/4,clap,.08+.01*i)
            t = np.arange(round(1.8*SR))/SR
            riser = filter_audio(rng.normal(0,1,len(t)),"bandpass",[2000,7500])*np.linspace(0,.055,len(t))
            add(music,finish-1.8,riser)
    # A final tonic resolves the song; its ring falls within the two-second tail.
    at = timeline["sections"][-1]["end"]-.15
    add(music,at,synth([60,64,67,72],2.1,"keys"),.15)
    tm = np.arange(count)/SR
    pulse = tm/beat-np.floor(tm/beat)
    sidechain = .64+.36*np.minimum(pulse/.38,1)
    music *= sidechain[:,None]
    bass *= (.82+.18*np.minimum(pulse/.22,1))[:,None]
    return rhythm,bass,music,events


def varlen(value):
    result = [value&127]
    while value>>7:
        value >>= 7
        result.insert(0,(value&127)|128)
    return bytes(result)


def midi(path,config,timeline,events):
    """A standard type-1 MIDI score with melody, bass, arpeggio and chord tracks."""
    tracks = []
    tempo = round(60_000_000/config["bpm"])
    tracks.append(b"\x00\xff\x51\x03"+tempo.to_bytes(3,"big")+b"\x00\xff\x58\x04\x04\x02\x18\x08\x00\xff\x2f\x00")
    beat = 60/config["bpm"]
    for section in timeline["sections"]:
        for occurrence in section["vocals"]:
            cursor = occurrence["start"]+.25*beat
            for word,duration,notes in config["phrases"][occurrence["phrase"]]["tokens"]:
                notes = notes if isinstance(notes,list) else [notes]
                for i,note in enumerate(notes):
                    events.append((0,cursor+duration*beat*i/len(notes),duration*beat/len(notes)-.015,note,95))
                cursor += duration*beat
    for channel,name,program in [(0,"Sung lead melody",53),(1,"Synth bass",38),(2,"Hook arpeggio",81),(3,"Chords",4)]:
        timed = [(0,bytes([0xC0|channel,program]))]
        for ch,at,length,note,velocity in events:
            if ch==channel:
                first = round(at/beat*480)
                last = round((at+length)/beat*480)
                timed.extend([(first,bytes([0x90|channel,note,velocity])),(last,bytes([0x80|channel,note,0]))])
        data = b"\x00\xff\x03"+varlen(len(name))+name.encode()
        previous = 0
        for at,event in sorted(timed,key=lambda e:(e[0],e[1][0]&0xF0!=0x80)):
            data += varlen(at-previous)+event
            previous = at
        data += b"\x00\xff\x2f\x00"
        tracks.append(data)
    payload = b"MThd"+struct.pack(">IHHH",6,1,len(tracks),480)
    for track in tracks:
        payload += b"MTrk"+struct.pack(">I",len(track))+track
    path.write_bytes(payload)


def verify_midi(path):
    """Independently parse the score and reject hanging or overlapping notes."""
    data = path.read_bytes()
    assert data[:4]==b"MThd"
    size,kind,count,division = struct.unpack(">IHHH",data[4:14])
    assert (size,kind,count,division)==(6,1,5,480)
    position = 14
    records = []
    for track_index in range(count):
        assert data[position:position+4]==b"MTrk"
        length = int.from_bytes(data[position+4:position+8],"big")
        body = data[position+8:position+8+length]
        assert len(body)==length
        position += 8+length
        offset,tick,notes = 0,0,0
        active = set()
        ended = False
        def vlq():
            nonlocal offset
            value = 0
            for _ in range(4):
                byte = body[offset]
                offset += 1
                value = (value<<7)|(byte&127)
                if not byte&128:
                    return value
            raise AssertionError("Invalid MIDI variable-length integer")
        while offset<len(body):
            tick += vlq()
            status = body[offset]
            offset += 1
            assert status&128
            if status==255:
                meta = body[offset]
                offset += 1
                n = vlq()
                offset += n
                if meta==47:
                    ended = True
            else:
                n = 1 if status&240 in [192,208] else 2
                args = body[offset:offset+n]
                offset += n
                assert len(args)==n and all(v<128 for v in args)
                key = (status&15,args[0])
                if status&240==144 and args[1]:
                    assert key not in active, f"Overlapping MIDI note: {key} at {tick}"
                    active.add(key)
                    notes += 1
                elif status&240 in [128,144]:
                    assert key in active, f"Unmatched MIDI note off: {key}"
                    active.remove(key)
        assert ended and not active and offset==len(body)
        records.append({"track":track_index,"note_pairs":notes,"final_tick":tick})
    assert position==len(data) and all(r["note_pairs"]>0 for r in records[1:])
    return {"passed":True,"type":kind,"tracks":count,"ticks_per_quarter":division,"records":records}
