"""Verify actual narration timing, caption fidelity and scene rendering."""
from __future__ import annotations

import json

import numpy as np
import skia

import render
from scenes import Film


def check_relevance_revision(script):
    """Protect the revised task-based example against the superseded adaptation."""
    text = " ".join(line["text"] for line in script["lines"] if line["scene"] in {"need", "contrast", "lenses"})
    for detail in ["empirical studies", "large language models", "university library",
                   "research consultation", "twenty twenty four", "task briefs",
                   "Feedback", "estimate suitability", "positive reactions",
                   "short demonstration", "introductory workshop", "same paper",
                   "limited evidence", "answer accuracy", "staff workload",
                   "real research consultations", "still contributes",
                   "match has not changed", "operational evidence",
                   "under what conditions", "work together"]:
        assert detail in text, f"Revised relevance explanation missing: {detail}"
    for old_claim in ["AI academic libraries", "opinion piece from twenty nineteen",
                      "misses every exact query word", "not your full need"]:
        assert old_claim not in text, f"Superseded relevance example remains: {old_claim}"


def main():
    script = render.config()
    check_relevance_revision(script)
    timeline = render.load_timeline(render.OUTPUT, script)
    captions = json.loads((render.OUTPUT / "captions.json").read_text(encoding="utf-8"))
    assert len({line["id"] for line in script["lines"]}) == len(script["lines"])
    assert [take["text"] for take in timeline["takes"]] == [line["text"] for line in script["lines"]]
    for cue in captions:
        assert 0 <= cue["start"] < cue["end"] <= timeline["duration"]
    assert all(a["end"] <= b["start"] for a, b in zip(captions, captions[1:]))
    assert render.media.voice.normalized(" ".join(c["text"] for c in captions)) == render.media.voice.normalized(" ".join(l["text"] for l in script["lines"]))
    for take in timeline["takes"]:
        words = take["words"]
        assert render.media.voice.normalized("".join(w["text"] for w in words)) == render.media.voice.normalized(take["text"])
        assert all(take["start"] <= w["start"] < w["end"] <= take["end"]+.001 for w in words)
    film = Film(timeline, script)
    surface = skia.Surface(1920, 1080)
    frames = 0
    for scene in script["scenes"]:
        a, b = timeline["scenes"][scene["id"]]
        times = [a+.01, b-.01] + list(np.arange(a+.4,b,.7))
        times += [w["start"]+.05 for take in timeline["takes"] if take["scene"]==scene["id"] for w in take["words"] if w["start"]+.05<b]
        for at in times:
            film.frame(surface.getCanvas(),float(at))
            frames += 1
        film.frame(surface.getCanvas(),a+(b-a)*.25)
        before = surface.makeImageSnapshot().toarray()[200:940,60:1860].copy()
        film.frame(surface.getCanvas(),a+(b-a)*.75)
        after = surface.makeImageSnapshot().toarray()[200:940,60:1860]
        assert np.count_nonzero(np.any(before != after,axis=2)) > 500, f"No visible motion: {scene['id']}"
    film.poster(surface.getCanvas())
    result = {"passed":True,"scenes":len(script["scenes"]),"sampled_frames":frames,
              "voice_takes":len(timeline["takes"]),"caption_cues":len(captions),
              "caption_text_matches_script":True,"all_word_reveals_valid":True,
              "revised_relevance_example_verified":True,
              "production_sha256":timeline["production_sha256"]}
    (render.OUTPUT / "scene-verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(f"PASS: {frames} rendered timeline samples, {len(script['scenes'])} moving scenes, "
          f"{len(timeline['takes'])} complete takes, {len(captions)} caption cues; revised relevance example.")


if __name__ == "__main__":
    main()
