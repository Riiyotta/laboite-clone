#!/usr/bin/env python3
"""Pixel-compare a live capture against a clone capture (R12).

    python3 extraction/parity/compare.py --live <run>/live --clone <run>/clone --label run1 \
        --out extraction/parity/results-run1.json

Metric (pinned here, documented in README): both screenshots (1440x900) are box-downsampled 4x to
360x225 RGB; a pixel matches when its largest channel difference is <= TOLERANCE (24/255). A shot's
score is the matched fraction; a section's score is the mean of its shots (1 shot for sections up to
1.5 viewports tall, 3 shots at 25/50/75 % of the scroll range for taller, scroll-scrubbed sections).
Gate: every section >= GATE (0.80) and the average >= GATE.

The output JSON is text-free (numbers, file names, sha256 of the images); the screenshots themselves
stay outside the repository. Requires Pillow + numpy (only for this optional harness).
"""
import argparse, hashlib, json, os, sys

TOLERANCE = 24
GATE = 0.80
SCALE = 4

ap = argparse.ArgumentParser()
ap.add_argument("--live", required=True)
ap.add_argument("--clone", required=True)
ap.add_argument("--label", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("compare.py needs Pillow and numpy (pip install pillow numpy)")


def load(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.resize((w // SCALE, h // SCALE), Image.BOX)
    return np.asarray(im, dtype=np.int16)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


gl = json.load(open(os.path.join(a.live, "geometry.json")))
gc = json.load(open(os.path.join(a.clone, "geometry.json")))
shots = {}
for s in gc["shots"]:
    if "file" not in s:
        continue
    lf, cf = os.path.join(a.live, s["file"]), os.path.join(a.clone, s["file"])
    if not os.path.exists(lf):
        shots[s["file"]] = {"section": s["section"], "error": "no live shot"}
        continue
    L, C = load(lf), load(cf)
    diff = np.abs(L - C).max(axis=2)
    score = float((diff <= TOLERANCE).mean())
    shots[s["file"]] = {"section": s["section"], "sample": s["sample"], "scrollY": s["scrollY"], "score": round(score, 4),
                        "meanAbsDiff": round(float(np.abs(L - C).mean()), 2), "liveSha256": sha(lf), "cloneSha256": sha(cf)}

sections = {}
for f, r in shots.items():
    sections.setdefault(r["section"], []).append(r.get("score"))
sec = {k: {"shots": len(v), "score": round(sum(x for x in v if x is not None) / len(v), 4) if all(x is not None for x in v) else None} for k, v in sections.items()}
vals = [v["score"] for v in sec.values() if v["score"] is not None]
avg = round(sum(vals) / len(vals), 4) if vals else None
below = sorted(k for k, v in sec.items() if v["score"] is None or v["score"] < GATE)
layout = {k: {"cloneTopPx": gc["sections"][k].get("topPx"), "liveTopPx": gl["sections"].get(k, {}).get("topPx")} for k in sec}
res = {
    "label": a.label, "metric": {"downsample": SCALE, "tolerance": TOLERANCE, "gate": GATE, "unit": "fraction of pixels whose max channel diff <= tolerance"},
    "capture": {k: {"capturedAt": g["capturedAt"], "gl": g.get("gl"), "settleMs": g["settleMs"], "documentHeightPx": g["documentHeightPx"], "consentOverlaysHidden": g["consentOverlaysHidden"]} for k, g in (("live", gl), ("clone", gc))},
    "layout": layout, "sections": sec, "average": avg, "sectionsBelowGate": below,
    "gatePassed": bool(vals) and not below and avg >= GATE, "shots": shots,
}
json.dump(res, open(a.out, "w"), indent=1)
print(f"{a.label}: average {avg}  sections below {GATE}: {len(below)}")
for k, v in sec.items():
    print(f"  {k:26} {v['score']}")
