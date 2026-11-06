#!/usr/bin/env python3
"""Semantic validator for PageSpecs: everything Draft-07 cannot express.

    python3 schema/semantic_validate.py <pagespec.json> [...]      # exit 1 on any error
    python3 schema/semantic_validate.py --schema <pagespec.json>    # also run the Draft-07 layer first

Rule ids are stable and named (TEMPLATE_*, NODE_*, MAXWORDS, MOTION_*, the compatibility-graph
rules, RETRIEVAL_*, ASSET_*, TOKEN_*, GENERATED_MODE_*). Every graph rule id in
compatibility/graph.json must be in IMPLEMENTED_GRAPH_RULES (verify_all.py checks both ways).
Standard library only (the --schema flag needs `jsonschema`). Paths derive from __file__.
"""
import json, os, re, sys, unicodedata, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- pins (independent of the registries; editing a registry alone cannot loosen these) ----
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
# runtime / utility UI that must never be retrievable as page content (R8)
RETRIEVAL_INELIGIBLE = {"backdrop.webgl-scene", "chrome.loader", "chrome.menu-overlay", "chrome.seo-modal"}
RUNTIME_UI_PATTERN = re.compile(r"loader|preloader|modal|dialog|overlay|drawer|cookie|consent|toast|cursor|backdrop|webgl|spinner", re.I)
LICENSED_FONTS_BLOCKED_IN_GENERATED = {"font.family.display"}
PLACEHOLDER_HOST = re.compile(r"^https?://([a-z0-9-]+\.)*[a-z0-9-]+\.(example|invalid|test)(/|$)", re.I)
RAW_COLOR = re.compile(r"^\s*(#[0-9a-f]{3,8}|rgba?\(|hsla?\(|[a-z]+\s*$)", re.I)  # hex, functional, or a bare CSS colour name
RAW_LENGTH = re.compile(r"^\s*-?[0-9.]+\s*(px|rem|em|%|vw|vh|lvh|svh|dvh|pt|ch)?\s*$", re.I)
IMPLEMENTED_GRAPH_RULES = {"BACKDROP_FIRST", "ONE_HERO", "HERO_FIRST_IN_FLOW", "FOOTER_LAST", "CLOSING_CTA_BEFORE_FOOTER",
                           "NO_ADJACENT_SAME_CATEGORY", "NO_CONSECUTIVE_SCROLL_STAGES", "SCROLL_STAGE_BUDGET", "THEME_COMBINATION"}
TEXT_LABEL_KEYS = {"label", "ctaLabel", "moreLabel", "menuLabel", "closeLabel"}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[’'`´]", "'", s)
    return re.sub(r"[^a-z0-9%+/'.:-]+", " ", s).strip()


def has(text_n, pat):
    p = norm(pat)
    return bool(p) and re.search(r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])", text_n) is not None


def load(rel, repo):
    with open(os.path.join(repo, rel), encoding="utf-8") as f:
        return json.load(f)


class Ctx:
    def __init__(self, repo=REPO):
        self.repo = repo
        self.templates = load("templates/templates.json", repo)["templates"]
        self.graph = load("compatibility/graph.json", repo)
        self.catalog = load("tokens/llm/token-catalog.json", repo)["tokens"]
        self.policy = load("tokens/llm/token-policy.json", repo)
        self.roles = load("assets/asset-roles.json", repo)["roles"]
        self.identity = load("policy/source-identity.json", repo)
        self.schema = load("schema/pagespec.schema.json", repo)
        self.contracts = {}
        for f in sorted(os.listdir(os.path.join(repo, "sections"))):
            if f.endswith(".json"):
                c = load(f"sections/{f}", repo)
                self.contracts[c["id"]] = c


