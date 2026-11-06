#!/usr/bin/env python3
"""Whole-page-wrapper quality gate (R9). Called by verify_all.py; also runnable alone:

    python3 extraction/wrapper_gate.py          # exit 1 on any error

Inputs: extraction/measured-values.json (sectionHeights + wrapperGate.whitelist, measured with a headless
browser at 1440x900 by extraction/measure_sections.mjs), sections/*.json (category, positionKind),
templates/templates.json (which sections each route renders).
Thresholds are pinned HERE (not only in JSON):
  HERO > 1800px warn; HERO > 3000px error unless whitelisted;
  one in-flow section > 50% of its page warn, > 60% error unless whitelisted
  (pages with < 3 in-flow sections are skipped; CHROME/BACKDROP and fixed elements take no share);
  non-HERO in-flow section > 3000px: informational warning (tall scroll stage);
  missing measurement or wrong viewport: error.
Whitelist entries need reviewedBy, justification >= 30 chars, maxHeightPx above the measured height,
status; an agent reviewer must say "agent attestation, not a human sign-off". Stale or over-cap entries
fail. A whitelisted hit still warns.
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWPORT = "1440x900"
HERO_WARN_PX = 1800
HERO_FAIL_PX = 3000
SHARE_WARN = 0.50
SHARE_FAIL = 0.60
TALL_STAGE_INFO_PX = 3000
MIN_INFLOW_FOR_SHARE = 3
SHELL_CATEGORIES = {"CHROME", "BACKDROP"}
AGENT_RE = re.compile(r"claude|agent|assistant|automated|\bai\b", re.I)
AGENT_DISCLAIMER = "agent attestation, not a human sign-off"


def evaluate(measured, contracts, templates):
    errors, warnings = [], []
    sh = measured.get("sectionHeights") or {}
    if sh.get("viewport") != VIEWPORT:
        errors.append(f"sectionHeights measured at {sh.get('viewport')!r}, gate requires {VIEWPORT}")
    wl = (measured.get("wrapperGate") or {}).get("whitelist", [])
    used = set()

    def whitelisted(route, sec, h, kind):
        for i, e in enumerate(wl):
            if e.get("route") == route and e.get("section") == sec and e.get("rule") == kind:
                ok = True
                if not e.get("reviewedBy"):
                    errors.append(f"whitelist {sec}: missing reviewedBy"); ok = False
                elif AGENT_RE.search(e["reviewedBy"]) and AGENT_DISCLAIMER not in e["reviewedBy"]:
                    errors.append(f"whitelist {sec}: agent reviewer must say '{AGENT_DISCLAIMER}'"); ok = False
                if len(e.get("justification") or "") < 30:
                    errors.append(f"whitelist {sec}: justification shorter than 30 chars"); ok = False
                if not isinstance(e.get("maxHeightPx"), (int, float)) or e["maxHeightPx"] <= h:
                    errors.append(f"whitelist {sec}: maxHeightPx {e.get('maxHeightPx')} is not above the measured {h}px"); ok = False
                if not e.get("status"):
                    errors.append(f"whitelist {sec}: missing status"); ok = False
                used.add(i)
                return ok
        return False

    for tid, t in templates.items():
        for route in t["routes"]:
            page = (sh.get("routes") or {}).get(route)
            if not page:
                errors.append(f"{route}: no measured heights"); continue
            doc = page.get("documentHeightPx") or 0
            inflow = []
            for n in t["nodes"]:
                c = contracts.get(n["section"])
                m = (page.get("sections") or {}).get(n["section"])
                if not c:
                    continue
                if not m or not isinstance(m.get("heightPx"), (int, float)):
                    errors.append(f"{route} {n['section']}: missing measurement"); continue
                if c["positionKind"] != "in-flow" or m.get("positionKind") == "fixed":
                    continue
                h = m["heightPx"]
                cat = c["semantic"]["category"]
                if cat not in SHELL_CATEGORIES:
                    inflow.append((n["section"], h))
                if cat == "HERO":
                    if h > HERO_FAIL_PX:
                        if whitelisted(route, n["section"], h, "HERO_MAX_HEIGHT"):
                            warnings.append(f"{route} {n['section']}: HERO {h}px > {HERO_FAIL_PX}px (whitelisted, status: {next(e['status'] for e in wl if e.get('section') == n['section'] and e.get('rule') == 'HERO_MAX_HEIGHT')})")
                        else:
                            errors.append(f"{route} {n['section']}: HERO {h}px > {HERO_FAIL_PX}px and not whitelisted")
                    elif h > HERO_WARN_PX:
                        warnings.append(f"{route} {n['section']}: HERO {h}px > {HERO_WARN_PX}px")
                elif h > TALL_STAGE_INFO_PX:
                    warnings.append(f"{route} {n['section']}: tall {cat} section {h}px (informational)")
            if len(inflow) >= MIN_INFLOW_FOR_SHARE and doc:
                for sec, h in inflow:
                    share = h / doc
                    if share > SHARE_FAIL:
                        if whitelisted(route, sec, h, "PAGE_SHARE"):
                            warnings.append(f"{route} {sec}: {share:.0%} of the page (whitelisted)")
                        else:
                            errors.append(f"{route} {sec}: holds {share:.0%} of the page (> {SHARE_FAIL:.0%})")
                    elif share > SHARE_WARN:
                        warnings.append(f"{route} {sec}: holds {share:.0%} of the page (> {SHARE_WARN:.0%})")
    for i, e in enumerate(wl):
        if i not in used:
            errors.append(f"whitelist entry {e.get('section')} ({e.get('rule')}) is stale: no gate hit uses it")
    return errors, warnings


def run(repo=REPO):
    load = lambda rel: json.load(open(os.path.join(repo, rel), encoding="utf-8"))
    contracts = {}
    for f in os.listdir(os.path.join(repo, "sections")):
        if f.endswith(".json"):
            c = load(f"sections/{f}")
            contracts[c["id"]] = c
    return evaluate(load("extraction/measured-values.json"), contracts, load("templates/templates.json")["templates"])


if __name__ == "__main__":
    errs, warns = run()
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print(f"wrapper gate: {len(errs)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errs else 0)
