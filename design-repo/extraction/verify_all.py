#!/usr/bin/env python3
"""One-shot verification of this design-repo. Exit 1 on any FAIL.

    python3 extraction/verify_all.py [--quiet]

Checks (each prints PASS / FAIL / WARN):
  json         every *.json parses
  schema       Draft-07: both schemas are valid, both example PageSpecs validate with 0 errors, every
               section contract validates against schema/section-contract.schema.json
  schema-sync  pagespec.schema.json content/motion definitions == the section contracts
  semantic     schema/semantic_validate.py: reference + generated examples 0 errors
  graph-sync   compatibility/graph.json rule ids == semantic_validate.IMPLEMENTED_GRAPH_RULES
  allowlist    parity with sections/ primitives/ components/ (no phantom, no orphan); settable content
               fields and token slots re-derived from the contracts / token policy
  versions     manifest allowlistVersion / tokenCatalogVersion == the files' own versions
  counts       manifest counts recomputed from disk
  catalog      tokens/llm/token-catalog.json re-derived from the token files (drift = FAIL)
  policy       token-policy ids/categories resolve in the catalog; theme combinations use allowed slots
  pins         PINNED_AVAILABILITY / RETRIEVAL_INELIGIBLE here == the copies in semantic_validate.py ==
               assets/asset-roles.json / sections / allowlist; runtime-looking ids are pinned;
               substitutes and generatedAssetRoles are generation-safe
  templates    every route mapped exactly once; template nodes resolve to contracts
  policy-hash  extraction/policy_hash.py == manifest + policy/design-policy.json contentHash
  gate         extraction/wrapper_gate.py (R9)
  parity       parity exceptions are evidence (status pending human approval, approvedBy null)
  paths        no absolute machine paths; entryPoints exist and stay inside the repo
  citations    every {cite, needle} and section source range resolves in the sibling source tree, the
               needle / tag is in range (WARN-only when the design-repo is used without its source)
  copy         every text string of the reference example exists in the source (WARN-only without source)
Standard library + jsonschema. Repo root derives from __file__.
"""
import glob, hashlib, html, importlib.util, json, os, re, sys, unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(REPO)
QUIET = "--quiet" in sys.argv

# ---- pins duplicated on purpose (must equal semantic_validate.py and the registries) ----
PINNED_AVAILABILITY = {
    "brand.wordmark": "blocked-for-generation", "hero.loop-video": "reference-only", "case.photo": "reference-only", "expertise.photo": "reference-only",
    "team.photo": "blocked-for-generation", "resource.cover": "reference-only", "credential.badge": "blocked-for-generation", "client.logo": "blocked-for-generation",
    "icon.ui": "reference-only", "scene.headset-model": "reference-only", "scene.sphere-thumbnail": "reference-only", "scene.hdr-environment": "reference-only",
    "scene.title-font-outline": "blocked-for-generation",
    "brand.placeholder-mark": "generation-safe", "brand.user-supplied-mark": "generation-safe", "media.generated-image": "generation-safe", "media.generated-video": "generation-safe",
    "media.placeholder": "generation-safe", "person.fictional-avatar": "generation-safe", "logo.placeholder-client": "generation-safe", "credential.placeholder-badge": "generation-safe",
    "rating.placeholder-badge": "generation-safe", "icon.generic": "generation-safe", "social.network-icon": "generation-safe", "font.open-licence-outline": "generation-safe",
    "url.placeholder": "generation-safe", "copy.original": "generation-safe",
}
RETRIEVAL_INELIGIBLE = {"backdrop.webgl-scene", "chrome.loader", "chrome.menu-overlay", "chrome.seo-modal"}
RUNTIME_UI_PATTERN = re.compile(r"loader|preloader|modal|dialog|overlay|drawer|cookie|consent|toast|cursor|backdrop|webgl|spinner", re.I)
ABS_PATH = re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|/private/(tmp|var)/|[A-Za-z]:\\\\?Users\\\\")

results = []


def rec(name, ok, msg, warn=False):
    results.append((name, "PASS" if ok else ("WARN" if warn else "FAIL"), msg))