def walk_strings(o, path="", key=None):
    if isinstance(o, str):
        yield path, key, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk_strings(v, f"{path}.{k}" if path else k, k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_strings(v, f"{path}[{i}]", key)


def walk_media(o, path=""):
    if isinstance(o, dict):
        if "assetRole" in o:
            yield path, o
        for k, v in o.items():
            yield from walk_media(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_media(v, f"{path}[{i}]")


def check_maxwords(schema, inst, path, defs, out):
    if isinstance(schema, dict) and "$ref" in schema:
        schema = defs[schema["$ref"].split("/")[-1]]
    if not isinstance(schema, dict):
        return
    if isinstance(inst, str) and "maxWords" in schema:
        n = len(inst.split())
        if n > schema["maxWords"]:
            out.append(("error", "MAXWORDS", path, f"{n} words > maxWords {schema['maxWords']}"))
    elif isinstance(inst, dict):
        for k, v in inst.items():
            if k in schema.get("properties", {}):
                check_maxwords(schema["properties"][k], v, f"{path}.{k}", defs, out)
    elif isinstance(inst, list) and isinstance(schema.get("items"), dict):
        for i, v in enumerate(inst):
            check_maxwords(schema["items"], v, f"{path}[{i}]", defs, out)


def validate(spec, ctx=None):
    ctx = ctx or Ctx()
    out = []
    E = lambda code, path, msg: out.append(("error", code, path, msg))
    W = lambda code, path, msg: out.append(("warn", code, path, msg))
    mode = spec.get("mode")
    gen = mode == "generated"

    # ---------------- graph/validator agreement
    graph_ids = {r["id"] for r in ctx.graph["rules"]}
    if graph_ids != IMPLEMENTED_GRAPH_RULES:
        E("GRAPH_RULE_UNIMPLEMENTED", "compatibility/graph.json", f"graph rules {sorted(graph_ids ^ IMPLEMENTED_GRAPH_RULES)} not matched by the validator")
    rules = {r["id"]: r for r in ctx.graph["rules"]}
    sev = lambda rid: (E if rules.get(rid, {}).get("severity", "error") == "error" else W)

    # ---------------- template / route
    tid = spec.get("template")
    tpl = ctx.templates.get(tid)
    if not tpl:
        E("TEMPLATE_UNKNOWN", "template", f"{tid!r} not in templates/templates.json")
        return out
    route = spec.get("route", "")
    if mode == "reference" and route not in tpl["routes"]:
        E("TEMPLATE_ROUTE_MISMATCH", "route", f"{route!r} is not a route of {tid}")
    if tpl.get("homeRouteOnly") and route != "/":
        E("TEMPLATE_ROUTE_MISMATCH", "route", f"{tid} is home-route only")

    # ---------------- nodes vs the template's real node list
    nodes = spec.get("nodes", [])
    tnodes = tpl["nodes"]
    tkeys = [(n["section"], n.get("variant", "default")) for n in tnodes]
    seen, ids, pos = set(), set(), []
    for i, n in enumerate(nodes):
        p = f"nodes[{i}]"
        sid, var = n.get("section"), n.get("variant", "default")
        if n.get("id") in ids:
            E("NODE_ID_DUPLICATE", p, f"id {n.get('id')} repeated")
        ids.add(n.get("id"))
        if sid not in ctx.contracts:
            E("NODE_UNKNOWN_SECTION", p, f"{sid!r} has no section contract")
            continue
        if var not in ctx.contracts[sid]["variants"]:
            E("VARIANT_UNKNOWN", p, f"variant {var!r} not in {sid} variants")
        if (sid, var) not in tkeys:
            E("NODE_NOT_IN_TEMPLATE", p, f"{sid}/{var} is not a node of {tid}")
            continue
        tn = tnodes[tkeys.index((sid, var))]
        if (sid, var) in seen and not tn.get("repeatable"):
            E("NODE_DUPLICATE", p, f"{sid}/{var} appears twice but is not repeatable")
        seen.add((sid, var))
        pos.append((tkeys.index((sid, var)), p, sid))
    for (a, _, _), (b, pb, sb) in zip(pos, pos[1:]):
        if b < a:
            E("NODE_ORDER", pb, f"{sb} is out of the template's order")
    for tn in tnodes:
        if tn.get("required") and (tn["section"], tn.get("variant", "default")) not in seen:
            E("NODE_REQUIRED_MISSING", "nodes", f"required node {tn['section']} missing")

    defs = ctx.schema["definitions"]
    check_maxwords(ctx.schema["properties"]["brand"], spec.get("brand", {}), "brand", defs, out)
    present = [n for n in nodes if n.get("section") in ctx.contracts]
    for i, n in enumerate(nodes):
        p, sid = f"nodes[{i}]", n.get("section")
        c = ctx.contracts.get(sid)
        if not c:
            continue
        check_maxwords(c["content"], n.get("content", {}), f"{p}.content", defs, out)
        # motion
        m = n.get("motion", {})
        if "reducedMotionFallback" not in m:
            E("MOTION_FALLBACK_MISSING", f"{p}.motion", "reducedMotionFallback is required")
        elif m["reducedMotionFallback"] != c["motion"]["reducedMotionFallback"]:
            E("MOTION_FALLBACK_MISMATCH", f"{p}.motion", f"{sid} fallback is locked to {c['motion']['reducedMotionFallback']!r}")
        for pat in m.get("patterns", []):
            if pat not in c["motion"]["allowedPatterns"]:
                E("MOTION_PATTERN_NOT_ALLOWED", f"{p}.motion", f"{pat!r} not allowed in {sid}")
        # retrieval (R8)
        pinned_eligible = sid not in RETRIEVAL_INELIGIBLE
        if RUNTIME_UI_PATTERN.search(sid + " " + c.get("title", "")) and pinned_eligible:
            E("RETRIEVAL_RUNTIME_UNPINNED", p, f"{sid} looks like runtime UI but is not in RETRIEVAL_INELIGIBLE")
        if c.get("retrievalEligible") != pinned_eligible:
            E("RETRIEVAL_CONTRACT_DRIFT", p, f"contract {sid} retrievalEligible={c.get('retrievalEligible')} contradicts the pin ({pinned_eligible})")
        if "retrievalEligible" in n and n["retrievalEligible"] != pinned_eligible:
            E("RETRIEVAL_PIN_MISMATCH", f"{p}.retrievalEligible", f"{sid} is pinned retrievalEligible={pinned_eligible}")
        # assets
        allowed_roles = set(c["generatedAssetRoles"]) if gen else set(c["assetRoles"]) | set(c["generatedAssetRoles"])
        for mp, media in walk_media(n.get("content", {}), f"{p}.content"):
            r = media.get("assetRole")
            if r not in PINNED_AVAILABILITY:
                E("ASSET_ROLE_UNKNOWN", mp, f"asset role {r!r} is not in the closed vocabulary")
                continue
            if ctx.roles.get(r, {}).get("availability") != PINNED_AVAILABILITY[r]:
                E("ASSET_AVAILABILITY_DRIFT", mp, f"assets/asset-roles.json says {ctx.roles.get(r, {}).get('availability')!r} for {r}, pinned {PINNED_AVAILABILITY[r]!r}")
            if gen and PINNED_AVAILABILITY[r] != "generation-safe":
                E("GENERATED_MODE_ASSET", mp, f"{r} is {PINNED_AVAILABILITY[r]}; use one of {ctx.roles.get(r, {}).get('generationSafeSubstitutes')}")
            elif r not in allowed_roles:
                E("ASSET_ROLE_NOT_ALLOWED", mp, f"{r} not allowed in {sid} ({mode} mode)")
            srcv = media.get("src")
            if gen and srcv is not None and not PLACEHOLDER_HOST.match(srcv):
                E("GENERATED_MODE_ASSET", f"{mp}.src", "generated media src must be absent or on a reserved .example/.invalid/.test host")
            if not gen and PINNED_AVAILABILITY[r] != "generation-safe" and not srcv:
                E("REFERENCE_MEDIA_SRC_MISSING", mp, f"reference-mode {r} must point at the real asset")
        # tokens
        tk = n.get("tokens", {})
        for slot, val in tk.items():
            tp = f"{p}.tokens.{slot}"
            sp = ctx.policy["nodeSlots"].get(slot)
            if RAW_COLOR.match(val):
                E("TOKEN_RAW_COLOR", tp, f"raw colour {val!r}; reference a color.* token")
            elif RAW_LENGTH.match(val):
                E("TOKEN_SPACING_ARBITRARY", tp, f"raw length {val!r}; use a space.* token")
            elif val not in ctx.catalog:
                E("TOKEN_UNKNOWN", tp, f"{val!r} is not in tokens/llm/token-catalog.json")
            elif sp is None or val not in sp["allowed"] or ctx.catalog[val]["category"] not in sp["allowedCategories"]:
                E("TOKEN_SLOT_NOT_ALLOWED", tp, f"{val!r} not allowed for slot {slot}")
        st = tk.get("surfaceTone")
        combos = ctx.policy["themeCombinations"].get(st) if st else None
        if combos:
            for slot in ("textTone", "accentColor"):
                if slot in tk and tk[slot] not in combos.get(slot, []):
                    sev("THEME_COMBINATION")("THEME_COMBINATION", f"{p}.tokens.{slot}", f"{tk[slot]} not allowed on {st}")

    # ---------------- page-level tokens
    if spec.get("theme") != "light":
        E("TOKEN_THEME_INVALID", "theme", f"theme {spec.get('theme')!r} is not a validated theme")
    for slot in ("display", "text"):
        v = spec.get("fonts", {}).get(slot)
        rule = ctx.policy["pageLevel"].get(f"fonts.{slot}", {})
        if v not in ctx.catalog or ctx.catalog[v]["category"] != "font" or v not in rule.get("allowed", []):
            E("TOKEN_FONT_UNSUPPORTED", f"fonts.{slot}", f"{v!r} is not an approved font token for fonts.{slot}")
        elif gen and v in LICENSED_FONTS_BLOCKED_IN_GENERATED:
            E("TOKEN_LICENSED_FONT_GENERATED", f"fonts.{slot}", f"{v} is a licensed typeface blocked in generated mode; use {ctx.policy['licensedTokens'].get(v, {}).get('substitute')}")

    # ---------------- compatibility graph
    secs = [n.get("section") for n in present]
    cat = lambda s: ctx.contracts[s]["semantic"]["category"]
    inflow = [s for s in secs if ctx.contracts[s]["positionKind"] == "in-flow"]
    if secs and secs[0] != "backdrop.webgl-scene":
        sev("BACKDROP_FIRST")("BACKDROP_FIRST", "nodes[0]", "the first node must be backdrop.webgl-scene")
    heroes = [s for s in secs if cat(s) == "HERO"]
    if len(heroes) != 1:
        sev("ONE_HERO")("ONE_HERO", "nodes", f"{len(heroes)} HERO nodes (exactly one required)")
    if inflow and cat(inflow[0]) != "HERO":
        sev("HERO_FIRST_IN_FLOW")("HERO_FIRST_IN_FLOW", "nodes", f"first in-flow node is {inflow[0]}, not the HERO")
    if secs and secs[-1] != "chrome.footer":
        sev("FOOTER_LAST")("FOOTER_LAST", "nodes", "chrome.footer must be the last node")
    if "chrome.footer" in secs and (secs.index("chrome.footer") == 0 or secs[secs.index("chrome.footer") - 1] != "conversion.closing-cta"):
        sev("CLOSING_CTA_BEFORE_FOOTER")("CLOSING_CTA_BEFORE_FOOTER", "nodes", "conversion.closing-cta must immediately precede chrome.footer")
    ex_cat = [tuple(x) for x in rules.get("NO_ADJACENT_SAME_CATEGORY", {}).get("exceptions", [])]
    ex_stage = [tuple(x) for x in rules.get("NO_CONSECUTIVE_SCROLL_STAGES", {}).get("exceptions", [])]
    for a, b in zip(inflow, inflow[1:]):
        if cat(a) == cat(b) and (a, b) not in ex_cat:
            sev("NO_ADJACENT_SAME_CATEGORY")("NO_ADJACENT_SAME_CATEGORY", "nodes", f"{a} -> {b} are both {cat(a)}")
        if ctx.contracts[a]["scrollStage"] and ctx.contracts[b]["scrollStage"] and (a, b) not in ex_stage:
            sev("NO_CONSECUTIVE_SCROLL_STAGES")("NO_CONSECUTIVE_SCROLL_STAGES", "nodes", f"{a} -> {b} are consecutive pinned stages")
    stages = sum(1 for s in inflow if ctx.contracts[s]["scrollStage"])
    if stages > rules.get("SCROLL_STAGE_BUDGET", {}).get("max", 5):
        sev("SCROLL_STAGE_BUDGET")("SCROLL_STAGE_BUDGET", "nodes", f"{stages} pinned stages")

    # ---------------- generated mode: no source identity or content (R2)
    if gen:
        idn = ctx.identity
        if spec.get("brand", {}).get("isFictional") is not True:
            E("GENERATED_MODE_PERSON", "brand.isFictional", "a generated page's brand must be fictional or user-supplied (isFictional: true)")
        shingle_set = set(idn["copyShingles"]["values"])
        size = idn["copyShingles"]["size"]
        cta_n = {norm(c) for c in idn["ctaStrings"]}
        def titles(o, path=""):  # lead + emphasis are one sentence on screen: also scan them joined
            if isinstance(o, dict):
                if isinstance(o.get("lead"), str) and isinstance(o.get("emphasis"), str):
                    yield path, "titleJoined", f"{o['lead']} {o['emphasis']}"
                for k, v in o.items():
                    yield from titles(v, f"{path}.{k}" if path else k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    yield from titles(v, f"{path}[{i}]")
        for path, key, s in list(walk_strings(spec)) + list(titles(spec)):
            if key in ("assetRole", "section", "variant", "mode", "template", "theme", "locale", "kind", "network", "reducedMotionFallback", "pageSpecVersion", "id") or path.startswith(("fonts", "nodes")) and ".tokens." in path:
                continue
            if key == "patterns" or ".motion." in path:
                continue
            t = norm(s)
            low = s.lower()
            for pat in idn["sourceBrand"]["patterns"]:
                if has(t, pat):
                    E("GENERATED_MODE_BRAND", path, f"source brand {pat!r}")
            if key in ("href", "src") or re.match(r"^(https?:)?//", s):
                if any(d in low for d in idn["domains"]):
                    E("GENERATED_MODE_URL", path, "source domain / profile URL")
                elif re.match(r"^(https?:)?//", s) and not PLACEHOLDER_HOST.match(s):
                    E("GENERATED_MODE_URL", path, "absolute URLs in generated pages must use a reserved .example/.invalid/.test host")
                if any(s.startswith(pfx) or pfx in s for pfx in idn["assetPathPrefixes"]):
                    E("GENERATED_MODE_URL", path, "source asset path")
            elif any(d in low for d in idn["domains"]):
                E("GENERATED_MODE_URL", path, "source domain in text")
            for pat in idn["storePatterns"]:
                if norm(pat) in t:
                    E("GENERATED_MODE_STORE", path, f"app-store mark/link {pat!r}")
            if key in TEXT_LABEL_KEYS and t in cta_n:
                E("GENERATED_MODE_CTA", path, f"source CTA {s!r}")
            for pat in idn["distinctivePhrases"]:
                if norm(pat) in t:
                    E("GENERATED_MODE_COPY", path, f"source phrase {pat!r}")
                    break
            else:
                w = t.split()
                if any(hashlib.sha256(" ".join(w[i:i + size]).encode()).hexdigest()[:16] in shingle_set for i in range(len(w) - size + 1)):
                    E("GENERATED_MODE_COPY", path, "reuses a 6-word run of the source copy")
            for pat in idn["claimPatterns"]:
                if norm(pat) in t:
                    E("GENERATED_MODE_CLAIM", path, f"source claim/statistic {pat!r}")
            for pat in idn["ratingPatterns"]:
                if norm(pat) in t:
                    E("GENERATED_MODE_RATING", path, f"source rating {pat!r}")
            for pat in idn["personNames"] + idn["clientNames"]:
                if has(t, pat):
                    E("GENERATED_MODE_PERSON", path, f"real person/client identity {pat!r}")
        for i, n in enumerate(nodes):
            c = n.get("content", {})
            for j, r in enumerate(c.get("reviews", []) if isinstance(c.get("reviews"), list) else []):
                if r.get("person", {}).get("isFictional") is not True:
                    E("GENERATED_MODE_PERSON", f"nodes[{i}].content.reviews[{j}].person", "generated testimonials must be fictional (isFictional: true)")
            for key in ("cards", "credentials"):
                for j, r in enumerate(c.get(key, []) if isinstance(c.get(key), list) else []):
                    if "isPlaceholder" in r and r["isPlaceholder"] is not True:
                        E("GENERATED_MODE_RATING", f"nodes[{i}].content.{key}[{j}]", "generated credentials/ratings must be placeholders (isPlaceholder: true)")
    return out


def schema_errors(spec, repo=REPO):
    from jsonschema import Draft7Validator
    v = Draft7Validator(load("schema/pagespec.schema.json", repo))
    return [("error", "SCHEMA", "/".join(map(str, e.absolute_path)), e.message[:200]) for e in v.iter_errors(spec)]


def main(argv):
    with_schema = "--schema" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    ctx, bad = Ctx(), 0
    for f in files:
        spec = json.load(open(f, encoding="utf-8"))
        res = (schema_errors(spec) if with_schema else []) + validate(spec, ctx)
        errs = [r for r in res if r[0] == "error"]
        warns = [r for r in res if r[0] == "warn"]
        print(f"{f}: {len(errs)} error(s), {len(warns)} warning(s)")
        for lvl, code, path, msg in res:
            print(f"  {lvl.upper():5} {code} {path}: {msg}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
