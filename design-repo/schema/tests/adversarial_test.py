#!/usr/bin/env python3
"""Adversarial suite: every mutation must be rejected with its expected rule id; every control must pass.

    python3 schema/tests/adversarial_test.py           # exit 1 if any mutation slips through or a control fails

Layers exercised: Draft-07 schema, schema/semantic_validate.py (template/node, maxWords, motion, retrieval,
assets, tokens, compatibility graph, generated-mode leakage) and extraction/wrapper_gate.py (R9).
A mutation passes the test only if (a) at least one error-level finding exists and (b) one of its expected
rule ids is among the findings (warn-level cases assert the warning and zero errors instead).
"""
import copy, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))


def mod(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sv = mod("schema/semantic_validate.py", "semantic_validate")
wg = mod("extraction/wrapper_gate.py", "wrapper_gate")
load = lambda rel: json.load(open(os.path.join(REPO, rel), encoding="utf-8"))
REF = load("schema/example.pagespec.json")
GEN = load("schema/examples/generated.home.pagespec.json")
BASE_CTX = sv.Ctx(REPO)


def node(spec, section):
    return next(n for n in spec["nodes"] if n["section"] == section)


def run(spec, ctx=None):
    return sv.schema_errors(spec, REPO) + sv.validate(spec, ctx or BASE_CTX)


# ------------------------------------------------------------------ mutations: (id, base, fn(spec, ctx), expected codes, level)
M = []


def mut(id_, base, expect, level="error"):
    def deco(fn):
        M.append((id_, base, fn, set(expect), level))
        return fn
    return deco


# schema layer
mut("schema/mode-not-in-enum", "gen", ["SCHEMA"])(lambda s, c: s.update(mode="draft"))
mut("schema/mode-missing", "gen", ["SCHEMA"])(lambda s, c: s.pop("mode"))
mut("schema/invented-section-alias", "gen", ["SCHEMA", "NODE_UNKNOWN_SECTION"])(lambda s, c: node(s, "proof.works").update(section="proof.case-grid"))
mut("schema/missing-reduced-motion-fallback", "gen", ["SCHEMA", "MOTION_FALLBACK_MISSING"])(lambda s, c: node(s, "story.tagline")["motion"].pop("reducedMotionFallback"))
mut("schema/motion-invented-field", "gen", ["SCHEMA"])(lambda s, c: node(s, "story.tagline")["motion"].update(inventedAnimation="spin"))
mut("schema/content-extra-field", "gen", ["SCHEMA"])(lambda s, c: node(s, "story.tagline")["content"].update(subtitle="extra"))
mut("schema/invented-asset-role", "gen", ["SCHEMA", "ASSET_ROLE_UNKNOWN"])(lambda s, c: node(s, "offer.spotlight")["content"]["media"].update(assetRole="photo.anything"))
mut("schema/unknown-token-slot", "gen", ["SCHEMA"])(lambda s, c: node(s, "proof.works").setdefault("tokens", {}).update(shadow="elevation.lg"))
mut("schema/theme-dark", "gen", ["SCHEMA", "TOKEN_THEME_INVALID"])(lambda s, c: s.update(theme="dark"))
mut("schema/variant-unknown", "gen", ["SCHEMA", "VARIANT_UNKNOWN"])(lambda s, c: node(s, "proof.works").update(variant="dark"))
# structure vs the template's real node list
mut("structure/duplicate-hero", "gen", ["NODE_DUPLICATE", "ONE_HERO"])(lambda s, c: s["nodes"].insert(5, dict(copy.deepcopy(node(s, "hero.statement")), id="n99")))
mut("structure/required-footer-removed", "gen", ["NODE_REQUIRED_MISSING"])(lambda s, c: s["nodes"].remove(node(s, "chrome.footer")))
mut("structure/required-closing-cta-removed", "gen", ["NODE_REQUIRED_MISSING", "CLOSING_CTA_BEFORE_FOOTER"])(lambda s, c: s["nodes"].remove(node(s, "conversion.closing-cta")))
mut("structure/faq-moved-before-works", "gen", ["NODE_ORDER"])(lambda s, c: (s["nodes"].remove(node(s, "content.faq")), s["nodes"].insert(5, node(GEN, "content.faq"))))
mut("structure/backdrop-not-first", "gen", ["NODE_ORDER", "BACKDROP_FIRST"])(lambda s, c: s["nodes"].insert(2, s["nodes"].pop(0)))
mut("structure/footer-not-last", "gen", ["NODE_ORDER", "FOOTER_LAST"])(lambda s, c: s["nodes"].insert(len(s["nodes"]) - 3, s["nodes"].pop()))
mut("structure/reference-route-mismatch", "ref", ["TEMPLATE_ROUTE_MISMATCH"])(lambda s, c: s.update(route="/contact"))
mut("structure/template-unknown-semantic", "gen", ["TEMPLATE_UNKNOWN", "SCHEMA"])(lambda s, c: s.update(template="template.article"))
mut("structure/node-id-duplicate", "gen", ["NODE_ID_DUPLICATE"])(lambda s, c: node(s, "proof.works").update(id=node(s, "story.tagline")["id"]))
# runtime word budgets
mut("maxwords/hero-subtitle", "gen", ["MAXWORDS"])(lambda s, c: node(s, "hero.statement")["content"].update(subtitle=" ".join(["word"] * 31)))
mut("maxwords/review-quote", "gen", ["MAXWORDS"])(lambda s, c: node(s, "proof.reviews")["content"]["reviews"][0].update(quote=" ".join(["calm"] * 111)))
mut("maxwords/brand-name", "gen", ["MAXWORDS"])(lambda s, c: s["brand"].update(name="One Two Three Four Five Six Seven"))
# motion
mut("motion/pattern-not-allowed", "gen", ["MOTION_PATTERN_NOT_ALLOWED", "SCHEMA"])(lambda s, c: node(s, "hero.statement")["motion"]["patterns"].append("marquee-loop"))
mut("motion/fallback-mismatch", "gen", ["MOTION_FALLBACK_MISMATCH", "SCHEMA"])(lambda s, c: node(s, "story.tagline")["motion"].update(reducedMotionFallback="final-state"))
# graph (error + warn levels)
mut("graph/rule-unimplemented", "gen", ["GRAPH_RULE_UNIMPLEMENTED"])(lambda s, c: c.graph["rules"].append({"id": "NO_TWO_CTAS", "severity": "error", "description": "x"}))
mut("graph/adjacent-same-category-warn", "gen", ["NO_ADJACENT_SAME_CATEGORY"], "warn")(lambda s, c: s["nodes"].remove(node(s, "story.vr")))
mut("graph/consecutive-stages-warn", "gen", ["NO_CONSECUTIVE_SCROLL_STAGES"], "warn")(lambda s, c: [s["nodes"].remove(node(s, x)) for x in ("proof.works", "proof.method")])
# retrieval eligibility (R8)
mut("retrieval/node-flips-loader-eligible", "ref", ["RETRIEVAL_PIN_MISMATCH"])(lambda s, c: node(s, "chrome.loader").update(retrievalEligible=True))
mut("retrieval/content-section-marked-ineligible", "ref", ["RETRIEVAL_PIN_MISMATCH"])(lambda s, c: node(s, "proof.works").update(retrievalEligible=False))
mut("retrieval/contract-flips-menu-eligible", "ref", ["RETRIEVAL_CONTRACT_DRIFT"])(lambda s, c: c.contracts["chrome.menu-overlay"].update(retrievalEligible=True))
mut("retrieval/contract-marks-content-ineligible", "ref", ["RETRIEVAL_CONTRACT_DRIFT"])(lambda s, c: c.contracts["proof.reviews"].update(retrievalEligible=False))


def add_cookie_banner(s, c):
    c.contracts["chrome.cookie-banner"] = dict(copy.deepcopy(c.contracts["chrome.header"]), id="chrome.cookie-banner", title="Cookie consent banner", retrievalEligible=True)
    c.templates["template.home"]["nodes"].insert(3, {"section": "chrome.cookie-banner", "variant": "default", "required": False, "repeatable": False})
    s["nodes"].insert(3, dict(copy.deepcopy(node(s, "chrome.header")), id="n98", section="chrome.cookie-banner"))


mut("retrieval/runtime-ui-not-pinned", "ref", ["RETRIEVAL_RUNTIME_UNPINNED"])(add_cookie_banner)
# assets (R3)
mut("asset/real-wordmark-in-generated", "gen", ["GENERATED_MODE_ASSET"])(lambda s, c: node(s, "chrome.header")["content"].update(brandMark={"assetRole": "brand.wordmark", "alt": "logo"}))
mut("asset/client-photo-in-generated", "gen", ["GENERATED_MODE_ASSET", "GENERATED_MODE_URL"])(lambda s, c: node(s, "proof.works")["content"]["cards"][0].update(media={"assetRole": "case.photo", "src": "/sk/uploads/Safran_0239f5157e.jpg", "alt": "x"}))
mut("asset/client-logo-in-generated-review", "gen", ["GENERATED_MODE_ASSET"])(lambda s, c: node(s, "proof.reviews")["content"]["reviews"][0].update(media={"assetRole": "client.logo", "alt": "logo"}))
mut("asset/proprietary-video", "gen", ["GENERATED_MODE_ASSET", "GENERATED_MODE_URL"])(lambda s, c: node(s, "hero.statement")["content"].update(video={"assetRole": "hero.loop-video", "src": "/sk/uploads/home_video_SD_79c96be094.mp4"}))
mut("asset/generated-image-on-real-host", "gen", ["GENERATED_MODE_ASSET", "GENERATED_MODE_URL"])(lambda s, c: node(s, "offer.spotlight")["content"]["media"].update(src="https://cdn.somewhere.com/team.jpg"))
mut("asset/credential-badge-in-generated", "gen", ["GENERATED_MODE_ASSET"])(lambda s, c: node(s, "proof.labels")["content"]["cards"][0].update(media={"assetRole": "credential.badge", "alt": "badge"}))
mut("asset/role-not-allowed-in-section", "ref", ["ASSET_ROLE_NOT_ALLOWED"])(lambda s, c: node(s, "hero.statement")["content"].update(video={"assetRole": "case.photo", "src": "/sk/uploads/Safran_0239f5157e.jpg"}))
mut("asset/registry-loosened-pin-holds", "gen", ["ASSET_AVAILABILITY_DRIFT", "GENERATED_MODE_ASSET"])(lambda s, c: (c.roles["brand.wordmark"].update(availability="generation-safe"), node(s, "chrome.header")["content"].update(brandMark={"assetRole": "brand.wordmark", "alt": "logo"})))
mut("asset/reference-media-without-src", "ref", ["REFERENCE_MEDIA_SRC_MISSING"])(lambda s, c: node(s, "proof.works")["content"]["cards"][0]["media"].pop("src"))
# generated-mode leakage (R2)
mut("leak/brand-name", "gen", ["GENERATED_MODE_BRAND"])(lambda s, c: s["brand"].update(name="La Boîte à Slides"))
mut("leak/brand-in-copy", "gen", ["GENERATED_MODE_BRAND"])(lambda s, c: node(s, "story.tagline")["content"].update(body="Built the LABAS way, slide after slide."))
mut("leak/brand-domain-word", "gen", ["GENERATED_MODE_BRAND", "GENERATED_MODE_URL"])(lambda s, c: node(s, "offer.spotlight")["content"].update(body="Inspired by laboiteaslides.fr and its studio."))
mut("leak/brand-not-fictional", "gen", ["GENERATED_MODE_PERSON"])(lambda s, c: s["brand"].update(isFictional=False))
mut("leak/store-url", "gen", ["GENERATED_MODE_URL", "GENERATED_MODE_STORE"])(lambda s, c: node(s, "chrome.header")["content"]["cta"].update(href="https://apps.apple.com/app/id123456"))
mut("leak/store-mark-text", "gen", ["GENERATED_MODE_STORE"])(lambda s, c: node(s, "conversion.closing-cta")["content"]["cta"].update(label="Download on the App Store"))
mut("leak/source-url", "gen", ["GENERATED_MODE_URL"])(lambda s, c: node(s, "chrome.header")["content"]["cta"].update(href="https://laboiteaslides.fr/contact"))
mut("leak/source-social-profile", "gen", ["GENERATED_MODE_URL"])(lambda s, c: node(s, "chrome.footer")["content"]["socials"][0].update(href="https://www.linkedin.com/company/laboiteaslides/"))
mut("leak/non-placeholder-absolute-url", "gen", ["GENERATED_MODE_URL"])(lambda s, c: node(s, "chrome.footer")["content"]["legalLinks"][0].update(href="https://realcompany.com/legal"))
mut("leak/source-cta", "gen", ["GENERATED_MODE_CTA"])(lambda s, c: node(s, "chrome.header")["content"]["cta"].update(label="Demander un devis"))
mut("leak/source-heading", "gen", ["GENERATED_MODE_COPY"])(lambda s, c: node(s, "proof.works")["content"].update(title={"lead": "Un seul outil, des", "emphasis": "possibilités infinies"}))
mut("leak/source-tagline-copy", "gen", ["GENERATED_MODE_COPY"])(lambda s, c: node(s, "story.tagline")["content"].update(statement=node(REF, "story.tagline")["content"]["statement"]))
mut("leak/source-faq-answer-fragment", "gen", ["GENERATED_MODE_COPY"])(lambda s, c: node(s, "content.faq")["content"]["items"][0].update(answer="Nous prenons le temps de comprendre vos attentes, puis on avance."))
mut("leak/real-review-quote", "gen", ["GENERATED_MODE_COPY"])(lambda s, c: node(s, "proof.reviews")["content"]["reviews"][0].update(quote=node(REF, "proof.reviews")["content"]["reviews"][0]["quote"]))
mut("leak/real-reviewer-name", "gen", ["GENERATED_MODE_PERSON"])(lambda s, c: node(s, "proof.reviews")["content"]["reviews"][0]["person"].update(name="Teddy G."))
mut("leak/reviewer-not-fictional", "gen", ["GENERATED_MODE_PERSON"])(lambda s, c: node(s, "proof.reviews")["content"]["reviews"][1]["person"].update(isFictional=False))
mut("leak/real-client-name", "gen", ["GENERATED_MODE_PERSON"])(lambda s, c: node(s, "proof.works")["content"]["cards"][0].update(client="Safran"))
mut("leak/real-rating", "gen", ["GENERATED_MODE_RATING"])(lambda s, c: node(s, "proof.method")["content"]["metrics"].__setitem__(0, "5/5 Note Google Avis"))
mut("leak/credential-not-placeholder", "gen", ["GENERATED_MODE_RATING"])(lambda s, c: node(s, "proof.labels")["content"]["cards"][0].update(isPlaceholder=False))
mut("leak/source-certification-claim", "gen", ["GENERATED_MODE_CLAIM"])(lambda s, c: node(s, "offer.skills")["content"]["items"][0].update(statement="Certified ISO 9001 schedules agreed on day one."))
mut("leak/source-statistic", "gen", ["GENERATED_MODE_CLAIM"])(lambda s, c: node(s, "proof.method")["content"]["marquee"].__setitem__(0, "+8 000 projets"))
# tokens (R10)
mut("token/raw-hex", "gen", ["TOKEN_RAW_COLOR"])(lambda s, c: node(s, "proof.works")["tokens"].update(textTone="#ff00ff"))
mut("token/raw-rgb", "gen", ["TOKEN_RAW_COLOR"])(lambda s, c: node(s, "proof.works")["tokens"].update(accentColor="rgb(102, 48, 255)"))
mut("token/raw-colour-name", "gen", ["TOKEN_RAW_COLOR"])(lambda s, c: node(s, "proof.works")["tokens"].update(accentColor="purple"))
mut("token/arbitrary-spacing", "gen", ["TOKEN_SPACING_ARBITRARY"])(lambda s, c: node(s, "proof.works")["tokens"].update(blockGap="37px"))
mut("token/unknown-token", "gen", ["TOKEN_UNKNOWN"])(lambda s, c: node(s, "proof.works")["tokens"].update(accentColor="color.neon"))
mut("token/slot-not-allowed", "gen", ["TOKEN_SLOT_NOT_ALLOWED"])(lambda s, c: node(s, "proof.works")["tokens"].update(surfaceTone="backdrop.gry"))
mut("token/space-token-in-colour-slot", "gen", ["TOKEN_SLOT_NOT_ALLOWED"])(lambda s, c: node(s, "proof.works")["tokens"].update(textTone="space.20"))
mut("token/unsupported-font-name", "gen", ["TOKEN_FONT_UNSUPPORTED"])(lambda s, c: s["fonts"].update(display="Comic Sans MS"))
mut("token/font-token-not-allowed-for-slot", "gen", ["TOKEN_FONT_UNSUPPORTED"])(lambda s, c: s["fonts"].update(display="font.family.system-arial"))
mut("token/licensed-font-in-generated", "gen", ["TOKEN_LICENSED_FONT_GENERATED"])(lambda s, c: s["fonts"].update(display="font.family.display"))
mut("token/invalid-theme-combination", "gen", ["THEME_COMBINATION"])(lambda s, c: node(s, "proof.works")["tokens"].update(textTone="color.lgh1"))
mut("token/invalid-accent-on-purple", "gen", ["THEME_COMBINATION"])(lambda s, c: node(s, "conversion.closing-cta")["tokens"].update(accentColor="color.prm1"))


def run_mutations():
    rows, failed = [], 0
    for id_, base, fn, expect, level in M:
        spec = copy.deepcopy(REF if base == "ref" else GEN)
        ctx = copy.deepcopy(BASE_CTX)
        fn(spec, ctx)
        res = run(spec, ctx)
        errs = [r for r in res if r[0] == "error"]
        codes = {r[1] for r in res if r[0] == level}
        if level == "error":
            ok = bool(errs) and bool(codes & expect)
        else:
            ok = not errs and bool(codes & expect)
        failed += not ok
        rows.append((("REJECTED" if level == "error" else "WARNED") if ok else "SLIPPED", id_, sorted(codes & expect) or sorted({r[1] for r in res})[:3]))
    return rows, failed


# ------------------------------------------------------------------ wrapper gate cases (R9)
MEAS = load("extraction/measured-values.json")
CONTRACTS = BASE_CTX.contracts
TPLS = BASE_CTX.templates


def gate(fn):
    m = copy.deepcopy(MEAS)
    fn(m)
    return wg.evaluate(m, CONTRACTS, TPLS)


H = lambda m, s: m["sectionHeights"]["routes"]["/"]["sections"][s]
WL = lambda m: m["wrapperGate"]["whitelist"]
GATE = [
    ("gate/hero-1900-warns", lambda m: (H(m, "hero.statement").update(heightPx=1900), WL(m).clear()), "warn", "> 1800px"),
    ("gate/hero-3100-not-whitelisted", lambda m: (H(m, "hero.statement").update(heightPx=3100), WL(m).clear()), "error", "not whitelisted"),
    ("gate/majority-share", lambda m: H(m, "proof.works").update(heightPx=30000), "error", "of the page"),
    ("gate/whitelist-missing-justification", lambda m: WL(m)[0].update(justification=""), "error", "justification"),
    ("gate/whitelist-agent-without-disclaimer", lambda m: WL(m)[0].update(reviewedBy="Claude (AI agent)"), "error", "agent reviewer"),
    ("gate/whitelist-over-cap", lambda m: WL(m)[0].update(maxHeightPx=6000), "error", "maxHeightPx"),
    ("gate/whitelist-stale", lambda m: H(m, "hero.statement").update(heightPx=1500), "error", "stale"),
    ("gate/missing-measurement", lambda m: H(m, "story.tagline").pop("heightPx"), "error", "missing measurement"),
    ("gate/wrong-viewport", lambda m: m["sectionHeights"].update(viewport="1280x800"), "error", "gate requires"),
]


def run_gate():
    rows, failed = [], 0
    for id_, fn, level, needle in GATE:
        errs, warns = gate(fn)
        pool = errs if level == "error" else warns
        ok = any(needle in x for x in pool) and (level == "error" or not errs)
        failed += not ok
        rows.append((("REJECTED" if level == "error" else "WARNED") if ok else "SLIPPED", id_, [x for x in pool if needle in x][:1] or (errs + warns)[:2]))
    return rows, failed


# ------------------------------------------------------------------ controls
def controls():
    rows, failed = [], 0
    cases = [("control/reference-example (real assets)", REF), ("control/generated-example", GEN)]
    for tid, t in TPLS.items():  # one minimal control per template, synthesised from its own node list
        req = [n["section"] for n in t["nodes"] if n.get("required")]
        cases.append((f"control/{tid}-required-only (generated)", dict(copy.deepcopy(GEN), nodes=[copy.deepcopy(node(GEN, s)) for s in req])))
    for name, spec in cases:
        res = run(spec)
        errs = [r for r in res if r[0] == "error"]
        failed += bool(errs)
        rows.append(("PASSES" if not errs else "FAILED", name, errs[:2] or f"0 errors, {len(res)} warnings"))
    errs, warns = wg.evaluate(MEAS, CONTRACTS, TPLS)
    failed += bool(errs)
    rows.append(("PASSES" if not errs else "FAILED", "control/wrapper-gate on measured heights", errs[:2] or f"0 errors, {len(warns)} warnings"))
    return rows, failed


if __name__ == "__main__":
    r1, f1 = run_mutations()
    r2, f2 = run_gate()
    r3, f3 = controls()
    for st, id_, info in r1 + r2 + r3:
        print(f"{st:8} {id_:48} {info}")
    total_m = len(r1) + len(r2)
    print(f"\nadversarial: {total_m - f1 - f2}/{total_m} mutations rejected (incl. {len(r2)} wrapper-gate cases), {len(r3) - f3}/{len(r3)} controls pass")
    sys.exit(1 if f1 or f2 or f3 else 0)