def load(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return json.load(f)


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- json
bad = []
for p in glob.glob(os.path.join(REPO, "**", "*.json"), recursive=True):
    try:
        json.load(open(p, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        bad.append(f"{os.path.relpath(p, REPO)}: {e}")
rec("json", not bad, "all JSON parses" if not bad else bad[:3])
if bad:
    for r in results:
        print(*r)
    sys.exit(1)

manifest = load("registry.manifest.json")
contracts = {load(f"sections/{f}")["id"]: load(f"sections/{f}") for f in sorted(os.listdir(os.path.join(REPO, "sections"))) if f.endswith(".json")}
section_files = {load(f"sections/{f}")["id"]: f for f in os.listdir(os.path.join(REPO, "sections")) if f.endswith(".json")}
prims = {load(f"primitives/{f}")["id"] for f in os.listdir(os.path.join(REPO, "primitives")) if f.endswith(".json")}
comps = {load(f"components/{f}")["id"] for f in os.listdir(os.path.join(REPO, "components")) if f.endswith(".json")}
allow = load("tokens/llm/component-allowlist.json")
catalog = load("tokens/llm/token-catalog.json")
policy = load("tokens/llm/token-policy.json")
roles = load("assets/asset-roles.json")["roles"]
templates = load("templates/templates.json")
graph = load("compatibility/graph.json")
pschema = load("schema/pagespec.schema.json")
cschema = load("schema/section-contract.schema.json")
measured = load("extraction/measured-values.json")
ref = load("schema/example.pagespec.json")
gen = load("schema/examples/generated.home.pagespec.json")

# ---------------------------------------------------------------- schema (Draft-07)
try:
    from jsonschema import Draft7Validator
except ImportError:
    rec("schema", False, "jsonschema is required (pip install jsonschema)")
    Draft7Validator = None
if Draft7Validator:
    errs = []
    for name, s in (("pagespec", pschema), ("section-contract", cschema)):
        try:
            Draft7Validator.check_schema(s)
        except Exception as e:  # noqa: BLE001
            errs.append(f"{name} schema invalid: {str(e)[:120]}")
    for name, inst in (("example.pagespec.json", ref), ("generated.home.pagespec.json", gen)):
        errs += [f"{name}: {'/'.join(map(str, e.absolute_path))}: {e.message[:120]}" for e in Draft7Validator(pschema).iter_errors(inst)]
    for sid, c in contracts.items():
        errs += [f"sections/{section_files[sid]}: {e.message[:120]}" for e in Draft7Validator(cschema).iter_errors(c)]
    rec("schema", not errs, "Draft-07: schemas valid; reference + generated examples 0 errors; 19 contracts valid" if not errs else errs[:4])

# ---------------------------------------------------------------- schema-sync
d = pschema["definitions"]
drift = [s for s, c in contracts.items() if d.get(f"content.{s}") != c["content"]]
drift += [f"motion.{s}" for s, c in contracts.items() if sorted(d.get(f"motion.{s}", {}).get("properties", {}).get("patterns", {}).get("items", {}).get("enum", [])) != sorted(c["motion"]["allowedPatterns"] or ["__none__"])
          or d.get(f"motion.{s}", {}).get("properties", {}).get("reducedMotionFallback", {}).get("const") != c["motion"]["reducedMotionFallback"]]
drift += [f"section enum" for _ in [0] if sorted(pschema["definitions"]["node"]["properties"]["section"]["enum"]) != sorted(contracts)]
rec("schema-sync", not drift, "pagespec content/motion definitions identical to the 19 contracts" if not drift else f"drift: {drift[:4]}")

# ---------------------------------------------------------------- semantic + graph-sync
sv = mod("schema/semantic_validate.py", "semantic_validate")
ctx = sv.Ctx(REPO)
r_ref = sv.validate(ref, ctx)
r_gen = sv.validate(gen, ctx)
e_ref = [r for r in r_ref if r[0] == "error"]
e_gen = [r for r in r_gen if r[0] == "error"]
rec("semantic", not e_ref and not e_gen, f"reference: 0 errors / {len(r_ref)} warnings; generated: 0 errors / {len(r_gen)} warnings" if not e_ref and not e_gen else (e_ref + e_gen)[:4])
gids = {r["id"] for r in graph["rules"]}
rec("graph-sync", gids == sv.IMPLEMENTED_GRAPH_RULES, f"{len(gids)} graph rules == validator rules" if gids == sv.IMPLEMENTED_GRAPH_RULES else f"mismatch {sorted(gids ^ sv.IMPLEMENTED_GRAPH_RULES)}")

# ---------------------------------------------------------------- allowlist parity
probs = []
a_secs = set(allow["sections"])
probs += [f"phantom section {x}" for x in a_secs - set(contracts)] + [f"orphan contract {x}" for x in set(contracts) - a_secs]
probs += [f"phantom primitive {x}" for x in set(allow["primitives"]) - prims] + [f"orphan primitive {x}" for x in prims - set(allow["primitives"])]
probs += [f"phantom component {x}" for x in set(allow["components"]) - comps] + [f"orphan component {x}" for x in comps - set(allow["components"])]
for s in a_secs & set(contracts):
    e = allow["sections"][s]
    if sorted(e["settable"]["content"]) != sorted(contracts[s]["content"]["properties"]):
        probs.append(f"{s}: settable content != contract fields")
    if sorted(e["settable"]["tokens"]) != sorted(policy["nodeSlots"]) or sorted(pschema["definitions"]["tokens"]["properties"]) != sorted(policy["nodeSlots"]):
        probs.append(f"{s}: token slots != token-policy nodeSlots")
    if e["retrievalEligible"] != contracts[s]["retrievalEligible"]:
        probs.append(f"{s}: allowlist retrievalEligible != contract")
rec("allowlist", not probs, f"{len(a_secs)} sections, {len(prims)} primitives, {len(comps)} components in parity" if not probs else probs[:4])

# ---------------------------------------------------------------- versions + counts
vprob = []
if manifest.get("allowlistVersion") != allow.get("version"):
    vprob.append(f"allowlistVersion {manifest.get('allowlistVersion')} != allowlist {allow.get('version')}")
if manifest.get("tokenCatalogVersion") != catalog.get("version"):
    vprob.append(f"tokenCatalogVersion {manifest.get('tokenCatalogVersion')} != catalog {catalog.get('version')}")
if manifest.get("pageSpecVersion") != pschema["properties"]["pageSpecVersion"]["const"]:
    vprob.append("pageSpecVersion != schema const")
rec("versions", not vprob, "allowlistVersion, tokenCatalogVersion, pageSpecVersion agree" if not vprob else vprob)
real_counts = {"tokens": len(catalog["tokens"]), "sections": len(contracts), "primitives": len(prims), "components": len(comps), "templates": len(templates["templates"]),
               "routes": len(templates["routes"]), "assetRoles": len(roles), "generationSafeAssetRoles": sum(1 for r in roles.values() if r["availability"] == "generation-safe"),
               "retrievalIneligibleSections": sum(1 for c in contracts.values() if c["retrievalEligible"] is False), "motionPatterns": len(load("tokens/00-foundation/motion-patterns.json")["patterns"]),
               "graphRules": len(graph["rules"]), "examplePageSpecs": len([p for p in glob.glob(os.path.join(REPO, "schema", "**", "*.json"), recursive=True) if "example" in p])}
cdiff = {k: (manifest.get("counts", {}).get(k), v) for k, v in real_counts.items() if manifest.get("counts", {}).get(k) != v}
readme = open(os.path.join(REPO, "README.md"), encoding="utf-8").read()
blk = re.search(r"<!-- counts:start -->(.*?)<!-- counts:end -->", readme, re.S)
readme_counts = dict(re.findall(r"^\| (\w+) \| (\d+) \|$", blk.group(1), re.M)) if blk else {}
for k, v in real_counts.items():
    if readme_counts.get(k) != str(v):
        cdiff[f"README.{k}"] = (readme_counts.get(k), v)
rec("counts", not cdiff, f"manifest + README counts match disk {real_counts}" if not cdiff else f"manifest vs disk: {cdiff}")

# ---------------------------------------------------------------- catalog drift
derived = {}
for f in catalog["sourceFiles"]:
    for k, v in load(f)["tokens"].items():
        derived[k] = {"category": k.split(".")[0], "type": v["type"], "value": v["value"], "file": f}
cd = sorted(set(derived) ^ set(catalog["tokens"])) + sorted(k for k in derived if k in catalog["tokens"] and derived[k] != catalog["tokens"][k])
cnt_ok = catalog["counts"]["total"] == len(catalog["tokens"])
rec("catalog", not cd and cnt_ok, f"{len(derived)} tokens re-derived from {len(catalog['sourceFiles'])} token files, identical" if not cd and cnt_ok else f"catalog drift: {cd[:5]} count_ok={cnt_ok}")

# ---------------------------------------------------------------- policy resolves
pp = []
cats = set(catalog["counts"]["byCategory"])
for scope in ("pageLevel", "nodeSlots"):
    for slot, r in policy[scope].items():
        pp += [f"{slot}: category {c} not in catalog" for c in r["allowedCategories"] if c not in cats]
        pp += [f"{slot}: {t} not in catalog" for t in r["allowed"] if t not in catalog["tokens"]]
        pp += [f"{slot}: {t} not in allowed categories" for t in r["allowed"] if t in catalog["tokens"] and catalog["tokens"][t]["category"] not in r["allowedCategories"]]
for st, combo in policy["themeCombinations"].items():
    if st.startswith("$"):
        continue
    if st not in policy["nodeSlots"]["surfaceTone"]["allowed"]:
        pp.append(f"themeCombinations {st} not an allowed surfaceTone")
    for slot in ("textTone", "accentColor"):
        pp += [f"{st}.{slot}: {t} not allowed in slot" for t in combo.get(slot, []) if t not in policy["nodeSlots"][slot]["allowed"]]
pp += [f"rawValueRestrictions key {k} is not a catalog category" for k in policy["rawValueRestrictions"] if k not in cats]
pp += [f"licensedTokens {k} not in catalog" for k in policy["licensedTokens"] if k not in catalog["tokens"]]
rec("policy", not pp, "token-policy slots, categories, combinations and licensed tokens resolve in the catalog" if not pp else pp[:4])

# ---------------------------------------------------------------- pins
pinp = []
if PINNED_AVAILABILITY != sv.PINNED_AVAILABILITY:
    pinp.append("PINNED_AVAILABILITY differs between verify_all.py and semantic_validate.py")
if set(PINNED_AVAILABILITY) != set(roles):
    pinp.append(f"pin vs registry role sets differ: {sorted(set(PINNED_AVAILABILITY) ^ set(roles))}")
for k, v in roles.items():
    if PINNED_AVAILABILITY.get(k) != v.get("availability"):
        pinp.append(f"{k}: registry {v.get('availability')} != pinned {PINNED_AVAILABILITY.get(k)}")
    if v.get("availability") != "generation-safe":
        subs = v.get("generationSafeSubstitutes") or []
        if not subs:
            pinp.append(f"{k}: no generationSafeSubstitutes")
        pinp += [f"{k}: substitute {s} is not generation-safe" for s in subs if PINNED_AVAILABILITY.get(s) != "generation-safe"]
    if v.get("availability") != "generation-safe" and v.get("generationPolicy") == "may-generate-new":
        pinp.append(f"{k}: reference-only/blocked role cannot be may-generate-new")
if k := [r for r in ("brand.wordmark", "client.logo", "credential.badge", "team.photo") if roles.get(r, {}).get("generationPolicy") != "must-not-fabricate"]:
    pinp.append(f"identity roles must be must-not-fabricate: {k}")
if RETRIEVAL_INELIGIBLE != sv.RETRIEVAL_INELIGIBLE:
    pinp.append("RETRIEVAL_INELIGIBLE differs between verify_all.py and semantic_validate.py")
for sid, c in contracts.items():
    pinned = sid not in RETRIEVAL_INELIGIBLE
    if c["retrievalEligible"] != pinned:
        pinp.append(f"{sid}: contract retrievalEligible={c['retrievalEligible']} contradicts pin")
    if allow["sections"].get(sid, {}).get("retrievalEligible") not in (None, pinned):
        pinp.append(f"{sid}: allowlist retrievalEligible contradicts pin")
    if RUNTIME_UI_PATTERN.search(sid + " " + c["title"]) and pinned:
        pinp.append(f"{sid}: looks like runtime UI but is not pinned ineligible")
    if not c["retrievalEligible"] and len(c.get("retrievalIneligibleReason", "")) < 30:
        pinp.append(f"{sid}: ineligible without a 30+ char reason")
    pinp += [f"{sid}: generatedAssetRoles {r} not generation-safe" for r in c["generatedAssetRoles"] if PINNED_AVAILABILITY.get(r) != "generation-safe"]
    pinp += [f"{sid}: unknown asset role {r}" for r in c["assetRoles"] + c["generatedAssetRoles"] if r not in PINNED_AVAILABILITY]
    if c["source"]["id"] == c["semantic"]["id"] or c["semantic"]["id"] != c["id"]:
        pinp.append(f"{sid}: source.id must differ from semantic.id, semantic.id must equal the contract id")
rec("pins", not pinp, f"{len(PINNED_AVAILABILITY)} asset availabilities and {len(RETRIEVAL_INELIGIBLE)} retrieval pins agree across code, registry, contracts, allowlist" if not pinp else pinp[:4])

# ---------------------------------------------------------------- templates / routes
tp = []
seen_routes = {}
for tid, t in templates["templates"].items():
    for r in t["routes"]:
        seen_routes.setdefault(r, []).append(tid)
    tp += [f"{tid}: node {n['section']} has no contract" for n in t["nodes"] if n["section"] not in contracts]
    tp += [f"{tid}: node keys must be structured" for n in t["nodes"] if not {"section", "required", "repeatable"} <= set(n)]
tp += [f"route {r} mapped {len(v)} times" for r, v in seen_routes.items() if len(v) != 1]
listed = {r["route"]: r["template"] for r in templates["routes"]}
tp += [f"route table mismatch {sorted(set(listed) ^ set(seen_routes))}"] if set(listed) != set(seen_routes) else []
tp += [f"unused contract {s}" for s in contracts if not any(n["section"] == s for t in templates["templates"].values() for n in t["nodes"])]
rec("templates", not tp, f"{len(seen_routes)} route(s) mapped exactly once; {sum(len(t['nodes']) for t in templates['templates'].values())} template nodes resolve" if not tp else tp[:4])

# ---------------------------------------------------------------- policy hash
ph = mod("extraction/policy_hash.py", "policy_hash").compute(REPO)
dp = load("policy/design-policy.json")
ok = ph == manifest.get("designPolicy", {}).get("contentHash") == dp.get("contentHash")
AGENT_RE = re.compile(r"claude|agent|assistant|automated|\bai\b|gpt|llm", re.I)
try:
    HD = load("extraction/human-decisions.json")
except Exception:
    HD = {"decisions": []}
def human_record(item, who):
    """An approval counts only if a hand-authored owner decision covers this item and names the same human approver."""
    for d in HD.get("decisions", []):
        if item in d.get("items", []) and d.get("decidedBy") == who and who and not AGENT_RE.search(who) and d.get("verbatim") and d.get("decidedAt"):
            return d
    return None
def approval_state_ok(item, e, pending_key="status", pending_val="pending human approval"):
    if e.get(pending_key) == pending_val and e.get("approvedBy") is None:
        return True
    return e.get(pending_key) == "approved" and human_record(item, e.get("approvedBy")) is not None
_a = dp["approval"]
appr_ok = manifest.get("productionApproved") is False and (
    (_a["status"] == "defined-pending-architecture-review" and _a["architectureDecisionRecorded"] is False)
    or (_a["status"] == "approved-by-owner" and _a["architectureDecisionRecorded"] is True and human_record("policy/design-policy.json:approval", _a.get("decidedBy")) is not None))
rec("policy-hash", ok and appr_ok, f"{ph} matches manifest + design-policy; approval pending or owner-recorded, productionApproved false" if ok and appr_ok else f"recomputed {ph} vs manifest {manifest.get('designPolicy', {}).get('contentHash')} / policy {dp.get('contentHash')}; approval_ok={appr_ok}")

# ---------------------------------------------------------------- wrapper gate
wg = mod("extraction/wrapper_gate.py", "wrapper_gate")
g_err, g_warn = wg.run(REPO)
rec("gate", not g_err, f"wrapper gate 0 errors, {len(g_warn)} warnings ({'; '.join(g_warn[:1])} ...)" if not g_err else g_err[:4])

# ---------------------------------------------------------------- parity exceptions
pe = []
par = measured.get("parity", {})
for e in par.get("exceptions", []):
    if not approval_state_ok("parity.exceptions:" + str(e.get("section")), e) or len(e.get("cause", "")) < 30:
        pe.append(f"{e.get('section')}: exception must be pending human approval (approvedBy null) or approved by a recorded human owner decision, with a cause")
for e in measured.get("wrapperGate", {}).get("whitelist", []):
    if not approval_state_ok("wrapperGate.whitelist:" + str(e.get("section")), e):
        pe.append(f"whitelist {e.get('section')}: must be pending human approval (approvedBy null) or approved by a recorded human owner decision")
for r in par.get("runs", []):
    f = os.path.join(REPO, r["file"])
    if not os.path.exists(f):
        pe.append(f"missing {r['file']}")
        continue
    res = json.load(open(f, encoding="utf-8"))
    if res["average"] != r["average"] or sorted(res["sectionsBelowGate"]) != sorted(r["sectionsBelowGate"]):
        pe.append(f"{r['file']} disagrees with measured-values parity summary")
    below = set(res["sectionsBelowGate"]) - {e["section"] for e in par.get("exceptions", [])}
    if below:
        pe.append(f"{r['label']}: sections below gate without a recorded exception: {sorted(below)}")
rec("parity", not pe, f"{len(par.get('runs', []))} runs recorded; {len(par.get('exceptions', []))} exception(s), each pending or approved by a recorded human decision" if not pe else pe[:4])

# ---------------------------------------------------------------- paths / entryPoints
ap = []
for p in glob.glob(os.path.join(REPO, "**", "*"), recursive=True):
    if os.path.isfile(p) and os.path.splitext(p)[1] in (".json", ".md", ".py", ".mjs", ".txt") and "__pycache__" not in p:
        if ABS_PATH.search(open(p, encoding="utf-8", errors="ignore").read()):
            ap.append(os.path.relpath(p, REPO))
eps = manifest.get("entryPoints", {})
eps = list(eps.values()) if isinstance(eps, dict) else eps
ap += [f"entryPoint outside repo: {e}" for e in eps if e.startswith("..") or os.path.isabs(e)]
ap += [f"entryPoint missing: {e}" for e in eps if not e.startswith("..") and not os.path.exists(os.path.join(REPO, e))]
rec("paths", not ap, f"no absolute machine paths; {len(eps)} entryPoints exist inside the repo" if not ap else ap[:4])

# ---------------------------------------------------------------- citations
have_src = os.path.isdir(os.path.join(ROOT, "src")) and os.path.exists(os.path.join(ROOT, "CLONE_SPEC_A.md"))
_lines = {}


def flines(rel):
    if rel not in _lines:
        _lines[rel] = open(os.path.join(ROOT, rel), encoding="utf-8").read().split("\n")
    return _lines[rel]


def walk_cites(o, where, out):
    if isinstance(o, dict):
        if isinstance(o.get("cite"), str) and isinstance(o.get("needle"), str):
            out.append((where, o["cite"], o["needle"]))
        for k, v in o.items():
            walk_cites(v, where, out)
    elif isinstance(o, list):
        for v in o:
            walk_cites(v, where, out)


if have_src:
    allc = []
    for p in glob.glob(os.path.join(REPO, "**", "*.json"), recursive=True):
        walk_cites(json.load(open(p, encoding="utf-8")), os.path.relpath(p, REPO), allc)
    cp = []
    for where, c, needle in allc:
        m = re.match(r"^(.+):(\d+)(?:-(\d+))?$", c)
        if not m or not os.path.exists(os.path.join(ROOT, m.group(1))):
            cp.append(f"{where}: {c} file missing"); continue
        L = flines(m.group(1)); a = int(m.group(2)); b = int(m.group(3) or a)
        if not (1 <= a <= b <= len(L)):
            cp.append(f"{where}: {c} out of range ({len(L)} lines)"); continue
        exact = needle[:1].isspace()
        if not any((l.rstrip() == needle) if exact else (needle in l) for l in L[a - 1:b]):
            cp.append(f"{where}: {c} does not contain its needle {needle!r}")
    for sid, ctr in contracts.items():
        s = ctr["source"]
        if not os.path.exists(os.path.join(ROOT, s["file"])):
            cp.append(f"{sid}: source file missing"); continue
        L = flines(s["file"]); m = re.match(r"^(\d+)(?:-(\d+))?$", s["lines"]); a = int(m.group(1)); b = int(m.group(2) or a)
        if s["citation"] != f"{s['file']}:{s['lines']}" or not (1 <= a <= b <= len(L)):
            cp.append(f"{sid}: source range invalid")
        elif s["tag"] not in L[a - 1]:
            cp.append(f"{sid}: tag {s['tag']!r} not at {s['citation']}")
    pins = measured.get("sourcePins", {})
    moved = [p for p, h in pins.items() if not os.path.exists(os.path.join(ROOT, p)) or hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest() != h]
    rec("citations", not cp, f"{len(allc)} needle citations + {len(contracts)} section source ranges resolve in the sibling source" if not cp else cp[:4])
    rec("source-pins", not moved, f"{len(pins)} cited source files unchanged since the build (sha256)" if not moved else f"source moved since the build, re-run extraction/build_repo.py and re-verify: {moved[:4]}", warn=True)
else:
    rec("citations", False, "no sibling source tree (design-repo used standalone): citation re-check skipped", warn=True)

# ---------------------------------------------------------------- reference copy fidelity
if have_src:
    def n_(s, strip_tags=False):
        s = html.unescape(unicodedata.normalize("NFC", s))
        s = s.replace("\\n", " ").replace('\\"', '"').replace("<br />", " ")
        if strip_tags:
            s = re.sub(r"<[^>]+>", " ", s)
        return re.sub(r"\s+", " ", s).strip()
    raw = " ".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(ROOT, "src", "**", "*.js*"), recursive=True))
    corpus = n_(raw) + " \n " + n_(raw, strip_tags=True)  # attributes (src/alt/href) + text with markup removed
    corpus2 = re.sub(r"\s+", "", corpus)
    missing = []
    for nd in ref["nodes"]:
        for path, key, s in sv.walk_strings(nd["content"], nd["section"]):
            if key in ("assetRole", "kind", "network", "publishedAt", "spinner", "mobileFallback") or key == "plugins" or s.startswith("inline-svg:"):
                continue
            if key == "src" and s.startswith("/"):
                if not os.path.exists(os.path.join(ROOT, "public", s.lstrip("/"))):
                    missing.append(f"{path}: {s[:50]!r} (no such file under public/)")
                continue
            if key == "href" and s not in corpus and s.rstrip("/").rsplit("/", 1)[-1] in corpus:
                continue  # composed in source from a shared prefix + slug (e.g. `${P}presentation-commerciale`)
            if n_(s) not in corpus and re.sub(r"\s+", "", n_(s)) not in corpus2:
                missing.append(f"{path}: {s[:50]!r}")
    rec("copy", not missing, "every reference-example string exists verbatim in src/ and every media src exists under public/" if not missing else f"{len(missing)} reference strings not found in src/: {missing[:3]}")
else:
    rec("copy", False, "no sibling source tree: reference copy fidelity skipped", warn=True)

# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
for name, st, msg in results:
    if not QUIET or st != "PASS":
        print(f"{st:4}  {name:12} {msg}")
print(f"\nverify_all: {sum(1 for r in results if r[1] == 'PASS')} pass, {len(fails)} fail, {sum(1 for r in results if r[1] == 'WARN')} warn")
sys.exit(1 if fails else 0)
