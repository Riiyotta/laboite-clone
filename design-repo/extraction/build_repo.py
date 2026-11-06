#!/usr/bin/env python3
"""Builder for this design-repo: derives every contract from the clone's REAL source.

    python3 extraction/build_repo.py           # run from anywhere; needs the sibling clone (../src, ../CLONE_SPEC_*.md)

Citations are resolved by NEEDLE (a literal string searched in the cited file), never typed as
line numbers, so re-running the builder after a source change re-points every citation (R16).
The builder refuses to run without the sibling source tree; the *checks* (verify_all.py,
semantic_validate.py, adversarial_test.py, prove_drift.py) do not need it.

Hand-maintained inputs live in this file (section intent, maxWords budgets, motion/fallback
choices, the generated-mode example); everything numeric (token values, line ranges, word counts
of the real copy, token catalog, policy hash) is read from the source or recomputed.
"""
import hashlib, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.dirname(REPO)  # the clone project (src/, public/, CLONE_SPEC_*.md)
if not os.path.isdir(os.path.join(ROOT, "src")):
    sys.exit("build_repo.py needs the sibling clone source tree (../src). The checks do not; run extraction/verify_all.py instead.")
sys.path.insert(0, HERE)
import policy_hash  # noqa: E402

VERSION = "1.0.1"
_cache = {}


def lines(path):
    if path not in _cache:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            _cache[path] = f.read().split("\n")
    return _cache[path]


def find(path, needle, after=1):
    """Needles that start with whitespace must equal the whole (right-stripped) line, e.g. a root closing tag at its indentation."""
    exact = needle[:1].isspace()
    for i, l in enumerate(lines(path), 1):
        if i >= after and (l.rstrip() == needle if exact else needle in l):
            return i
    raise SystemExit(f"needle not found: {path}: {needle!r} (after line {after})")


def cite(path, needle, end=None, after=None):
    """{'cite': 'path:a[-b]', 'needle': needle}; a = first line containing needle (after `after`), b = first line >= a containing end."""
    a = find(path, needle, find(path, after) if after else 1)
    b = find(path, end, a) if end else a
    return {"cite": f"{path}:{a}" + (f"-{b}" if b != a else ""), "needle": needle}


def dump(rel, obj):
    p = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def words(s):
    return len([w for w in re.split(r"\s+", s.strip()) if w])


T, IDX = "tailwind.config.js", "src/index.css"
SA, SB, SAA = "CLONE_SPEC_A.md", "CLONE_SPEC_B.md", "CLONE_SPEC_A_ASSETS.md"
C = "src/components/"

# ----------------------------------------------------------------------------------- tokens
def tok(type_, value, evidence, usage=None, **extra):
    d = {"type": type_, "value": value, "evidence": evidence if isinstance(evidence, list) else [evidence]}
    if usage:
        d["usage"] = usage
    d.update(extra)
    return d


COLORS = [("lgh1", "#ffffff", "light / white: inverse text, light buttons, glass tint"),
          ("drk1", "#120042", "dark navy: primary text, dark buttons, navy backdrop"),
          ("gry1", "#cecece", "light grey (declared palette; grey backdrop pair)"),
          ("gry2", "#aca6bd", "lavender grey (declared palette)"),
          ("gry3", "#5f5f5f", "mid grey: VR body copy end colour"),
          ("prm1", "#6630ff", "primary violet: emphasis words, marquee, purple backdrop, hover sweep"),
          ("scd1", "#01daf6", "secondary cyan (declared palette)"),
          ("scd2", "#ff61f8", "secondary pink (declared palette)"),
          ("scd3", "#62f740", "secondary green (declared palette; green backdrop pair top)"),
          ("trt1", "#29daff", "tertiary cyan: logo corner triangle, cyan backdrop pair top"),
          ("trt3", "#70f74a", "tertiary green: logo corner triangle"),
          ("err1", "#d00000", "error red (declared palette)")]
color_tokens = {f"color.{k}": tok("color", v, [cite(T, f"{k}: '{v}'"), cite(IDX, f"--{k}:{v if k != 'lgh1' else '#fff'}"), cite(SA, "### 0.3 Colors", "--lgh1 #FFFFFF")], u)
                for k, v, u in COLORS}
color_tokens["color.glass.light"] = tok("color", "#ffffff1a", cite(IDX, ".glass-lgh { background-color: #ffffff1a"), "superGlass @background[lgh] tint (white 10%)")
color_tokens["color.glass.dark"] = tok("color", "#12004212", cite(IDX, ".glass-drk { background-color: #12004212"), "superGlass @background[drk] tint (navy 7%)")
BACKDROPS = [("lgh", "#ffffff", "#ededed", "LGH `#FFFFFF/#EDEDED`"), ("prm", "#6630ff", "#612ef1", "PRM `#6630FF/#612EF1`"),
             ("scd", "#62f740", "#61ed40", "SCD `#62F740/#61ED40`"), ("trt", "#29daff", "#27cef1", "TRT `#29DAFF/#27CEF1`"),
             ("drk", "#120042", "#10003d", "DRK `#120042/#10003D`"), ("gry", "#cecece", "#cbcbcb", "GRY `#CECECE/#CBCBCB`"),
             ("blk", "#080808", "#080808", "BLK `#080808/#080808`")]
backdrop_tokens = {f"backdrop.{k}": tok("gradientPair", {"top": t, "bottom": b}, cite(SA, n),
                                          "WebGL background shader layer (top/bottom gradient pair); sections choose one as their surface tone")
                   for k, t, b, n in BACKDROPS}
dump("tokens/00-foundation/color.json", {"$description": "Foundation colours: the 12-colour palette declared in tailwind.config.js and :root (src/index.css), the two glass tints, and the WebGL background-shader gradient pairs (CLONE_SPEC_A §0.3). Rendered text uses only lgh1/prm1/drk1 at 1440 (extraction/measured-values.json styleHistogram1440).",
                                          "version": VERSION, "tokens": {**color_tokens, **backdrop_tokens}})

FONT_FAMILIES = {
    "font.family.text": tok("fontFamily", "vInter", [cite(IDX, "font-family: vInter; src: url('/fonts/Inter/Inter.woff2')"), cite(T, "inter: ['vInter'")],
                            "all running text, buttons, labels (Inter variable 100-900)", stack="vInter, sans-serif, arial", file="/fonts/Inter/Inter.woff2", weights="100 900",
                            licence="Inter is published by its author under the SIL Open Font License 1.1 upstream; the clone ships no licence file, so record the OFL text when redistributing."),
    "font.family.display": tok("fontFamily", "FKScreamer", [cite(IDX, "font-family: FKScreamer; src: url('/fonts/FKScreamer"), cite(SA, "only one face — weight 700/900 requested")],
                               "condensed uppercase display titles; one 400 face only, never synthesised bold", stack="FKScreamer, sans-serif, arial", file="/fonts/FKScreamer/woff2/FKScreamerLegacy-Upright.woff2", weights="400",
                               licence="commercial typeface (FK Screamer); no licence file in the clone; reference mode only, blocked for generated pages (see tokens/llm/token-policy.json licensedTokens)"),
    "font.family.system-arial": tok("fontFamily", "Arial", cite("src/components/faq/faq.css", "font-family: Arial; font-size: 1.8rem"), "FAQ question buttons (system font, as measured on the live page)", stack="Arial"),
}
FS = [("micro", "max(1.1rem, 11px)", "src/components/footer/footer.css", "font-size: max(1.1rem, 11px)", "tiny uppercase labels (lang switch, nav titles)"),
      ("caption", "max(1.2rem, 12px)", "src/components/expertises/expertises.css", "font-size: max(1.2rem, 12px)", "uppercase overline captions (NOS EXPERTISES, FAQ, nav group titles)"),
      ("body-sm", "1.5rem", IDX, "font-size: 1.5rem; font-weight: 500", "buttons, small body, card meta, metrics"),
      ("body", "1.6rem", "src/components/hero/hero.css", "font-size: 1.6rem; font-weight: 400; line-height: 1.6", "SEO modal prose"),
      ("body-lg", "1.8rem", "src/components/review-cards/reviewCards.css", ".reviewCard__content { overflow: hidden; font-size: 1.8rem", "review quotes, FAQ questions"),
      ("lead-sm", "2rem", "src/components/footer/footer.css", ".footerNav__route--expertise { font-size: 2rem", "mobile footer/menu lists"),
      ("lead", "2.4rem", "src/components/method/method.css", ".method__content { font-size: 2.4rem", "lead paragraphs, footer explore links"),
      ("title-xs", "3rem", "src/components/hero/hero.css", ".seoContent h3 { font-size: 3rem", "SEO h3"),
      ("title-sm", "3.2rem", "src/components/header/header.css", ".menu__explore-route { font-family: vInter; font-synthesis: none; font-size: 3.2rem", "menu explore links, white-paper titles"),
      ("title-md", "4rem", "src/components/works/works.css", ".workCard__title { color: #fff; font-size: 4rem", "card titles; statement size on mobile"),
      ("statement", "5.2rem", "src/components/hero/hero.css", ".hero__subtitle { font-family: vInter; font-synthesis: none; font-size: 5.2rem", "Inter statements (hero subtitle, tagline, method tagline, skills)"),
      ("title-lg", "6rem", "src/components/hero/hero.css", ".seoContent h2 { font-family: FKScreamer", "SEO h2"),
      ("title-xl", "6.4rem", "src/components/resource-cards/resource-cards.css", ".rcs.is-whole .rc .rc__title { font-size: 6.4rem", "resource card titles, menu expertise widget"),
      ("display-sm", "9.6rem", "src/components/expertises/expertises.css", ".exp .exp__router { display: flex", "expertise labels below desktop"),
      ("display-md", "11.2rem", "src/components/works/works.css", ".works .works__title { word-break: break-word; font-size: 11.2rem", "section titles (works, VR, spotlight, resources, reviews, FAQ)"),
      ("display-lg", "16.4rem", "src/components/footer/footer.css", "font-size: 16.4rem; font-weight: 700; line-height: .75", "hero/footer titles, expertise labels"),
      ("display-xl", "25.2rem", "src/components/method/method.css", ".method__marquee-title { color: #6630ff; font-size: 25.2rem", "marquee, label-cards title")]
fs_tokens = {f"fontSize.{k}": tok("fontSize", v, cite(p, n), u) for k, v, p, n, u in FS}
FW = {"400": ("src/components/hero/hero.css", "font-size: 1.6rem; font-weight: 400"), "500": (IDX, "font-size: 1.5rem; font-weight: 500"),
      "600": ("src/components/hero/hero.css", "font-size: 5.2rem; font-weight: 600"), "700": ("src/components/works/works.css", "font-size: 11.2rem; font-weight: 700")}
fw_tokens = {f"fontWeight.{k}": tok("fontWeight", int(k), cite(p, n)) for k, (p, n) in FW.items()}
LH = [("tightest", ".75", "src/components/hero/hero.css", "font-size: 16.4rem; font-weight: 700; line-height: .75"), ("tighter", ".8", "src/components/works/works.css", "font-weight: 700; line-height: .8"),
      ("tight", ".85", "src/components/resource-cards/resource-cards.css", "line-height: .85; text-align: center"), ("snug", ".9", "src/components/works/works.css", "font-weight: 700; line-height: .9"),
      ("statement", "1.04", "src/components/hero/hero.css", "letter-spacing: -.04em; line-height: 1.04"), ("lead", "1.3", "src/components/method/method.css", "letter-spacing: -.02em; line-height: 1.3"),
      ("body", "1.4", IDX, "font-weight: 500; line-height: 1.4"), ("prose", "1.6", "src/components/hero/hero.css", "font-weight: 400; line-height: 1.6"),
      ("caption", "1.5rem", "src/components/expertises/expertises.css", "font-weight: 600; line-height: 1.5rem")]
lh_tokens = {f"lineHeight.{k}": tok("lineHeight", v, cite(p, n)) for k, v, p, n in LH}
ls_tokens = {"letterSpacing.statement": tok("letterSpacing", "-.04em", cite("src/components/hero/hero.css", "letter-spacing: -.04em")),
             "letterSpacing.lead": tok("letterSpacing", "-.02em", cite("src/components/method/method.css", "letter-spacing: -.02em")),
             "letterSpacing.prose-h4": tok("letterSpacing", ".02em", cite("src/components/hero/hero.css", "letter-spacing: .02em"))}
tt_tokens = {"textTransform.display": tok("textTransform", "uppercase", cite("src/components/works/works.css", "line-height: .8; text-transform: uppercase"), "every FKScreamer title and caption overline")}
dump("tokens/00-foundation/typography.json", {"$description": "Font families, sizes (rem on the fluid root: html font-size clamp(7px, .6097560976vw, 10.2777777778px) = 8.78049px at 1440), weights, line heights, letter spacing. Values are the CSS declarations of the clone (which decodes the original's superFont utilities, CLONE_SPEC_A §0.2).",
                                               "version": VERSION, "tokens": {**FONT_FAMILIES, **fs_tokens, **fw_tokens, **lh_tokens, **ls_tokens, **tt_tokens}})

RADII = [("sm", "1.2rem", "src/components/hero/hero.css", "border-radius: 1.2rem", "hero video"), ("md", "1.6rem", "src/components/header/header.css", ".lbsTag {", "tags, images, glass badges"),
         ("lg", "2rem", "src/components/review-cards/reviewCards.css", "border-radius: 2rem", "review logo tile"), ("xl", "2.4rem", IDX, "height: 5.6rem; border-radius: 2.4rem", "buttons, review/label cards, menu widgets"),
         ("2xl", "3.2rem", "src/components/works/works.css", "border-radius: 3.2rem", "work cards, panels, resource cards"), ("pill", "4rem", "src/components/footer/footer.css", ".langSwitcher__option.\\@current", "language switch chip"),
         ("bubble", "48px", "src/components/footer/footer.css", "border-radius: 48px", "tooltip bubble"), ("paper", "2.13%", "src/components/resource-cards/resource-cards.css", "border-radius: 2.13%", "white-paper mockup sheet")]
dump("tokens/00-foundation/radius.json", {"$description": "Border radii (CSS declarations; rendered px at 1440 in measured-values styleHistogram1440.borderRadius).", "version": VERSION,
                                           "tokens": {f"radius.{k}": tok("radius", v, cite(p, n), u) for k, v, p, n, u in RADII}})

SP = [("0", "0"), ("0-8", ".8rem"), ("1-6", "1.6rem"), ("2", "2rem"), ("2-4", "2.4rem"), ("3-2", "3.2rem"), ("4-2", "4.2rem"), ("4-8", "4.8rem"), ("5-6", "5.6rem"), ("6-4", "6.4rem"), ("10-3", "10.3rem"), ("20", "20rem"), ("40", "40rem")]
sp_ev = cite(SA, "`superGrid` → `display:grid", "`@margin[16|25|48]`")
sp_tokens = {f"space.{k}": tok("space", v, sp_ev, "superGrid @gb/@gi/@margin step" if k not in ("20", "40") else None) for k, v in SP}
sp_tokens["space.20"]["evidence"] = [cite("src/components/spotlight/spotlight.css", ".spot { display: flex; margin-bottom: 20rem")]
sp_tokens["space.20"]["usage"] = "gap between bottom-half sections (margin-bottom 20rem)"
sp_tokens["space.40"]["evidence"] = [cite("src/App.jsx", "marginBottom: '40rem'")]
sp_tokens["space.40"]["usage"] = "#MAIN margin-bottom before the footer"
dump("tokens/00-foundation/spacing.json", {"$description": "Spacing steps: the superGrid gap/margin vocabulary (CLONE_SPEC_A §0.2) plus the two section gaps. Arbitrary spacing is rejected in PageSpecs (token-policy).", "version": VERSION, "tokens": sp_tokens})

bp_ev = cite(SA, "Formats: Desktop `min-width:1440px")
dump("tokens/00-foundation/breakpoint.json", {"$description": "Formats. 'whole' (full WebGL + scroll timelines) = NOT mobile; on mobile no scroll timeline or 3D plugin is created.", "version": VERSION, "tokens": {
    "breakpoint.mobile": tok("breakpoint", "(max-width: 767.9px), (max-height: 434.9px)", [bp_ev, cite("src/components/tagline/sectionMotion.js", "const MOBILE_MQ")]),
    "breakpoint.tablet": tok("breakpoint", "(min-width: 768px) and (max-width: 1439.9px)", bp_ev),
    "breakpoint.desktop": tok("breakpoint", "(min-width: 1440px) and (min-height: 435px)", bp_ev),
    "breakpoint.root-font-size": tok("fluidRoot", "clamp(7px, .6097560976vw, 10.2777777778px)", cite(IDX, "font-size: clamp(7px, .6097560976vw, 10.2777777778px)"), "1rem = 8.78049px at 1440, 7px at <= 1148px"),
}})

dump("tokens/00-foundation/elevation.json", {"$description": "Stacking order and glass blur (the site has no box-shadow elevation; depth comes from the WebGL backdrop behind #MAIN and backdrop-filter glass).", "version": VERSION, "tokens": {
    "zIndex.backdrop": tok("zIndex", -1, cite("src/scene/Scene.jsx", "zIndex: -1"), "fixed WebGL canvas behind the page"),
    "zIndex.loader": tok("zIndex", 1, cite("src/components/header/header.css", "#HEADER .loader {")),
    "zIndex.menu": tok("zIndex", 2, cite("src/components/header/header.css", "#HEADER .menu {")),
    "zIndex.footer": tok("zIndex", 5, cite("src/components/footer/footer.css", "#FOOTER {")),
    "zIndex.header": tok("zIndex", 6, cite("src/components/header/header.css", "#HEADER {")),
    "zIndex.modal": tok("zIndex", 6, cite("src/components/hero/hero.css", ".seoModal.\\@stillReadable.\\@show")),
    "glassBlur.sm": tok("glassBlur", "7px", cite(SA, "`superGlass`: `@blur[7|24|90]`")),
    "glassBlur.md": tok("glassBlur", "24px", cite(IDX, "--glassBlur, 24px")),
    "glassBlur.lg": tok("glassBlur", "90px", cite("src/components/LabelCards.jsx", "'--glassBlur': '90px'")),
}})

ICONS = [("s1", "1.6rem"), ("s2", "2rem"), ("s6", "6.4rem"), ("s7", "13.2rem"), ("s8", "20rem")]
dump("tokens/00-foundation/icon-size.json", {"$description": "ui-icon heights (width auto).", "version": VERSION,
                                              "tokens": {f"iconSize.{k}": tok("iconSize", v, cite("src/components/tagline/sectionMotion.css", f".ui-icon.{k} > *")) for k, v in ICONS}})

M = "src/lib/motion.js"
motion_tokens = {
    "easing.custom-out": tok("easing", "cubic path M0,0 C.084,.61 .088,.874 .184,.944 .283,1.016 .374,1 1,1", cite(M, "CustomEase.create('custom::out',"), "load intros, menu, hover sweeps, chars-in"),
    "easing.custom-out-back": tok("easing", "cubic path M0,0 C.08,.7 .1,1.05 .2,1.12 .35,1.08 .5,1 1,1", cite(M, "CustomEase.create('custom::out::back'")),
    "easing.home-custom-out": tok("easing", "cubic path M0,0 C0,1 0,0.903 1,1", cite(M, "CustomEase.create('home::custom::out'")),
    "easing.default": tok("easing", "power1.out", cite(SA, "GSAP default ease is used wherever none is given"), "every scroll tween without an explicit ease"),
    "easing.linear": tok("easing", "none", cite("src/components/tagline/sectionMotion.js", "maskPosition: '0% 0%', ease: 'none'"), "mask reveals, parallax image"),
    "easing.image-pop": tok("easing", "cubic-bezier(.06, .93, .07, .93)", cite("src/components/expertises/expertises.css", "cubic-bezier(.06, .93, .07, .93)")),
    "easing.scroll-badge": tok("easing", "cubic-bezier(.36,.84,.72,.28)", cite("src/components/hero/hero.css", "lbsScrollRotate 2s")),
    "easing.accordion": tok("easing", "ease-out", cite("src/components/faq/faq.css", "max-height .27s ease-out")),
    "duration.hover-color": tok("duration", "0.25s", cite(IDX, "transition: color .25s ease-out")),
    "duration.button-sweep-in": tok("duration", "2.5s", cite("src/components/header/Button.jsx", "duration: 2.5, ease: 'custom::out'")),
    "duration.button-sweep-out": tok("duration", "0.4s", cite("src/components/header/Button.jsx", "duration: 0.4")),
    "duration.cards-pop": tok("duration", "0.7s", cite("src/components/review-cards/reveal.js", "stagger: 0.1, duration: 0.7")),
    "duration.chars-in": tok("duration", "1.7s", cite("src/components/tagline/sectionMotion.js", "stagger: 0.05, duration: 1.7")),
    "duration.load-intro": tok("duration", "7s", cite("src/components/Header.jsx", "x: -7, duration: 7, delay: 0.7")),
    "duration.marquee-loop": tok("duration", "30s", cite("src/components/method/Marquee.jsx", "duration = 30")),
    "duration.menu-close": tok("duration", "0.5s", cite("src/components/header/Menu.jsx", "y: '-100%', scale: 0.95, duration: 0.5")),
    "duration.loader-hide": tok("duration", "1s", cite("src/components/header/Loader.jsx", "duration: fromMenu ? 1.5 : 1")),
    "duration.accordion": tok("duration", "0.27s", cite("src/components/faq/faq.css", "max-height .27s ease-out")),
    "duration.scroll-badge": tok("duration", "2s", cite("src/components/hero/hero.css", "lbsScrollRotate 2s")),
    "stagger.cards": tok("stagger", 0.1, cite("src/components/review-cards/reveal.js", "stagger: 0.1, duration: 0.7")),
    "stagger.words": tok("stagger", 0.07, cite("src/components/review-cards/reveal.js", "scale: 1, stagger: 0.07")),
    "stagger.chars": tok("stagger", 0.05, cite("src/components/tagline/sectionMotion.js", "stagger: 0.05, duration: 1.7")),
    "scroll.smoothing": tok("scrollSmoothing", "lenis lerp 0.1 (defaults), driven by the GSAP ticker", [cite(M, "new Lenis({ autoRaf: false })"), cite(SA, "Lenis 1.3.26 `new Lenis({autoRaf:false})`")]),
}
dump("tokens/00-foundation/motion.json", {"$description": "Motion primitives: eases, durations, staggers, scroll smoothing. Scroll-scrubbed tweens have no duration of their own (scrub: true maps them to scroll distance; see motion-patterns.json).",
                                           "version": VERSION, "tokens": motion_tokens})

STM = "src/components/tagline/sectionMotion.js"
PATTERNS = {
    "pinned-scroll-timeline": ("Sticky track inside a tall section (height N lvh); one scrubbed timeline maps scroll progress to item tweens with overflowStart/overflowEnd = 1 lvh.", cite(STM, "export function sectionTimeline", "return api"), "fit-layout"),
    "webgl-scroll-scene": ("The fixed WebGL backdrop reads the section's scroll progress (background layer wipes, glass triangles, 3D titles, VR sphere).", cite("src/scene/engine.js", "// ---- whole / mobile gating"), "static-gradient"),
    "lines-slide": ("Text split into lines; each line slides 20px on x or y and fades in (scrubbed).", cite(STM, "export function linesSlide"), "final-state"),
    "words-rise": ("Words rise from 130% inside line masks, scale 1.05 -> 1, colour #6630ff -> computed colour.", cite(STM, "export function wordsRise"), "final-state"),
    "words-reveal": ("Stand-alone scrubbed words-rise (start 0% 90%, end 0% 30%, stagger .07).", cite("src/components/review-cards/reveal.js", "export function wordsReveal"), "final-state"),
    "fade": ("autoAlpha 0 -> 1 (or 1 -> 0) on scroll.", cite(STM, "export function fade"), "final-state"),
    "parallax": ("y +n px -> -n px across the scroll range.", cite(STM, "export function parallax"), "final-state"),
    "chars-in": ("Characters slide in from x 100% (stagger .05, 1.7s custom::out) when the trigger enters; reverses on leave-back.", cite(STM, "export function charsIn"), "final-state"),
    "mask-reveal": ("A 200px soft linear-gradient mask sweeps up as the element crosses 90% of the viewport.", cite(STM, "export function maskReveal"), "final-state"),
    "cards-pop": ("Cards y 25% / scale .95 -> 0 / 1, stagger .1, 0.7s, play on enter, reverse on leave-back.", cite("src/components/review-cards/reveal.js", "export function cardsPop"), "final-state"),
    "blur-in": ("filter blur(100px) -> blur(0) on scroll.", cite("src/components/review-cards/reveal.js", "export function blurIn"), "final-state"),
    "marquee-loop": ("Infinite horizontal loop of the credential line, 30s per cycle.", cite("src/components/method/Marquee.jsx", "export default function Marquee"), "static-first-frame"),
    "sticker-curve-path": ("Glass cards travel right-to-left on a cubic Bezier across the pinned range with a small per-card rotation.", cite("src/components/LabelCards.jsx", "// §5.3 Cards: Sticker scroll value"), "fit-layout"),
    "hover-image-pop": ("On hover the label lights up and a photo pops at the viewport edge (CSS transform 2s cubic-bezier).", cite("src/components/expertises/expertises.css", "cubic-bezier(.06, .93, .07, .93)"), "instant-toggle"),
    "cursor-image-follow": ("Case-study card image follows the cursor and the title words swap on hover.", cite("src/components/works/WorkCard.jsx", "duration: 2.5, stagger: 0.045"), "instant-toggle"),
    "draggable-swiper": ("Horizontal track dragged with momentum and edge resistance; prev/next buttons step one card (0.7s power2.out).", cite("src/components/review-cards/useSwiper.js", "duration: 0.7, ease: 'power2.out'"), "native-scroll"),
    "accordion": ("Answer region max-height transition .27s ease-out; several answers may stay open.", cite("src/components/faq/faq.css", "max-height .27s ease-out"), "instant-toggle"),
    "music-string": ("Divider lines bend toward the cursor and spring back (elastic.out(1.5, .3)).", cite("src/components/faq/MusicString.jsx", "elastic.out(1.5, .3)"), "static-first-frame"),
    "cursor-glow": ("A glow follows the cursor inside the footer glass panel.", cite("src/components/footer/useGlower.js", "export function useGlower"), "static-first-frame"),
    "menu-swing-3d": ("Menu panel and widgets swing in on a 3D Bezier path (2-2.9s custom::out); mobile slides down 0.5s.", cite("src/components/header/Menu.jsx", "const swing = "), "instant-toggle"),
    "loader-mask": ("Purple panel with an elliptical three-layer mask lifts on load (1s power2.in) and frames the menu.", cite("src/components/header/Loader.jsx", "export default function Loader"), "instant-toggle"),
    "button-hover-sweep": ("A violet dome sweeps up through the button on hover (2.5s custom::out in, 0.4s out); text turns white.", cite(IDX, ".btn.hover-bottom::before"), "instant-toggle"),
    "load-intro": ("Header logo / CTA and the hero video ease in over 7s custom::out after load.", cite("src/components/Header.jsx", "// Load intro (desktop only)"), "final-state"),
}
FALLBACKS = {
    "fit-layout": "Collapse the pinned section to fit-content height and render every item at its final state with no scrub (the source's own mobile 'is-fit' layout).",
    "static-gradient": "Do not create the WebGL scene; paint the static white-to-grey gradient the source uses on mobile.",
    "final-state": "Render the element at its end state immediately (no transform, full opacity, final colour).",
    "static-first-frame": "Render one static frame of the loop / interaction and never animate it.",
    "instant-toggle": "Switch states instantly (no tween); keep the interaction itself.",
    "native-scroll": "Keep the horizontal track as plain overflow scrolling without momentum or tweened steps.",
}
dump("tokens/00-foundation/motion-patterns.json", {"$description": "Closed vocabulary of motion patterns observed in the source, each with its reduced-motion fallback. The source itself implements NO prefers-reduced-motion handling (grep returns nothing); the fallbacks are design-repo requirements grounded in the source's own mobile/fit behaviour (CLONE_SPEC_A §0.1: on mobile no timeline or 3D plugin is created).",
                                                   "version": VERSION, "reducedMotionFallbacks": FALLBACKS,
                                                   "patterns": {k: {"description": d, "evidence": [e], "reducedMotionFallback": f} for k, (d, e, f) in PATTERNS.items()}})

# semantic / component / layout / theme
sem = {
    "text.primary": tok("alias", "color.drk1", cite(IDX, "color: #120042; font-size: clamp"), "default text on light surfaces"),
    "text.inverse": tok("alias", "color.lgh1", cite("src/components/works/works.css", ".workCard__title { color: #fff"), "text on purple, navy, black surfaces and image cards"),
    "text.muted": tok("alias", "color.gry3", cite("src/components/vr/vr.css", "color: var(--gry3); font-size: 5.2rem"), "VR body copy end colour"),
    "text.accent": tok("alias", "color.prm1", cite("src/components/Works.jsx", "<strong className=\"text-prm1\">"), "emphasised words in titles"),
    "surface.page": tok("alias", "color.lgh1", cite(IDX, "background-color: #fff; -webkit-tap-highlight-color"), "html background"),
    "surface.glass-light": tok("alias", "color.glass.light", cite(IDX, ".glass-lgh")),
    "surface.glass-dark": tok("alias", "color.glass.dark", cite(IDX, ".glass-drk")),
    "type.display-xl": tok("typeRole", {"fontFamily": "font.family.display", "fontSize": "fontSize.display-xl", "fontWeight": "fontWeight.700", "lineHeight": "lineHeight.tightest", "textTransform": "textTransform.display"}, cite("src/components/method/method.css", ".method__marquee-title")),
    "type.display-lg": tok("typeRole", {"fontFamily": "font.family.display", "fontSize": "fontSize.display-lg", "fontWeight": "fontWeight.700", "lineHeight": "lineHeight.tightest", "textTransform": "textTransform.display"}, cite("src/components/footer/footer.css", "font-size: 16.4rem; font-weight: 700; line-height: .75")),
    "type.display-md": tok("typeRole", {"fontFamily": "font.family.display", "fontSize": "fontSize.display-md", "fontWeight": "fontWeight.700", "lineHeight": "lineHeight.tighter", "textTransform": "textTransform.display"}, cite("src/components/works/works.css", ".works .works__title")),
    "type.card-title": tok("typeRole", {"fontFamily": "font.family.display", "fontSize": "fontSize.title-md", "fontWeight": "fontWeight.700", "lineHeight": "lineHeight.snug", "textTransform": "textTransform.display"}, cite("src/components/works/works.css", ".workCard__title")),
    "type.statement": tok("typeRole", {"fontFamily": "font.family.text", "fontSize": "fontSize.statement", "fontWeight": "fontWeight.600", "lineHeight": "lineHeight.statement", "letterSpacing": "letterSpacing.statement"}, cite("src/components/tagline/tagline.css", ".tagline__title")),
    "type.lead": tok("typeRole", {"fontFamily": "font.family.text", "fontSize": "fontSize.lead", "fontWeight": "fontWeight.500", "lineHeight": "lineHeight.lead", "letterSpacing": "letterSpacing.lead"}, cite("src/components/method/method.css", ".method__content")),
    "type.body": tok("typeRole", {"fontFamily": "font.family.text", "fontSize": "fontSize.body-sm", "fontWeight": "fontWeight.500", "lineHeight": "lineHeight.body"}, cite("src/components/tagline/tagline.css", ".tagline__content")),
    "type.caption": tok("typeRole", {"fontFamily": "font.family.text", "fontSize": "fontSize.caption", "fontWeight": "fontWeight.600", "lineHeight": "lineHeight.caption", "textTransform": "textTransform.display"}, cite("src/components/expertises/expertises.css", ".exp .exp__title")),
}
dump("tokens/10-semantic/semantic.json", {"$description": "Semantic roles resolved to foundation token ids (aliases) and composite type roles.", "version": VERSION, "tokens": sem})
BTN = [("light", "#fff", "#120042", None, "d-light"), ("dark", "#120042", "#fff", None, "d-dark"), ("primary", "#6630ff", "#fff", None, "d-primary"),
       ("lightGlass", "color.glass.light", "#fff", "24px", "d-lightGlass"), ("darkGlass", "color.glass.dark", "#120042", "24px", "d-darkGlass")]
REF = {"#fff": "color.lgh1", "#120042": "color.drk1", "#6630ff": "color.prm1"}
comp = {f"button.design.{k}": tok("buttonDesign", {"background": REF.get(bg, bg), "text": REF[fg], **({"backdropBlur": "glassBlur.md"} if blur else {})}, cite(IDX, f".btn.{cls} {{")) for k, bg, fg, blur, cls in BTN}
comp["button.shape.pill"] = tok("buttonShape", {"height": "5.6rem", "radius": "radius.xl", "paddingInline": "space.3-2", "fontSize": "fontSize.body-sm", "fontWeight": "fontWeight.500"}, cite(IDX, ".btn { position: relative"))
comp["button.shape.round"] = tok("buttonShape", {"size": "5.6rem", "radius": "radius.xl"}, cite(IDX, ".btn.round {"))
comp["tag.default"] = tok("tag", {"height": "4rem", "radius": "radius.md", "paddingInline": "space.1-6"}, cite("src/components/works/works.css", ".ui-tag {"))
dump("tokens/20-component/component.json", {"$description": "Component-scoped tokens: the five button designs (UIActionButton), button shapes, tag.", "version": VERSION, "tokens": comp})
lay = {
    "layout.container": tok("container", {"width": "83vw", "maxWidth": "1480px", "paddingInline": "space.3-2", "mobileWidth": "100vw", "mobilePaddingInline": "space.2"}, cite(IDX, ".superDevice { width: 83vw")),
    "layout.grid": tok("grid", {"columns": 12, "gapInline": "space.1-6"}, cite(IDX, ".superGrid { display: grid")),
    "layout.section-gap": tok("alias", "space.20", cite("src/components/resource-cards/resource-cards.css", ".rcs { margin-bottom: 20rem")),
    "layout.main-bottom": tok("alias", "space.40", cite("src/App.jsx", "marginBottom: '40rem'")),
    "layout.pinned-stage.hero": tok("stageHeight", "700lvh", cite(SA, "## 3. Hero `header._header_jx0rq` (y 0 → 6 300)")),
    "layout.pinned-stage.tagline": tok("stageHeight", "500lvh", cite("src/components/Tagline.jsx", "height: whole ? '500lvh'")),
    "layout.pinned-stage.skills": tok("stageHeight", "540lvh", cite("src/components/Skills.jsx", "height: whole ? '540lvh'")),
    "layout.pinned-stage.vr": tok("stageHeight", "600lvh", cite("src/components/Vr.jsx", "height: whole ? '600lvh'")),
    "layout.pinned-stage.labels": tok("stageHeight", "500lvh", cite("src/components/LabelCards.jsx", "const HEIGHT = FRAG_H")),
}
dump("tokens/30-layout/layout.json", {"$description": "Layout tokens: container (superDevice), 12-column grid, section gaps, pinned-stage heights (desktop/tablet 'whole' only).", "version": VERSION, "tokens": lay})

ALL_TOKEN_FILES = ["tokens/00-foundation/color.json", "tokens/00-foundation/typography.json", "tokens/00-foundation/radius.json", "tokens/00-foundation/spacing.json",
                   "tokens/00-foundation/breakpoint.json", "tokens/00-foundation/elevation.json", "tokens/00-foundation/icon-size.json", "tokens/00-foundation/motion.json",
                   "tokens/10-semantic/semantic.json", "tokens/20-component/component.json", "tokens/30-layout/layout.json"]


def load_tokens():
    out = {}
    for f in ALL_TOKEN_FILES:
        for k, v in json.load(open(os.path.join(REPO, f), encoding="utf-8"))["tokens"].items():
            out[k] = (f, v)
    return out


toks = load_tokens()


def resolve(v):
    seen = 0
    while isinstance(v, str) and v in toks and seen < 5:
        v = toks[v][1]["value"]; seen += 1
    return v


theme = {"$description": "The one theme the source renders (white page, navy text). Every semantic token resolved to a literal foundation value; surface tones map to the WebGL backdrop pairs.",
         "version": VERSION, "id": "light",
         "resolved": {k: resolve(v["value"]) for k, (f, v) in toks.items() if f == "tokens/10-semantic/semantic.json" and v["type"] == "alias"},
         "surfaceTones": {k: v["value"] for k, (f, v) in toks.items() if k.startswith("backdrop.")}}
dump("tokens/themes/light.json", theme)

# token catalog (derived; verify_all re-derives and compares)
catalog = {"$description": "Flat, derived catalog of every approved token (generated by extraction/build_repo.py from the token files; extraction/verify_all.py re-derives it and fails on drift). PageSpecs may only reference ids listed here, subject to token-policy.json.",
           "version": VERSION, "sourceFiles": ALL_TOKEN_FILES,
           "tokens": {k: {"category": k.split(".")[0], "type": v["type"], "value": v["value"], "file": f} for k, (f, v) in sorted(toks.items())}}
catalog["counts"] = {"total": len(catalog["tokens"]), "byCategory": {}}
for k, v in catalog["tokens"].items():
    catalog["counts"]["byCategory"][v["category"]] = catalog["counts"]["byCategory"].get(v["category"], 0) + 1
dump("tokens/llm/token-catalog.json", catalog)

SURFACES = ["backdrop.lgh", "backdrop.prm", "backdrop.scd", "backdrop.trt", "backdrop.drk", "backdrop.blk"]
policy = {
    "$description": "What a PageSpec may set, with which tokens. Category names are the catalog's own categories (token-catalog.json counts.byCategory); verify_all checks they resolve.",
    "version": VERSION,
    "pageLevel": {
        "fonts.display": {"allowedCategories": ["font"], "allowed": ["font.family.display", "font.family.text"]},
        "fonts.text": {"allowedCategories": ["font"], "allowed": ["font.family.text"]},
    },
    "nodeSlots": {
        "surfaceTone": {"allowedCategories": ["backdrop"], "allowed": SURFACES, "evidence": [cite(SB, "### 0.2 Background shader layers"), cite(SA, "- Home layers (in this order")]},
        "textTone": {"allowedCategories": ["color"], "allowed": ["color.drk1", "color.lgh1", "color.gry3"]},
        "accentColor": {"allowedCategories": ["color"], "allowed": ["color.prm1", "color.drk1", "color.lgh1"]},
        "blockGap": {"allowedCategories": ["space"], "allowed": ["space.0", "space.0-8", "space.1-6", "space.2-4", "space.3-2", "space.5-6", "space.10-3", "space.20"]},
        "buttonDesign": {"allowedCategories": ["button"], "allowed": [k for k in toks if k.startswith("button.design.")]},
    },
    "themeCombinations": {
        "$description": "surfaceTone -> allowed textTone / accentColor, from the rendered pages (header light/dark logic CLONE_SPEC_A §1.3, title colours per section).",
        "backdrop.lgh": {"textTone": ["color.drk1"], "accentColor": ["color.prm1"], "evidence": [cite("src/components/Works.jsx", "<strong className=\"text-prm1\">")]},
        "backdrop.prm": {"textTone": ["color.lgh1"], "accentColor": ["color.drk1"], "evidence": [cite("src/components/footer/footer.css", ".footer__title strong { color: #120042")]},
        "backdrop.scd": {"textTone": ["color.drk1"], "accentColor": ["color.prm1"], "evidence": [cite(SA, "## 4. Tagline sticker")]},
        "backdrop.trt": {"textTone": ["color.drk1"], "accentColor": ["color.prm1"], "evidence": [cite(SA, "## 7. Skills sticker")]},
        "backdrop.drk": {"textTone": ["color.lgh1"], "accentColor": ["color.prm1"], "evidence": [cite("src/components/LabelCards.jsx", "Engagés pour <strong className=\"text-prm1\">")]},
        "backdrop.blk": {"textTone": ["color.lgh1", "color.gry3"], "accentColor": ["color.prm1"], "evidence": [cite("src/components/vr/vr.css", ".vr__track-title strong { color: var(--prm1)")]},
    },
    "rawValueRestrictions": {
        "color": "Raw hex/rgb/hsl colours are rejected (TOKEN_RAW_COLOR); reference a color.* token.",
        "space": "Raw lengths (px/rem/em/%/vw) are rejected (TOKEN_SPACING_ARBITRARY); reference a space.* token from nodeSlots.blockGap.",
        "font": "Font names that are not a font.family.* token are rejected (TOKEN_FONT_UNSUPPORTED).",
    },
    "licensedTokens": {
        "font.family.display": {"generatedMode": "blocked", "reason": "commercial typeface without a licence file in the source; generated pages use font.family.text for display titles (uppercase, 700) or a typeface the requester licenses outside this repo",
                                 "substitute": "font.family.text"},
    },
    "overrides": "Styling is owned by the section contracts; a PageSpec may only choose among the slot values above (per node) and the two page fonts. There is no free-form style field.",
}
dump("tokens/llm/token-policy.json", policy)
print("tokens:", len(toks))

# ----------------------------------------------------------------------------------- asset roles
def role(av, policy_, desc, evidence, subs=None, kind="media", lic=None, files=None):
    d = {"kind": kind, "availability": av, "generationPolicy": policy_, "description": desc, "evidence": evidence if isinstance(evidence, list) else [evidence]}
    if subs:
        d["generationSafeSubstitutes"] = subs
    if lic:
        d["licensing"] = lic
    if files:
        d["sourceFiles"] = files
    return d


REAL = "Belongs to La boîte à slides or its clients. Never reproduce, trace, restyle or AI-regenerate it in a generated page."
GEN_IMG = ["media.generated-image", "media.placeholder"]
ROLES = {
    # reference-only / blocked (source identity and proprietary media)
    "brand.wordmark": role("blocked-for-generation", "must-not-fabricate", "The source's 'la boite à slides' wordmark SVG (header, footer).", cite(C + "header/icons.jsx", "<title>Logo - la Boite à Slides</title>"), ["brand.placeholder-mark", "brand.user-supplied-mark"], lic=REAL),
    "hero.loop-video": role("reference-only", "must-reuse-exact", "Hero widget showreel video (autoplay, muted loop).", cite(C + "hero/Widgets.jsx", "const VIDEO = '/sk/uploads/home_video_SD"), ["media.generated-video", "media.placeholder"], lic=REAL, files=["public/sk/uploads/home_video_SD_79c96be094.mp4"]),
    "case.photo": role("reference-only", "must-reuse-exact", "Client case-study photographs on the works cards.", cite(C + "Works.jsx", "const WORKS = ["), GEN_IMG, lic=REAL, files=["public/sk/uploads/*Safran*", "public/sk/uploads/*Adidas*", "public/sk/uploads/*Nissan*"]),
    "expertise.photo": role("reference-only", "must-reuse-exact", "Photos popped on hover of the expertise labels.", cite(C + "Expertises.jsx", "const ROUTES = ["), GEN_IMG, lic=REAL),
    "team.photo": role("blocked-for-generation", "must-not-fabricate", "Spotlight photograph (alt 'logo la boite à slides'): agency branding/people.", cite(C + "Spotlight.jsx", "large_Labas_20f4ebe642.jpg"), GEN_IMG, lic=REAL),
    "resource.cover": role("reference-only", "must-reuse-exact", "Resource and menu widget cover photos.", cite(C + "ResourceCards.jsx", "large_presentation_equipe_0eebf6541e.jpeg"), GEN_IMG, lic=REAL),
    "credential.badge": role("blocked-for-generation", "must-not-fabricate", "Certification / rating badges (ISO 9001 Bureau Veritas, Microsoft Office Specialist, 5-star Google reviews).", cite(C + "LabelCards.jsx", "const LABELS = ["), ["credential.placeholder-badge", "rating.placeholder-badge"], lic=REAL + " A generated page must not claim these certifications or ratings."),
    "client.logo": role("blocked-for-generation", "must-not-fabricate", "Logos of the reviewers' companies on the testimonial cards.", cite(C + "review-cards/data.js", "thumbnail_logo_Caterpillar"), ["logo.placeholder-client", "person.fictional-avatar"], lic="Third-party trademarks shown with the source's client relationships; never reuse."),
    "icon.ui": role("reference-only", "must-reuse-exact", "The source's own inline SVG icons (menu points, plus, arrow, triangle mirror, checkmark badge, rotating Scroll badge).", cite(SAA, "## Inline SVGs"), ["icon.generic"]),
    "scene.headset-model": role("reference-only", "must-reuse-exact", "VR headset GLB drawn by the backdrop scene in the VR section.", cite("src/scene/engine.js", "DECIMATE v2_compressed-compressed.glb"), ["media.placeholder"], lic=REAL, files=["public/assets/models/DECIMATE v2_compressed-compressed.glb"]),
    "scene.sphere-thumbnail": role("reference-only", "must-reuse-exact", "61 client-work thumbnails textured on the VR sphere.", cite("src/scene/vr.js", "the 61 `small_*` thumbnails"), GEN_IMG, lic=REAL),
    "scene.hdr-environment": role("reference-only", "must-reuse-exact", "HDR environment map lighting the glass triangles.", cite("src/scene/engine.js", "studio_small_08_1k.hdr"), ["media.placeholder"], lic="Licence of the HDR file is not recorded in the clone; treat as reference-only until confirmed."),
    "scene.title-font-outline": role("blocked-for-generation", "must-not-fabricate", "Typeface JSON outline of the licensed display font used by the 3D hero title.", cite("src/scene/title.js", "FK Screamer Legacy Upright_Regular.json"), ["font.open-licence-outline"], lic="Derived from a commercial typeface; same restriction as font.family.display."),
    # generation-safe
    "brand.placeholder-mark": role("generation-safe", "may-generate-new", "Neutral placeholder mark (initials or geometric shape) for a generated page's brand.", cite(C + "header/icons.jsx", "export function Logo"), kind="media"),
    "brand.user-supplied-mark": role("generation-safe", "must-reuse-exact", "The requester's own logo, supplied by them (never fetched or fabricated).", cite(C + "header/icons.jsx", "export function Logo")),
    "media.generated-image": role("generation-safe", "may-generate-new", "Newly generated or properly licensed image with no real people, client logos or source imagery.", cite(C + "Works.jsx", "const WORKS = [")),
    "media.generated-video": role("generation-safe", "may-generate-new", "Newly produced or licensed short loop video.", cite(C + "hero/Widgets.jsx", "const VIDEO =")),
    "media.placeholder": role("generation-safe", "placeholder-only", "Flat placeholder (solid backdrop-tone fill with an aspect ratio) until real media is supplied.", cite(C + "Works.jsx", "const WORKS = [")),
    "person.fictional-avatar": role("generation-safe", "may-generate-new", "Illustrative avatar for a fictional reviewer; never a photo of a real person.", cite(C + "review-cards/data.js", "export const REVIEWS")),
    "logo.placeholder-client": role("generation-safe", "placeholder-only", "Neutral client-logo placeholder (initials tile).", cite(C + "review-cards/data.js", "export const REVIEWS")),
    "credential.placeholder-badge": role("generation-safe", "placeholder-only", "Neutral badge placeholder for a credential the requester actually holds (stated by them).", cite(C + "LabelCards.jsx", "const LABELS = [")),
    "rating.placeholder-badge": role("generation-safe", "placeholder-only", "Neutral rating badge placeholder; no real platform mark or score.", cite(C + "LabelCards.jsx", "const LABELS = [")),
    "icon.generic": role("generation-safe", "may-generate-new", "Generic UI icon drawn new or taken from an openly licensed set.", cite(SAA, "## Inline SVGs")),
    "social.network-icon": role("generation-safe", "must-reuse-exact", "A social network's own published icon used per its brand guidelines, linking to the requester's profile.", cite(C + "Footer.jsx", "aria-label=\"linkedin\"")),
    "font.open-licence-outline": role("generation-safe", "may-generate-new", "Typeface outline generated from an openly licensed font (e.g. the page's Inter) for the 3D title.", cite("src/scene/title.js", "new FontLoader()")),
    "url.placeholder": role("generation-safe", "placeholder-only", "Links in generated pages: relative paths or reserved .example / .invalid / .test domains only.", cite(C + "Footer.jsx", "const EXPLORE = ["), kind="url"),
    "copy.original": role("generation-safe", "may-generate-new", "Original copy written for the generated page; no source sentence, claim, statistic or testimonial.", cite(C + "Tagline.jsx", "const TITLE ="), kind="copy"),
}
dump("assets/asset-roles.json", {
    "$description": "Closed asset-role vocabulary. availability is pinned in code too (PINNED_AVAILABILITY in schema/semantic_validate.py and extraction/verify_all.py); editing this file alone cannot loosen it. The source is a real, live agency site: logos, people, client photos, certification marks and the display typeface must never appear in a generated page.",
    "version": VERSION,
    "availabilityValues": ["reference-only", "generation-safe", "blocked-for-generation"],
    "generationPolicyValues": ["must-reuse-exact", "may-generate-new", "must-not-fabricate", "placeholder-only"],
    "roles": ROLES})
MEDIA_ROLES = sorted(k for k, v in ROLES.items() if v["kind"] == "media")

# ----------------------------------------------------------------------------------- source identity registry (R2)
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[’'`´]", "'", s)
    return re.sub(r"[^a-z0-9%+/'.:-]+", " ", s).strip()


# ----------------------------------------------------------------------------------- content-schema helpers
def S(maxw, min_len=1):
    return {"type": "string", "minLength": min_len, "maxWords": maxw}


HREF = {"type": "string", "minLength": 1, "maxLength": 200, "pattern": "^(/|#|https?://|mailto:)"}
MEDIA = {"$ref": "#/definitions/media"}


def obj(props, required=None):
    return {"type": "object", "additionalProperties": False, "required": sorted(required if required is not None else props.keys()), "properties": props}


def arr(item, lo, hi):
    return {"type": "array", "minItems": lo, "maxItems": hi, "items": item}


def TITLE(lead, emph):
    return obj({"lead": S(lead), "emphasis": S(emph)})


def LINK(maxw):
    return obj({"label": S(maxw), "href": HREF})


SOCIAL = obj({"network": {"type": "string", "enum": ["linkedin", "vimeo"]}, "href": HREF})
LANGS = arr({"type": "string", "enum": ["fr", "en"]}, 1, 4)


def src(path, needle, end, tag, after="export default function"):
    c = cite(path, needle, end, after=after)
    a, _, rng = c["cite"].rpartition(":")
    return {"file": path, "tag": tag, "lines": rng, "citation": c["cite"]}


def motion(patterns, triggers, fallback, evidence):
    return {"allowedPatterns": patterns, "triggers": triggers, "reducedMotionFallback": fallback,
            "reducedMotionFallbackText": FALLBACKS[fallback], "evidence": evidence}


def resp(desktop, tablet, mobile, evidence):
    return {"desktop": desktop, "tablet": tablet, "mobile": mobile, "evidence": evidence}


TL = C + "tagline/sectionMotion.js"
SECTIONS = {}


def section(id_, title, category, description, source, content, motion_, responsive, *, position="in-flow", stage=False, eligible=True, reason=None,
            constraints=None, surfaces=None, roles=(), gen_roles=(), evidence=(), notes=None, source_id=None):
    d = {"id": id_, "version": VERSION, "title": title, "description": description,
         "source": {"id": source_id, **source}, "semantic": {"id": id_, "category": category},
         "retrievalEligible": eligible}
    if not eligible:
        d["retrievalIneligibleReason"] = reason
    d.update({"positionKind": position, "scrollStage": stage, "variants": ["default"], "content": content,
              "constraints": constraints or {}, "motion": motion_, "responsive": responsive,
              "surfaceTones": surfaces or [], "assetRoles": sorted(roles), "generatedAssetRoles": sorted(gen_roles),
              "evidence": list(evidence)})
    if notes:
        d["generationNotes"] = notes
    SECTIONS[id_] = d


H = C + "Header.jsx"
section("backdrop.webgl-scene", "WebGL backdrop", "BACKDROP",
        "Fixed full-viewport WebGL canvas behind the page: domed gradient background layers that wipe per section, 22 glass triangles, clipped 3D display titles in the hero, VR headset and thumbnail sphere, RGB-shift post pass. Computes the header light/dark state.",
        src("src/scene/Scene.jsx", "return <canvas id=\"SYNTHRA\"", None, "<canvas id=\"SYNTHRA\""),
        obj({"plugins": arr({"type": "string", "enum": ["gradient-layers", "glass-triangles", "title-3d", "vr-sphere", "rgb-shift"]}, 1, 5),
             "mobileFallback": {"type": "string", "enum": ["static-gradient"]}}),
        motion(["webgl-scroll-scene"], ["scroll-scrub", "time"], "static-gradient", [cite(SA, "### 3.4 Scene recipe (three r181)"), cite("src/scene/engine.js", "// ---- whole / mobile gating")]),
        resp("full scene (all plugins)", "full scene (all plugins)", "no scene: static white-to-grey gradient only, no triangles/titles/VR", [cite("src/scene/engine.js", "function applyWhole(w)", "else {")]),
        position="fixed", eligible=False,
        reason="Runtime rendering layer (fixed canvas, pointer-events none) with no content of its own; its look is selected per section through node tokens.surfaceTone, so it is never retrieved as a standalone section.",
        constraints={"onePerPage": True, "mustBeFirst": True}, surfaces=[s for s in SURFACES],
        roles=["scene.headset-model", "scene.sphere-thumbnail", "scene.hdr-environment", "scene.title-font-outline"],
        gen_roles=["media.generated-image", "media.placeholder", "font.open-licence-outline"],
        evidence=[cite("src/scene/Scene.jsx", "const style = { position: 'fixed'"), cite(SB, "### 0.2 Background shader layers")], source_id="Scene.jsx canvas#SYNTHRA",
        notes="Generated pages keep the gradient-layer mechanism with the backdrop.* tones; the VR sphere must be fed generation-safe images and the 3D title must use an open-licence outline.")

section("chrome.loader", "Load curtain", "CHROME",
        "Purple full-screen panel with a three-layer elliptical mask and a two-triangle spinner; lifts once the page has loaded and reappears as the frame behind the open menu.",
        src(C + "header/Loader.jsx", "<div className={`loader", "    </div>", "className={`loader"),
        obj({"spinner": {"type": "string", "enum": ["two-triangles"]}}),
        motion(["loader-mask"], ["load", "menu-toggle"], "instant-toggle", [cite(SA, "## 2. Loader"), cite(C + "header/Loader.jsx", "duration: fromMenu ? 1.5 : 1")]),
        resp("mask lift 1s power2.in", "same", "same", [cite(C + "header/Loader.jsx", "const parked = ")]),
        position="fixed", eligible=False, reason="Preloader / transition curtain: runtime utility UI shown only while loading or behind the menu, it carries no page content.",
        constraints={"onePerPage": True}, surfaces=["backdrop.prm"], evidence=[cite("src/components/header/header.css", "#HEADER .loader {")], source_id="Loader.jsx div.loader")

section("chrome.header", "Fixed header bar", "CHROME",
        "Fixed 12rem bar: wordmark link (left), centred glass 'Menu/Fermer' trigger with clip-path text swap, quote-request CTA (right). Switches light/dark design from the backdrop under it.",
        src(H, "<div className={`header__A1", "      </div>", "header__A1"),
        obj({"brandMark": MEDIA, "menuLabel": S(1), "closeLabel": S(1), "cta": LINK(4)}),
        motion(["load-intro", "button-hover-sweep"], ["load", "hover"], "final-state", [cite(H, "// Load intro (desktop only)"), cite(SA, "### 1.3 Header color logic")]),
        resp("logo / menu trigger / CTA in one row", "same", "CTA hidden; logo + trigger only", [cite("src/components/header/header.css", ".header__A1.\\@mobile .header__cta { display: none")]),
        position="fixed", constraints={"onePerPage": True}, surfaces=["backdrop.lgh", "backdrop.prm", "backdrop.drk", "backdrop.blk"],
        roles=["brand.wordmark", "icon.ui"], gen_roles=["brand.placeholder-mark", "brand.user-supplied-mark", "icon.generic"],
        evidence=[cite(SA, "## 1. Fixed `#HEADER`")], source_id="Header.jsx header#HEADER > .header__A1")

section("chrome.menu-overlay", "Menu overlay", "CHROME",
        "White rounded panel opened from the header trigger with a 3D swing: explore links, expertise links, FR/EN switch, office cities, socials and three promo widgets (expertise, white paper, client case).",
        src(C + "header/Menu.jsx", "<section className={cls} ref={ref}>", "    </section>", "<section className={cls}"),
        obj({"languages": LANGS,
             "widgets": arr(obj({"kind": {"type": "string", "enum": ["expertise", "whitePaper", "clientCase"]}, "tag": S(3), "title": S(10), "ctaLabel": S(2), "href": HREF, "media": MEDIA}, ["kind", "title", "href"]), 0, 3),
             "explore": obj({"title": S(2), "links": arr(LINK(4), 1, 8)}), "expertises": obj({"title": S(2), "links": arr(LINK(4), 1, 10)}),
             "address": S(12), "socials": arr(SOCIAL, 0, 4)}, ["languages", "explore", "expertises"]),
        motion(["menu-swing-3d", "button-hover-sweep"], ["click"], "instant-toggle", [cite(C + "header/Menu.jsx", "A.W = gsap.timeline"), cite(SA, "### 1.5 Menu overlay")]),
        resp("3-column grid: widgets | explore | expertises, 3D swing", "same (crushed variant keeps columns)", "single column, slides down 0.5s, scrollable", [cite("src/components/header/header.css", "#HEADER .menu.\\@mobile:not(.\\@crushed) .menu__expertises, #HEADER"), cite(C + "header/Menu.jsx", "A.U = gsap.fromTo(menu")]),
        position="fixed", eligible=False, reason="Navigation overlay (dialog-like layer toggled by the header trigger); it duplicates site navigation and is not page content.",
        constraints={"onePerPage": True}, surfaces=["backdrop.lgh"], roles=["resource.cover", "icon.ui"], gen_roles=["media.generated-image", "media.placeholder", "social.network-icon", "icon.generic"],
        evidence=[cite(C + "header/Menu.jsx", "const EXPLORE = [")], source_id="Menu.jsx section.menu")

section("hero.statement", "Hero statement (scroll-scrubbed opener)", "HERO",
        "Page opener: two-part display title drawn in 3D by the backdrop (visually-hidden DOM copy), a fixed Inter statement that slides in line by line mid-scroll, and the bottom-left showreel video widget with a rotating Scroll badge. 700lvh scroll-scrubbed stage.",
        src(C + "Hero.jsx", "data-section=\"hero\"", "      </header>", "data-section=\"hero\""),
        obj({"titleLines": arr(TITLE(5, 2), 2, 2), "subtitle": S(30), "video": MEDIA, "scrollBadge": {"type": "boolean"}}),
        motion(["pinned-scroll-timeline", "webgl-scroll-scene", "lines-slide", "fade", "load-intro"], ["scroll-scrub", "load"], "fit-layout",
               [cite(C + "Hero.jsx", "st.add(split.lines", "st.add(h1"), cite(SA, "### 3.3 Hero timeline")]),
        resp("700lvh stage, fixed subtitle, 3D title", "700lvh stage (lvh = viewport height)", "fit-content: title and subtitle as plain stacked text (subtitle 4rem), video widget inline, no scrub",
             [cite("src/components/hero/hero.css", ".heroHeader:not(.\\@whole) .hero__subtitle { font-size: 4rem"), cite(C + "Hero.jsx", "className={`heroHeader")]),
        stage=True, constraints={"onePerPage": True, "mustBeFirstInFlow": True}, surfaces=["backdrop.prm", "backdrop.lgh"],
        roles=["hero.loop-video", "icon.ui"], gen_roles=["media.generated-video", "media.placeholder", "icon.generic"],
        evidence=[cite(SA, "## 3. Hero `header._header_jx0rq` (y 0 → 6 300)"), cite(SA, "### 3.6 Scroll story")], source_id="Hero.jsx header.heroHeader",
        notes="Measured 6300px at 1440x900 (700lvh); above the 3000px HERO cap, so it is a whitelisted exception; its approval status and owner decision are in extraction/measured-values.json (wrapperGate.whitelist).")

section("chrome.seo-modal", "SEO modal", "CHROME",
        "Hidden 'still readable' dialog holding the long-form SEO text (h2 title + h3-bounded parts), toggled from the footer info button.",
        src(C + "hero/SeoModal.jsx", "className={`seoModal modal", "    </div>", "seoModal modal"),
        obj({"title": S(16), "parts": arr(obj({"heading": S(16), "paragraphs": arr(S(120), 0, 6), "listItems": arr(S(70), 0, 12)}, ["heading", "paragraphs"]), 1, 16)}),
        motion([], ["click"], "instant-toggle", [cite(SA, "## 8. SEO modal")]),
        resp("8 of 12 columns centred", "same", "full width, max 93rem", [cite("src/components/hero/hero.css", ".seoModal .seoModal__content { grid-column: 1/13")]),
        position="fixed", eligible=False, reason="Modal dialog hidden by default (z-index -3 until opened); its prose is SEO filler, not part of the visible page composition.",
        constraints={"onePerPage": True}, evidence=[cite(C + "hero/seoContent.js", "export default")], source_id="SeoModal.jsx div.seoModal",
        notes="Decomposed by its own heading boundaries (title + parts[heading, paragraphs, listItems]); never one opaque body.")

section("story.tagline", "Positioning statement", "STORY",
        "500lvh pinned block: large Inter statement slides in line by line on the left, a short paragraph bottom-right, over the green backdrop and the triangle 'fence'.",
        src(C + "Tagline.jsx", "data-section=\"tagline\"", "    </section>", "data-section=\"tagline\""),
        obj({"statement": S(32), "body": S(42)}),
        motion(["pinned-scroll-timeline", "webgl-scroll-scene", "lines-slide", "parallax", "fade"], ["scroll-scrub"], "fit-layout", [cite(C + "Tagline.jsx", "linesSlide(tl, title.current", "fade(tl"), cite(SA, "### 4.2 Timeline (`TAGLINE`)")]),
        resp("500lvh sticker, statement cols 1-8, body bottom-right", "same", "fit-content, title 4rem then body, grid gap 10.3rem", [cite(C + "Tagline.jsx", "style={{ height: whole ? '500lvh'"), cite("src/components/tagline/tagline.css", ".tagline:not(.is-whole) .tagline__title")]),
        stage=True, surfaces=["backdrop.scd", "backdrop.lgh"], evidence=[cite(SA, "## 4. Tagline sticker")], source_id="Tagline.jsx section.tagline")

section("proof.works", "Case-study grid", "PROOF",
        "Display title over a 2-column grid of 8 case-study cards (client, category tag, photo) with staggered pop-in and cursor-following hover image.",
        src(C + "Works.jsx", "data-section=\"works\"", "    </section>", "data-section=\"works\""),
        obj({"title": TITLE(6, 3), "cards": arr(obj({"client": S(4), "tag": S(3), "href": HREF, "media": MEDIA}), 2, 8)}),
        motion(["words-rise", "cards-pop", "cursor-image-follow", "webgl-scroll-scene"], ["scroll-scrub", "scroll-toggle", "hover"], "final-state", [cite(C + "Works.jsx", "wordsRise(tl, title.current"), cite(SA, "### 5.2 Motion")]),
        resp("2 columns, gap .8rem", "2 columns", "1 column, no hover physics", [cite(C + "Works.jsx", "'--gridColumns': whole ? 2 : 1")]),
        surfaces=["backdrop.lgh"], roles=["case.photo"], gen_roles=["media.generated-image", "media.placeholder"],
        evidence=[cite(SA, "## 5. Works")], source_id="Works.jsx section.works")

section("proof.method", "Credentials marquee and method", "PROOF",
        "30s looping marquee of credentials with a triangle icon, then an Inter tagline and a lead paragraph with a checkmarked metrics list revealed by a scroll mask.",
        src(C + "Method.jsx", "data-section=\"method\"", "    </section>", "data-section=\"method\""),
        obj({"marquee": arr(S(5), 3, 8), "tagline": S(22), "body": S(40), "metrics": arr(S(9), 2, 6)}),
        motion(["marquee-loop", "chars-in", "parallax", "lines-slide", "mask-reveal"], ["time", "scroll-scrub", "scroll-toggle"], "static-first-frame", [cite(C + "Method.jsx", "for (const t of titles.current)", "maskReveal(metrics.current"), cite(SA, "### 6.2 Motion")]),
        resp("marquee 25.2rem, tagline 5.2rem, body + metrics in a second column", "same", "marquee 16.4rem, tagline 4rem, single column max 93rem", [cite("src/components/method/method.css", ".method:not(.is-whole) .method__marquee-title"), cite("src/components/method/method.css", ".method:not(.is-whole) .method__tagline, .method")]),
        surfaces=["backdrop.lgh"], roles=["icon.ui"], gen_roles=["icon.generic"], evidence=[cite(SA, "## 6. Method")], source_id="Method.jsx section.method")

section("offer.skills", "Commitments stage", "OFFER",
        "540lvh pinned block of three stacked commitment statements that slide in and fade out in turn, with glass credential badges and a final portfolio CTA, over the cyan backdrop and triangle pinwheel.",
        src(C + "Skills.jsx", "data-section=\"skills\"", "    </div>", "data-section=\"skills\""),
        obj({"items": arr(obj({"statement": S(32), "badges": arr(MEDIA, 0, 3), "cta": LINK(4)}, ["statement", "badges"]), 2, 4)}),
        motion(["pinned-scroll-timeline", "webgl-scroll-scene", "lines-slide", "fade", "button-hover-sweep"], ["scroll-scrub", "hover"], "fit-layout", [cite(C + "Skills.jsx", "const tl = sectionTimeline(root.current", "tl.sync()"), cite(SA, "### 7.2 Motion — timeline `SKILLS`")]),
        resp("540lvh sticker, statements in the right half", "same", "fit-content list, statements 4rem at 80% width", [cite(C + "Skills.jsx", "style={{ height: whole ? '540lvh'"), cite("src/components/skills/skills.css", ".skills:not(.is-whole) .skills__track-skill .skill__title")]),
        stage=True, surfaces=["backdrop.trt", "backdrop.lgh"], roles=["credential.badge", "icon.ui"], gen_roles=["credential.placeholder-badge", "rating.placeholder-badge", "icon.generic"],
        evidence=[cite(SA, "## 7. Skills sticker")], source_id="Skills.jsx div.skills")

section("offer.expertises", "Service index", "OFFER",
        "Caption overline and a centred list of giant display labels (one per service) at low opacity that light up and pop a photo at the viewport edge on hover.",
        src(C + "Expertises.jsx", "data-section=\"expertises\"", "    </section>", "data-section=\"expertises\""),
        obj({"title": S(3), "routes": arr(obj({"label": S(4), "href": HREF, "media": MEDIA}), 3, 8)}),
        motion(["parallax", "hover-image-pop"], ["scroll-scrub", "hover"], "instant-toggle", [cite(C + "Expertises.jsx", "// §1.4 — labels rise 17lvh"), cite(SB, "### 1.4 Scroll motion")]),
        resp("labels 16.4rem", "labels 16.4rem", "labels 9.6rem, no hover photo", [cite("src/components/expertises/expertises.css", ".exp .exp__router { display: flex"), cite("src/components/expertises/expertises.css", ".exp.is-whole .exp__router")]),
        surfaces=["backdrop.lgh"], roles=["expertise.photo"], gen_roles=["media.generated-image", "media.placeholder"], evidence=[cite(SB, "## 1. Expertises")], source_id="Expertises.jsx section.exp")

section("story.vr", "Immersive showcase stage", "STORY",
        "600lvh pinned stage: display title rises then clears, a VR headset flies through the camera, the backdrop cuts to black and a sphere of project thumbnails surrounds the camera while a short statement and CTA fade in; ends with a curved white wipe.",
        src(C + "Vr.jsx", "data-section=\"vr\"", "    </section>", "data-section=\"vr\""),
        obj({"title": TITLE(4, 4), "body": S(20), "cta": LINK(3)}),
        motion(["pinned-scroll-timeline", "webgl-scroll-scene", "words-rise", "fade", "parallax", "button-hover-sweep"], ["scroll-scrub", "hover"], "fit-layout", [cite(C + "Vr.jsx", "wordsRise(tl, title", "fade(tl, a1"), cite(SB, "### 2.3 Timeline")]),
        resp("600lvh stage, body 5.2rem grey on black", "same", "fit-content, body 4rem white centred, no 3D", [cite(C + "Vr.jsx", "style={{ height: whole ? '600lvh'"), cite("src/components/vr/vr.css", ".vr.is-fit .vr__track-content")]),
        stage=True, surfaces=["backdrop.blk", "backdrop.lgh"], roles=["scene.headset-model", "scene.sphere-thumbnail"], gen_roles=["media.generated-image", "media.placeholder"],
        evidence=[cite(SB, "## 2. VR sticker")], source_id="Vr.jsx section.vr")

section("offer.spotlight", "Team statement with image", "OFFER",
        "Triangle icon, display title with an emphasised second half, a short paragraph and a CTA on the left; a photo parallaxing +300 -> -300px on the right.",
        src(C + "Spotlight.jsx", "data-section=\"spotlight\"", "    </section>", "data-section=\"spotlight\""),
        obj({"title": TITLE(3, 3), "body": S(36), "cta": LINK(3), "media": MEDIA}),
        motion(["words-rise", "blur-in", "lines-slide", "fade", "parallax", "button-hover-sweep"], ["scroll-scrub", "hover"], "final-state", [cite(C + "Spotlight.jsx", "wordsRise(standalone, title.current", "parallax(standalone, image.current"), cite(SB, "### 3.3 Motion")]),
        resp("two columns: text | image", "same", "column: text above image", [cite(C + "Spotlight.jsx", "className={`spot ${whole ? '' : 'is-column'}`}")]),
        surfaces=["backdrop.lgh"], roles=["team.photo", "icon.ui"], gen_roles=["media.generated-image", "media.placeholder", "icon.generic"], evidence=[cite(SB, "## 3. Spotlight")], source_id="Spotlight.jsx section.spot")

section("content.resources", "Latest resources", "CONTENT",
        "Display title with an 'all resources' CTA, then a row of three resource cards (article on navy, client case over a photo, white paper as a rotated sheet mockup) that pop in once.",
        src(C + "ResourceCards.jsx", "data-section=\"resource-cards\"", "    </section>", "data-section=\"resource-cards\""),
        obj({"title": TITLE(3, 2), "cta": LINK(5), "cards": arr(obj({"kind": {"type": "string", "enum": ["article", "clientCase", "whitePaper"]}, "tag": S(3),
                                                                      "publishedAt": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"}, "title": S(12), "href": HREF, "media": MEDIA}, ["kind", "tag", "publishedAt", "title", "href"]), 1, 3)}),
        motion(["words-rise", "fade", "cards-pop", "button-hover-sweep"], ["scroll-scrub", "scroll-toggle", "hover"], "final-state", [cite(C + "ResourceCards.jsx", "wordsRise(standalone, title.current", "toggleActions"), cite(SB, "### 4.3 Motion")]),
        resp("3 columns, gap 1.6rem, card titles 6.4rem", "3 columns", "2 columns, gap .8rem, card titles 4rem", [cite(C + "ResourceCards.jsx", "'--gridColumns': whole ? 3 : 2")]),
        surfaces=["backdrop.lgh"], roles=["resource.cover"], gen_roles=["media.generated-image", "media.placeholder"], evidence=[cite(SB, "## 4. Resource cards")], source_id="ResourceCards.jsx section.rcs")

section("proof.labels", "Quality credentials stage", "PROOF",
        "500lvh pinned block over the navy backdrop: a giant two-tone title and three glass credential cards (title, badge image, year tag) travelling right-to-left on a curved path.",
        src(C + "LabelCards.jsx", "data-section=\"label-cards\"", "    </section>", "data-section=\"label-cards\""),
        obj({"title": TITLE(3, 3), "cards": arr(obj({"title": S(6), "tag": S(3), "media": MEDIA, "isPlaceholder": {"type": "boolean"}}), 2, 4)}),
        motion(["pinned-scroll-timeline", "sticker-curve-path", "parallax", "lines-slide", "webgl-scroll-scene"], ["scroll-scrub"], "fit-layout", [cite(C + "LabelCards.jsx", "// §5.3 Title: PARALLAX_Y 50"), cite(SB, "### 5.3 Motion")]),
        resp("500lvh sticker, title 25.2rem, cards on a Bezier path", "same", "fit-content 2-column grid of cards, title 11.2rem", [cite(C + "LabelCards.jsx", "className={whole ? 'lcs__list' : 'lcs__list superGrid'}"), cite("src/components/label-cards/label-cards.css", ".lcs.is-whole .lcs__title")]),
        stage=True, surfaces=["backdrop.drk", "backdrop.lgh"], roles=["credential.badge"], gen_roles=["credential.placeholder-badge", "rating.placeholder-badge"],
        evidence=[cite(SB, "## 5. Label cards sticker")], source_id="LabelCards.jsx section.lcs",
        notes="In generated mode every card is a placeholder (isPlaceholder: true) unless the requester supplies their own real credential.")

section("proof.reviews", "Testimonials slider", "PROOF",
        "Display title with prev/next round buttons and a draggable glass-card slider of client testimonials (logo, name, role, quote).",
        src(C + "ReviewCards.jsx", "data-section=\"review-cards\"", "    </section>", "data-section=\"review-cards\""),
        obj({"title": TITLE(3, 2), "reviews": arr(obj({"person": obj({"name": S(3), "role": S(8), "isFictional": {"type": "boolean"}}), "quote": S(110), "media": MEDIA}), 3, 12)}),
        motion(["words-reveal", "cards-pop", "draggable-swiper", "button-hover-sweep"], ["scroll-scrub", "scroll-toggle", "drag", "click"], "native-scroll", [cite(C + "ReviewCards.jsx", "wordsReveal(title.current"), cite(SB, "### 6.3 Behaviour")]),
        resp("track bleeds to the right edge, buttons beside the title", "same", "inside the container, no reveal motion", [cite(C + "ReviewCards.jsx", "className={`reviewCards home__reviewCards ${whole ? '' : 'superDevice'}`}")]),
        surfaces=["backdrop.lgh"], roles=["client.logo"], gen_roles=["person.fictional-avatar", "logo.placeholder-client"], evidence=[cite(SB, "## 6. Review cards")], source_id="ReviewCards.jsx section.reviewCards")

section("content.faq", "FAQ accordion", "CONTENT",
        "Overline, centred two-tone display title, an accordion of questions (6 shown, +6 per 'more' click; several may be open) with cursor-bending string dividers.",
        src(C + "Faq.jsx", "data-section=\"faq\"", "    </div>", "data-section=\"faq\""),
        obj({"overline": S(1), "title": TITLE(2, 3), "items": arr(obj({"question": S(14), "answer": S(110)}), 1, 24), "pageSize": {"type": "integer", "enum": [6]}, "moreLabel": S(5)}),
        motion(["blur-in", "words-reveal", "mask-reveal", "fade", "accordion", "music-string", "button-hover-sweep"], ["scroll-scrub", "click", "hover"], "instant-toggle", [cite(C + "Faq.jsx", "blurIn(ontitle.current", "fadeIn(sec"), cite(SB, "### 7.4 Scroll motion")]),
        resp("centred column in the 12-col grid", "same", "full width, max 93rem, no string bending", [cite("src/components/faq/faq.css", "[data-section=\"faq\"] .faq { grid-column: 1 / 13")]),
        surfaces=["backdrop.lgh"], evidence=[cite(SB, "## 7. FAQ")], source_id="Faq.jsx section.faq")

FT = C + "Footer.jsx"
section("conversion.closing-cta", "Closing call to action", "CONVERSION",
        "Opening band of the footer: a giant two-tone display question and a contact CTA on the rising purple backdrop.",
        src(FT, "<div ref={title} className=\"footer__title", "<ActionCTA design=\"light\"", "footer__title"),
        obj({"title": TITLE(4, 2), "cta": LINK(3)}),
        motion(["words-reveal", "fade", "button-hover-sweep"], ["scroll-scrub", "hover"], "final-state", [cite(FT, "wordsReveal(title.current, { trigger: root.current"), cite(SB, "### 8.4 Motion")]),
        resp("title 16.4rem", "same", "title 11.2rem, max 93rem", [cite("src/components/footer/footer.css", "#FOOTER .footer__title { font-size: 11.2rem")]),
        constraints={"onePerPage": True, "mustPrecede": "chrome.footer"}, surfaces=["backdrop.prm"],
        evidence=[cite(SB, "## 8. Footer")], source_id="Footer.jsx footer#FOOTER > .footer__title + .footer__cta",
        notes="Split from footer#FOOTER on purpose: it is a conversion block (R6 category honesty), while the panel below is site chrome.")

section("chrome.footer", "Footer panel", "CHROME",
        "Glass panel inside footer#FOOTER with a cursor glow: wordmark, FR/EN switch, office cities, three nav groups, credential icons with tooltips, copyright + SEO-modal trigger, socials and legal links.",
        src(FT, "className=\"footer__A1 superGrid\"", "    </footer>", "footer__A1"),
        obj({"brandMark": MEDIA, "languages": LANGS, "address": S(12),
             "navGroups": arr(obj({"title": S(2), "links": arr(obj({"strong": S(1), "label": S(4), "href": HREF}, ["label", "href"]), 1, 10)}), 1, 4),
             "credentials": arr(obj({"title": S(6), "media": MEDIA, "isPlaceholder": {"type": "boolean"}}), 0, 4),
             "legalLinks": arr(LINK(4), 0, 4), "socials": arr(SOCIAL, 0, 4), "showCopyrightYear": {"type": "boolean"}, "seoModalTrigger": {"type": "boolean"}},
            ["brandMark", "languages", "navGroups", "legalLinks"]),
        motion(["cursor-glow"], ["hover"], "static-first-frame", [cite(FT, "useGlower(panel, whole)"), cite(SB, "### 8.3 Hover")]),
        resp("12-col glass panel, margin 4.8rem", "same", "stacked groups, expertise links 2rem", [cite("src/components/footer/footer.css", "#FOOTER .footerNav__route--expertise { font-size: 2rem")]),
        constraints={"onePerPage": True, "mustBeLast": True}, surfaces=["backdrop.prm"],
        roles=["brand.wordmark", "credential.badge", "icon.ui"], gen_roles=["brand.placeholder-mark", "brand.user-supplied-mark", "credential.placeholder-badge", "rating.placeholder-badge", "social.network-icon", "icon.generic"],
        evidence=[cite(SB, "### 8.1 DOM")], source_id="Footer.jsx footer#FOOTER > .footer__A1")

for k, v in SECTIONS.items():
    dump(f"sections/{k}.json", v)
print("sections:", len(SECTIONS))

# ----------------------------------------------------------------------------------- primitives / components
def part(kind, id_, desc, props, tokens_, evidence, used_by):
    return {"id": id_, "kind": kind, "version": VERSION, "description": desc, "props": props, "tokens": tokens_, "evidence": evidence, "usedBySections": sorted(used_by)}


PRIMS = [
    part("primitive", "primitive.button", "UIActionButton: pill or round, five designs, optional violet hover sweep.", {"design": ["light", "dark", "primary", "lightGlass", "darkGlass"], "round": "boolean", "hover": ["bottom", "left", "right", "none"], "label": "string"},
         ["button.shape.pill", "button.shape.round"] + [f"button.design.{d}" for d in ["light", "dark", "primary", "lightGlass", "darkGlass"]], [cite(C + "header/Button.jsx", "const DESIGN = {"), cite(IDX, ".btn { position: relative")], ["chrome.header", "proof.reviews", "chrome.seo-modal"]),
    part("primitive", "primitive.action-cta", "UIActionCTA: round arrow button + pill label that sweep together on hover.", {"design": ["light", "darkGlass", "lightGlass"], "label": "string", "href": "string"},
         ["button.design.light", "button.design.darkGlass", "button.design.lightGlass"], [cite(C + "header/ActionCTA.jsx", "export default function ActionCTA")], ["offer.skills", "story.vr", "offer.spotlight", "content.resources", "content.faq", "conversion.closing-cta", "chrome.menu-overlay"]),
    part("primitive", "primitive.tag", "Outlined pill tag (category / year / resource kind).", {"label": "string", "tone": ["lgh1", "drk1"]}, ["tag.default", "radius.md"], [cite("src/components/header/header.css", ".lbsTag {"), cite("src/components/works/works.css", ".ui-tag {")], ["proof.works", "content.resources", "proof.labels", "chrome.menu-overlay"]),
    part("primitive", "primitive.icon", "ui-icon box: inline SVG at a fixed height step.", {"size": ["s1", "s2", "s6", "s7", "s8"], "assetRole": ["icon.ui", "icon.generic"]}, [k for k in toks if k.startswith("iconSize.")], [cite("src/components/tagline/sectionMotion.css", ".ui-icon { display: flex")], ["proof.method", "offer.skills", "offer.spotlight"]),
    part("primitive", "primitive.glass-surface", "superGlass: backdrop-filter blur with a light or dark tint.", {"tint": ["light", "dark"], "blur": ["sm", "md", "lg"]}, ["color.glass.light", "color.glass.dark", "glassBlur.sm", "glassBlur.md", "glassBlur.lg"], [cite(IDX, ".superGlass { backdrop-filter")], ["offer.skills", "proof.labels", "proof.reviews", "chrome.footer"]),
    part("primitive", "primitive.emphasis-title", "Display title whose trailing words are wrapped in <strong> and coloured with the accent.", {"lead": "string", "emphasis": "string"}, ["type.display-md", "text.accent"], [cite(C + "Works.jsx", "Un seul outil, des <strong")], ["proof.works", "story.vr", "offer.spotlight", "content.resources", "proof.labels", "proof.reviews", "content.faq", "conversion.closing-cta"]),
    part("primitive", "primitive.media", "Image or video reference bound to a closed asset role.", {"assetRole": "closed enum (assets/asset-roles.json)", "src": "string", "alt": "string"}, ["radius.md"], [cite(C + "resource-cards/useAutoSizes.js", "export const srcSet")], ["proof.works", "offer.expertises", "offer.spotlight", "content.resources", "proof.labels", "proof.reviews", "hero.statement"]),
    part("primitive", "primitive.lang-switcher", "FR / EN option chips.", {"languages": ["fr", "en"]}, ["radius.pill", "fontSize.micro"], [cite(FT, "<ul className=\"langSwitcher\">")], ["chrome.menu-overlay", "chrome.footer"]),
    part("primitive", "primitive.tooltip", "Hover/focus bubble above an icon (glass title + arrow).", {"title": "string"}, ["radius.bubble", "glassBlur.md"], [cite(FT, "className=\"tooltip__bubble\" role=\"tooltip\"")], ["chrome.footer"]),
]
COMPS = [
    part("component", "component.work-card", "Case-study card: photo, client title, category tag; hover image follows the cursor.", {"client": "string", "tag": "string", "href": "string", "media": "primitive.media"}, ["radius.2xl", "type.card-title"], [cite(C + "works/WorkCard.jsx", "export default function WorkCard")], ["proof.works"]),
    part("component", "component.resource-card", "Resource card in three kinds: article (navy), client case (photo), white paper (sheet mockup).", {"kind": ["article", "clientCase", "whitePaper"], "tag": "primitive.tag", "publishedAt": "date", "title": "string"}, ["radius.2xl", "fontSize.title-xl"], [cite(C + "ResourceCards.jsx", "className=\"rc is-article bg-drk\"")], ["content.resources"]),
    part("component", "component.white-paper-mockup", "Rotated cover sheet + white back sheet + drop shadow.", {"title": "string"}, ["radius.paper"], [cite(C + "resource-cards/WhitePaper.jsx", "export default function WhitePaper")], ["content.resources", "chrome.menu-overlay"]),
    part("component", "component.label-card", "Glass credential card: title, badge image, year tag.", {"title": "string", "tag": "primitive.tag", "media": "primitive.media"}, ["glassBlur.lg", "radius.xl"], [cite(C + "LabelCards.jsx", "<section className=\"lc superGlass glass-lgh\"")], ["proof.labels"]),
    part("component", "component.review-card", "Glass testimonial card: logo, name, role, quote.", {"person": "object", "quote": "string", "media": "primitive.media"}, ["glassBlur.md", "radius.xl", "fontSize.body-lg"], [cite(C + "ReviewCards.jsx", "function ReviewCard")], ["proof.reviews"]),
    part("component", "component.faq-dropdown", "Question button + collapsible answer + bending string divider.", {"question": "string", "answer": "string"}, ["font.family.system-arial", "duration.accordion"], [cite(C + "faq/Dropdown.jsx", "export default")], ["content.faq"]),
    part("component", "component.credential-marquee", "Looping display line of credentials separated by bullets, with a triangle icon.", {"items": "string[]"}, ["type.display-xl", "duration.marquee-loop"], [cite(C + "method/Marquee.jsx", "export default function Marquee")], ["proof.method"]),
    part("component", "component.metric-list", "Checkmarked list of short proof points.", {"items": "string[]"}, ["fontSize.body-sm", "iconSize.s2"], [cite(C + "Method.jsx", "className=\"method__metrics ff-inter\"")], ["proof.method"]),
    part("component", "component.skill-item", "Statement + glass badges + optional CTA, one per pinned fragment.", {"statement": "string", "badges": "primitive.media[]", "cta": "primitive.action-cta"}, ["type.statement"], [cite(C + "Skills.jsx", "className=\"skills__track-skill\"")], ["offer.skills"]),
    part("component", "component.expertise-route", "Giant display label link with a hover photo.", {"label": "string", "href": "string", "media": "primitive.media"}, ["fontSize.display-lg", "easing.image-pop"], [cite(C + "Expertises.jsx", "className=\"exp__route\"")], ["offer.expertises"]),
    part("component", "component.video-widget", "Hero video card with a fullscreen toggle and rotating Scroll badge.", {"media": "primitive.media", "scrollBadge": "boolean"}, ["radius.sm", "duration.scroll-badge"], [cite(C + "hero/Widgets.jsx", "const Widgets = forwardRef")], ["hero.statement"]),
    part("component", "component.nav-group", "Titled list of links (menu / footer).", {"title": "string", "links": "link[]"}, ["fontSize.caption", "fontSize.lead"], [cite(FT, "function Nav(")], ["chrome.menu-overlay", "chrome.footer"]),
    part("component", "component.menu-widget", "Promo tile in the menu (expertise / white paper / client case).", {"kind": ["expertise", "whitePaper", "clientCase"], "title": "string", "tag": "string"}, ["radius.xl", "radius.2xl"], [cite(C + "header/Menu.jsx", "<ul className=\"menu__widgets superGrid\">")], ["chrome.menu-overlay"]),
]
for p_ in PRIMS:
    dump(f"primitives/{p_['id'].split('.', 1)[1]}.json", p_)
for c_ in COMPS:
    dump(f"components/{c_['id'].split('.', 1)[1]}.json", c_)

# ----------------------------------------------------------------------------------- templates
ORDER = ["backdrop.webgl-scene", "chrome.loader", "chrome.header", "chrome.menu-overlay", "hero.statement", "chrome.seo-modal", "story.tagline", "proof.works", "proof.method",
         "offer.skills", "offer.expertises", "story.vr", "offer.spotlight", "content.resources", "proof.labels", "proof.reviews", "content.faq", "conversion.closing-cta", "chrome.footer"]
REQUIRED = {"backdrop.webgl-scene", "chrome.loader", "chrome.header", "chrome.menu-overlay", "hero.statement", "conversion.closing-cta", "chrome.footer"}
assert set(ORDER) == set(SECTIONS)
templates = {
    "$description": "One template per page shape. The clone serves exactly one route ('/'); every other href in the source (expertises, réalisations, ressources, contact, legal, ...) points at the original site's routes and is NOT built here, so no template is invented for them.",
    "version": VERSION,
    "templates": {"template.home": {
        "name": "Homepage (FR)", "routes": ["/"], "homeRouteOnly": True,
        "evidence": [cite("src/App.jsx", "<section id=\"HOME\">", "</section>"), cite("ia.json", "\"id\": \"template.home\"")],
        "nodes": [{"section": s, "variant": "default", "required": s in REQUIRED, "repeatable": False} for s in ORDER],
        "nodeOrderNote": "Order = DOM order of src/App.jsx (Scene, Header{Loader, bar, Menu}, Hero + SeoModal, then #HOME sections, then footer#FOOTER split into conversion.closing-cta + chrome.footer). Optional nodes may be omitted; present nodes must keep this order."}},
    "routes": [{"route": "/", "template": "template.home"}],
    "notBuilt": {"reason": "Links to the original site's other pages; the clone only cloned the FR homepage (README.md, ia.json meta).", "evidence": [cite("README.md", "Only `/` is cloned")]},
}
dump("templates/templates.json", templates)

# ----------------------------------------------------------------------------------- compatibility graph
CATS = {k: v["semantic"]["category"] for k, v in SECTIONS.items()}
IN_FLOW = [s for s in ORDER if SECTIONS[s]["positionKind"] == "in-flow"]
real_adj = [[a, b] for a, b in zip(IN_FLOW, IN_FLOW[1:]) if CATS[a] == CATS[b]]
real_stage_adj = [[a, b] for a, b in zip(IN_FLOW, IN_FLOW[1:]) if SECTIONS[a]["scrollStage"] and SECTIONS[b]["scrollStage"]]
graph = {
    "$description": "Rhythm/position rules JSON Schema cannot express. Each rule is enforced by schema/semantic_validate.py under the same id; verify_all.py checks the two lists agree. Exceptions were read off templates/templates.json's real node order (in-flow sections only).",
    "version": VERSION,
    "categories": sorted(set(CATS.values())),
    "inFlowOrder": IN_FLOW,
    "rules": [
        {"id": "BACKDROP_FIRST", "severity": "error", "description": "backdrop.webgl-scene is the first node (the fixed canvas sits behind everything)."},
        {"id": "ONE_HERO", "severity": "error", "description": "Exactly one HERO-category node per page.", "exceptions": []},
        {"id": "HERO_FIRST_IN_FLOW", "severity": "error", "description": "The HERO is the first in-flow node (fixed CHROME/BACKDROP nodes may precede it)."},
        {"id": "FOOTER_LAST", "severity": "error", "description": "chrome.footer is the last node."},
        {"id": "CLOSING_CTA_BEFORE_FOOTER", "severity": "error", "description": "conversion.closing-cta immediately precedes chrome.footer (they share footer#FOOTER)."},
        {"id": "NO_ADJACENT_SAME_CATEGORY", "severity": "warn", "description": "Two consecutive in-flow nodes should not share a category, except the real pairs below.", "exceptions": real_adj},
        {"id": "NO_CONSECUTIVE_SCROLL_STAGES", "severity": "warn", "description": "Two pinned scroll stages should not follow each other, except the real pair below.", "exceptions": real_stage_adj},
        {"id": "SCROLL_STAGE_BUDGET", "severity": "warn", "description": "At most 5 pinned scroll stages per page (the source has 5: hero, tagline, skills, VR, labels).", "max": 5},
        {"id": "THEME_COMBINATION", "severity": "error", "description": "A node's textTone/accentColor must be allowed for its surfaceTone (tokens/llm/token-policy.json themeCombinations)."},
    ],
}
dump("compatibility/graph.json", graph)
print("templates/graph ok; same-category exceptions:", real_adj, "stage exceptions:", real_stage_adj)

# ----------------------------------------------------------------------------------- reference example (real copy, read from source)
def js_json(path, marker):
    s = open(os.path.join(ROOT, path), encoding="utf-8").read()
    return json.loads(s[s.index(marker) + len(marker):].strip().rstrip(";"))


def clean(s):
    return re.sub(r"\s+", " ", s.replace("<br />", " ")).strip()


U = "/sk/uploads/"
M_ = lambda role_, src_=None, alt=None: {k: v for k, v in (("assetRole", role_), ("src", src_), ("alt", alt)) if v is not None}
REVIEWS = js_json(C + "review-cards/data.js", "export const REVIEWS =")
QUESTIONS = js_json(C + "faq/data.js", "export const QUESTIONS =")
seo_html = js_json(C + "hero/seoContent.js", "export default ")


def seo_parts(h):
    import html as html_
    txt = lambda x: clean(html_.unescape(re.sub(r"<[^>]+>", " ", x)))
    title = txt(re.search(r"<h2[^>]*>(.*?)</h2>", h, re.S).group(1))
    parts = []
    for chunk in re.split(r"(?=<h3)", h)[1:]:
        head = txt(re.search(r"<h3[^>]*>(.*?)</h3>", chunk, re.S).group(1))
        body = re.sub(r"<h3[^>]*>.*?</h3>", "", chunk, flags=re.S)
        paras = [txt(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
        items = [txt(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S)]
        part_ = {"heading": head, "paragraphs": [p for p in paras if p][:6]}
        if items:
            part_["listItems"] = [i for i in items if i][:12]
        parts.append(part_)
    return title, parts


seo_title, seo_parts_ = seo_parts(seo_html)
EXPLORE = [("Réalisations", "/realisations"), ("Nous connaître", "/nous-connaitre"), ("Notre méthode", "/la-methode-labas"), ("Ressources", "/ressources"), ("Contact", "/contact"), ("Offres d'emploi", "/nos-offres-d-emploi")]
LNK = lambda pairs: [{"label": a, "href": b} for a, b in pairs]
EXP_MENU = [("Présentations", "/expertises/presentations-powerpoint"), ("Communication 360", "/expertises/communication-360"), ("Navigation App Like", "/expertises/navigation-interactive-powerpoint"),
            ("Animatiques", "/expertises/Animatiques-powerpoint"), ("Conférences Interactives", "/expertises/conferences-interactives"), ("Séminaire VR", "/expertises/seminaire-realite-virtuelle"),
            ("Solutions IA", "/expertises/solutions-ia-powerpoint"), ("Formations & Coaching", "/expertises/formations-powerpoint-coaching-labas-agence-powerpoint")]
P_ = "/expertises/presentations-powerpoint/"
PRES = [("Présentation", "commerciale", P_ + "presentation-commerciale"), ("Présentation", "corporate", P_ + "presentation-corporate"), ("Présentation", "événementielle", P_ + "presentation-evenementielle-labas-agence-powerpoint"),
        ("Présentation", "appel d’offre", P_ + "presentation-appel-offre"), ("Présentation", "ressources humaines", P_ + "presentation-ressources-humaines"), ("Masque", "PPT", P_ + "masque-ppt-labas-agence-powerpoint"),
        ("Présentation", "marketing", P_ + "presentation-marketing"), ("Présentation", "financière", P_ + "presentation-financiere")]
SOC = [{"network": "linkedin", "href": "https://www.linkedin.com/company/laboiteaslides/"}, {"network": "vimeo", "href": "https://vimeo.com/laboiteaslides?fl=pp&fe=sh"}]
ADDR = "Paris, Bordeaux, Verdun, Aix-en-Provence, Rennes, Strasbourg"
BADGES = [M_("credential.badge", "/sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg", "Certification ISO9001 LABAS"), M_("credential.badge", "/sk/uploads/Badge_simple_MOS_LABAS_d0815bc7cf.svg", "Badge-simple-MOS-LABAS.svg"),
          M_("credential.badge", "/sk/uploads/Logo_simple_Avis_Google_LABAS_d3f7b5bccc.svg", "Avis Google")]
WORKS_ = [("Safran Electronics & Defense", "Corporate", "/realisations/Safran-Electronics-Defense-presentation-corporate", "Safran_0239f5157e.jpg", "Safran.jpg"),
          ("Adidas", "Masque", "/realisations/adidas-masque-powerpoint", "Adidas_2_20aaceff99.jpg", "Adidas-2.jpg"),
          ("Marriott", "Commerciale", "/realisations/marriott-presentation-commerciale-interactive", "Touchscreen_Mariott_la_boite_a_slides_agence_powerpoint_0415bcab60.jpg", "une personne utilisant la présentation Interactive pour Mariott sur table tactile"),
          ("LIPTON", "Évènement", "/realisations/lipton-presentation-evenement-selling-story", "Ekaterra_Tea_Lipton_43f10e2e06.jpg", "Ekaterra-Tea-Lipton.jpg"),
          ("Brasseries Kronenbourg", "Interactions Live", "/realisations/brasseries-kronenbourg-presentation-evenementielle-gamification", "Brasseries_kronenbourg_sceno_72f519a001.jpg", "Mise en situation sur scène d'un quiz géant projeté pour une convention Brasseries Kronenbourg"),
          ("Nissan", "Marketing", "/realisations/nissan-presentation-marketing", "Nissan_ef41272a76.jpg", "Nissan.jpg"),
          ("Viridien", "Finance", "/realisations/viridien-presentation-financiere-resultats-annuels", "Viridien_e87722da36.jpg", "Photo aérienne pour illustrer le projet Powerpoint Viridien"),
          ("Upciti", "Masque", "/realisations/upciti-masque-powerpoint", "Upciti_82768aec88.jpg", "Upciti.jpg")]
EXPS = [("Présentations", "/expertises/presentations-powerpoint", "Presentation_e945d6b799.png", "Presentation.png"), ("Communication 360", "/expertises/communication-360", "Communication_360_7a5ef30bda.png", "Communication-360.png"),
        ("Navigation App Like", "/expertises/navigation-interactive-powerpoint", "FDH_URW_navigation_interactive_87d42a0822.jpg", "Un homme cliquant sur la présentation interaction du Forum des halles sur un ipad"),
        ("Séminaire VR", "/expertises/seminaire-realite-virtuelle", "Immersion_VR_e950803a61.png", "Immersion-VR.png"), ("Solutions IA", "/expertises/solutions-ia-powerpoint", "Assistance_IA_LABAS_bot_1963bf7998.jpg", "Bot Assistance IA La boite à slides")]
MARQ = "Depuis 2002 ● ISO 9001 ● 5/5 Note Google Avis ● +8 000 projets ● 85% de réachat ● MOS PowerPoint"


def mo(sec_id, patterns=None):
    m = SECTIONS[sec_id]["motion"]
    return {"patterns": patterns if patterns is not None else list(m["allowedPatterns"]), "reducedMotionFallback": m["reducedMotionFallback"]}


def node(i, sec_id, content, tokens_=None):
    n = {"id": f"n{i:02d}", "section": sec_id, "variant": "default", "content": content, "motion": mo(sec_id)}
    if tokens_:
        n["tokens"] = tokens_
    if not SECTIONS[sec_id]["retrievalEligible"]:
        n["retrievalEligible"] = False
    return n


LGH = {"surfaceTone": "backdrop.lgh", "textTone": "color.drk1", "accentColor": "color.prm1"}
REF_CONTENT = {
    "backdrop.webgl-scene": ({"plugins": ["gradient-layers", "glass-triangles", "title-3d", "vr-sphere", "rgb-shift"], "mobileFallback": "static-gradient"}, None),
    "chrome.loader": ({"spinner": "two-triangles"}, {"surfaceTone": "backdrop.prm"}),
    "chrome.header": ({"brandMark": M_("brand.wordmark", "inline-svg:Logo", "Logo - la Boite à Slides"), "menuLabel": "Menu", "closeLabel": "Fermer", "cta": {"label": "Demander un devis", "href": "/contact"}}, None),
    "chrome.menu-overlay": ({"languages": ["fr", "en"], "widgets": [
        {"kind": "expertise", "title": "Conférences Interactives", "ctaLabel": "Découvrir", "href": "/expertises/conferences-interactives", "media": M_("resource.cover", U + "large_Presentation_augmentee_1d02882a38.jpg", "Presentation-augmentee.jpg")},
        {"kind": "whitePaper", "tag": "Livre blanc", "title": "4 conseils pour capter l’attention en 1 minute", "href": "/ressources/4-conseils-pour-capter-lattention-en-1-minute"},
        {"kind": "clientCase", "tag": "Cas client", "title": "Arcitek - Présentation corporate", "href": "/ressources/arcitek-presentation-corporate", "media": M_("resource.cover", U + "large_Adobe_Stock_206118370_5ab61dcb89.jpg", "AdobeStock_206118370.jpg")}],
        "explore": {"title": "Explorer", "links": LNK(EXPLORE)}, "expertises": {"title": "Expertises", "links": LNK(EXP_MENU)}, "address": ADDR, "socials": SOC}, {"surfaceTone": "backdrop.lgh"}),
    "hero.statement": ({"titleLines": [{"lead": "Les meilleures idées font", "emphasis": "l'avenir"}, {"lead": "Quand elles sont bien", "emphasis": "présentées"}],
                        "subtitle": clean("La boite à slides® :<br />seule agence au monde<br />certifiée ISO 9001<br />qui transforme Powerpoint<br />en un puissant levier d'impact<br />pour votre business"),
                        "video": M_("hero.loop-video", U + "home_video_SD_79c96be094.mp4"), "scrollBadge": True}, {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1"}),
    "chrome.seo-modal": ({"title": seo_title, "parts": seo_parts_}, None),
    "story.tagline": ({"statement": "Notre agence PowerPoint amplifie le retentissement des présentations stratégiques des leaders. On équipe ceux qui veulent faire bouger les lignes, dans tous les secteurs",
                       "body": clean("Nos clients ont des idées fortes, des stratégies à partager, des messages complexes à faire passer.\nAvec des contenus interactifs et des expériences captivantes, ils offrent à leur cible ce qu’il y a de plus puissant : l’évidence.")},
                      {"surfaceTone": "backdrop.scd", "textTone": "color.drk1"}),
    "proof.works": ({"title": {"lead": "Un seul outil, des", "emphasis": "possibilités infinies"}, "cards": [{"client": a, "tag": b, "href": c, "media": M_("case.photo", U + d, e)} for a, b, c, d, e in WORKS_]}, LGH),
    "proof.method": ({"marquee": MARQ.split(" ● "), "tagline": "Tirer parti des dernières avancées technologiques et intelligences artificielles pour valoriser vos messages les plus importants",
                      "body": "À la boite à slides, on maximise l'engagement de votre public depuis 2002. On repousse les limites de PowerPoint pour vous faire gagner en impact, en performance et en autonomie. Pour votre plus grande satisfaction.",
                      "metrics": ["La seule agence PPT au monde certifiée ISO 9001", "85% de réachat", "5/5 Note Google Avis", "Certifiés Microsoft Office Specialist PowerPoint"]}, LGH),
    "offer.skills": ({"items": [{"statement": "0 retard sur +8 000 projets. Nous utilisons la rigueur de l'ISO 9001 pour sécuriser vos calendriers.", "badges": BADGES},
                                {"statement": "96% de stabilité de l'enveloppe budgétaire. Notre méthode vise la justesse dès le départ pour respecter votre budget.", "badges": BADGES},
                                {"statement": "La preuve ultime d'un rendu maîtrisé ? Un taux de réachat de 85% auprès des directions marketing, qui nous renouvellent leur confiance au cours de l'année.", "badges": [], "cta": {"label": "Voir nos réalisations", "href": "/realisations"}}]},
                     {"surfaceTone": "backdrop.trt", "textTone": "color.drk1", "buttonDesign": "button.design.darkGlass"}),
    "offer.expertises": ({"title": "Nos expertises", "routes": [{"label": a, "href": b, "media": M_("expertise.photo", U + "large_" + c, d)} for a, b, c, d in EXPS]}, LGH),
    "story.vr": ({"title": {"lead": "Dépassez toutes les", "emphasis": "limites de PowerPoint"}, "body": "Une expérience aussi bluffante, vous n’êtes pas prêt de l’oublier. Votre public non plus.",
                  "cta": {"label": "En savoir plus", "href": "/expertises/conferences-interactives"}}, {"surfaceTone": "backdrop.blk", "textTone": "color.gry3", "accentColor": "color.prm1"}),
    "offer.spotlight": ({"title": {"lead": "Toujours carrés.", "emphasis": "Jamais formatés."}, "body": "Une équipe de spécialistes qui réunit sans concession une culture de la réflexion et le goût de l’inattendu. Ça donne la première agence Powerpoint en France.",
                         "cta": {"label": "Nous connaître", "href": "/nous-connaitre"}, "media": M_("team.photo", U + "large_Labas_20f4ebe642.jpg", "logo la boite à slides")}, {**LGH, "blockGap": "space.20"}),
    "content.resources": ({"title": {"lead": "Nos dernières", "emphasis": "ressources"}, "cta": {"label": "Voir toutes nos ressources", "href": "/ressources"}, "cards": [
        {"kind": "article", "tag": "Article", "publishedAt": "2025-01-12", "title": "Gamification et PowerPoint : mettez du jeu dans vos formations !", "href": "/ressources/gamification-et-powerpoint-mettez-du-jeu-dans-vos-formations"},
        {"kind": "clientCase", "tag": "Cas client", "publishedAt": "2026-03-18", "title": "Ideuzo- Présentation commerciale", "href": "/ressources/ideuzo-presentation-commerciale", "media": M_("resource.cover", U + "large_presentation_equipe_0eebf6541e.jpeg", "équipe qui applaudit")},
        {"kind": "whitePaper", "tag": "Livre blanc", "publishedAt": "2026-01-27", "title": "Gagner en autonomie sur PowerPoint", "href": "/ressources/gagner-en-autonomie-sur-powerpoint"}]}, {**LGH, "blockGap": "space.20"}),
    "proof.labels": ({"title": {"lead": "Engagés pour", "emphasis": "la qualité"}, "cards": [
        {"title": "5 étoiles Google Avis", "tag": "Notation 2026", "media": M_("credential.badge", U + "Badge_Google_avis_labas_149fc344c9.png", "illustration du badge 5 étoiles avis google"), "isPlaceholder": False},
        {"title": "Certifié ISO 9001:2015 Bureau Veritas", "tag": "Certification 2025", "media": M_("credential.badge", U + "Badge_ISO_9001_labas_49c6d38cef.png", "illustration du badge certification ISO9001 de la boite à slides"), "isPlaceholder": False},
        {"title": "Microsoft Office Specialist", "tag": "Depuis 2020", "media": M_("credential.badge", U + "Badge_MOS_labas_83992cf13f.png", "illustration du badge Microsoft Office Specialist de la boite à slides"), "isPlaceholder": False}]},
        {"surfaceTone": "backdrop.drk", "textTone": "color.lgh1", "accentColor": "color.prm1"}),
    "proof.reviews": ({"title": {"lead": "Ils nous font", "emphasis": "confiance"}, "reviews": [
        {"person": {"name": r["title"].strip(), "role": r["role"].strip(), "isFictional": False}, "quote": clean(r["content"]), "media": M_("client.logo", r["src"], r["alt"])} for r in REVIEWS]}, LGH),
    "content.faq": ({"overline": "FAQ", "title": {"lead": "Des questions?", "emphasis": "On vous répond"}, "items": [{"question": q.strip(), "answer": clean(a)} for q, a in QUESTIONS], "pageSize": 6, "moreLabel": "Voir plus de questions"}, LGH),
    "conversion.closing-cta": ({"title": {"lead": "Prêt à transformer votre", "emphasis": "impact?"}, "cta": {"label": "Contactez-nous", "href": "/contact"}}, {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1", "buttonDesign": "button.design.light"}),
    "chrome.footer": ({"brandMark": M_("brand.wordmark", "inline-svg:Logo", "Logo - la Boite à Slides"), "languages": ["fr", "en"], "address": ADDR, "navGroups": [
        {"title": "Explorer", "links": LNK(EXPLORE)}, {"title": "Expertises", "links": LNK(EXP_MENU[1:])},
        {"title": "Présentations", "links": [{"strong": a, "label": b, "href": c} for a, b, c in PRES]}],
        "credentials": [{"title": "Certifié ISO 9001:2015 Bureau Veritas", "media": M_("credential.badge", U + "Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg", "Certification ISO9001 LABAS"), "isPlaceholder": False},
                        {"title": "Microsoft Office Specialist", "media": M_("credential.badge", U + "Badge_simple_MOS_LABAS_d0815bc7cf.svg", "Badge-simple-MOS-LABAS.svg"), "isPlaceholder": False},
                        {"title": "5 étoiles Google Avis", "media": M_("credential.badge", U + "Logo_simple_Avis_Google_LABAS_f10bfef852.svg", "Avis Google LABAS"), "isPlaceholder": False}],
        "legalLinks": LNK([("Mentions légales", "/mentions-legales"), ("Politique de confidentialité", "/politique-de-confidentialite"), ("Cookies", "#")]), "socials": SOC, "showCopyrightYear": True, "seoModalTrigger": True},
        {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1"}),
}
ref_spec = {"pageSpecVersion": VERSION, "mode": "reference", "template": "template.home", "route": "/", "locale": "fr-FR", "theme": "light",
            "brand": {"name": "La boîte à slides", "isFictional": False}, "fonts": {"display": "font.family.display", "text": "font.family.text"},
            "nodes": [node(i + 1, s, *REF_CONTENT[s]) for i, s in enumerate(ORDER)]}
dump("schema/example.pagespec.json", ref_spec)

# ----------------------------------------------------------------------------------- generated example (fictional, original copy)
X = "https://northlight.example"
G = lambda role_, alt=None: M_(role_, None, alt)
GEN_CONTENT = {
    "backdrop.webgl-scene": ({"plugins": ["gradient-layers", "glass-triangles", "title-3d", "rgb-shift"], "mobileFallback": "static-gradient"}, None),
    "chrome.loader": ({"spinner": "two-triangles"}, {"surfaceTone": "backdrop.prm"}),
    "chrome.header": ({"brandMark": G("brand.placeholder-mark", "Northlight Decks placeholder mark"), "menuLabel": "Menu", "closeLabel": "Close", "cta": {"label": "Plan a deck", "href": "/brief"}}, None),
    "chrome.menu-overlay": ({"languages": ["en"], "widgets": [{"kind": "expertise", "title": "Keynote rehearsal studio", "ctaLabel": "Explore", "href": "/services/rehearsal", "media": G("media.placeholder", "Placeholder studio image")}],
                             "explore": {"title": "Explore", "links": LNK([("Projects", "/projects"), ("Studio", "/studio"), ("Journal", "/journal"), ("Brief us", "/brief")])},
                             "expertises": {"title": "Services", "links": LNK([("Investor decks", "/services/investor"), ("Sales stories", "/services/sales"), ("Event keynotes", "/services/events")])},
                             "address": "Remote-first studio, fictional harbour town", "socials": [{"network": "linkedin", "href": X + "/social/linkedin"}]}, {"surfaceTone": "backdrop.lgh"}),
    "hero.statement": ({"titleLines": [{"lead": "Ideas travel further", "emphasis": "on stage"}, {"lead": "When every slide", "emphasis": "lands"}],
                        "subtitle": "Northlight Decks is a fictional studio that turns dense briefs into calm, confident keynotes for teams who present to big rooms.",
                        "video": G("media.generated-video"), "scrollBadge": True}, {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1"}),
    "story.tagline": ({"statement": "We sit between the strategist and the stage, shaping every argument so the room follows it without effort.", "body": "Our clients arrive with too much to say. We help them say less, show more and leave a single idea behind."},
                      {"surfaceTone": "backdrop.scd", "textTone": "color.drk1"}),
    "proof.works": ({"title": {"lead": "One canvas,", "emphasis": "many rooms"}, "cards": [{"client": f"Sample client {c}", "tag": t, "href": f"/projects/sample-{c.lower()}", "media": G("media.generated-image", f"Generated cover {c}")} for c, t in (("A", "Investor"), ("B", "Sales"), ("C", "Event"), ("D", "Training"))]}, LGH),
    "proof.method": ({"marquee": ["Fictional studio", "Sample metric one", "Sample metric two"], "tagline": "Research, story and design move together from the first call to the final rehearsal.",
                      "body": "Every project starts with the audience and ends with a speaker who knows each slide by heart.", "metrics": ["Placeholder proof point one", "Placeholder proof point two"]}, LGH),
    "offer.skills": ({"items": [{"statement": "Clear schedules agreed on day one, reviewed every week until delivery.", "badges": [G("credential.placeholder-badge", "Placeholder credential")]},
                                {"statement": "Budgets framed by scope, with every change discussed before it happens.", "badges": []},
                                {"statement": "Most teams come back for their next big moment.", "badges": [], "cta": {"label": "See sample projects", "href": "/projects"}}]},
                     {"surfaceTone": "backdrop.trt", "textTone": "color.drk1", "buttonDesign": "button.design.darkGlass"}),
    "offer.expertises": ({"title": "What we make", "routes": [{"label": a, "href": b, "media": G("media.generated-image", a)} for a, b in (("Investor decks", "/services/investor"), ("Sales stories", "/services/sales"), ("Event keynotes", "/services/events"))]}, LGH),
    "story.vr": ({"title": {"lead": "Step inside", "emphasis": "the story"}, "body": "An immersive walk-through that lets a room explore the plan before it is built.", "cta": {"label": "Learn more", "href": "/services/immersive"}},
                 {"surfaceTone": "backdrop.blk", "textTone": "color.gry3", "accentColor": "color.prm1"}),
    "offer.spotlight": ({"title": {"lead": "Calm process.", "emphasis": "Bold slides."}, "body": "A small fictional team of writers and designers who prefer one strong idea to twenty weak ones.", "cta": {"label": "Meet the studio", "href": "/studio"}, "media": G("media.generated-image", "Generated studio illustration")}, LGH),
    "content.resources": ({"title": {"lead": "From the", "emphasis": "journal"}, "cta": {"label": "Read the journal", "href": "/journal"}, "cards": [
        {"kind": "article", "tag": "Article", "publishedAt": "2026-02-01", "title": "Three ways to open a keynote", "href": "/journal/open-a-keynote"},
        {"kind": "clientCase", "tag": "Case", "publishedAt": "2026-03-01", "title": "Sample client B sales story", "href": "/journal/sample-b", "media": G("media.generated-image", "Generated case cover")},
        {"kind": "whitePaper", "tag": "Guide", "publishedAt": "2026-04-01", "title": "Rehearsal checklist", "href": "/journal/rehearsal-checklist"}]}, LGH),
    "proof.labels": ({"title": {"lead": "Held to", "emphasis": "a standard"}, "cards": [{"title": f"Placeholder credential {k}", "tag": "Sample year", "media": G("credential.placeholder-badge", "Placeholder badge"), "isPlaceholder": True} for k in ("A", "B")]},
                     {"surfaceTone": "backdrop.drk", "textTone": "color.lgh1", "accentColor": "color.prm1"}),
    "proof.reviews": ({"title": {"lead": "Kind", "emphasis": "words"}, "reviews": [
        {"person": {"name": n, "role": r, "isFictional": True}, "quote": q, "media": G("person.fictional-avatar", "Illustrated avatar")} for n, r, q in (
            ("Alex Sample", "Fictional head of sales", "The deck finally sounded like us, only clearer."),
            ("Jordan Example", "Fictional event lead", "Our speakers walked on stage relaxed for the first time."),
            ("Sam Placeholder", "Fictional founder", "Investors asked better questions because the story was easy to follow."))]}, LGH),
    "content.faq": ({"overline": "FAQ", "title": {"lead": "Questions?", "emphasis": "Answered"}, "items": [
        {"question": "How does a project start?", "answer": "With a short call about the audience, the date and the one idea the room must remember."},
        {"question": "Do you write the content?", "answer": "Yes, or we edit yours. Either way the story is agreed before design begins."}], "pageSize": 6, "moreLabel": "More questions"}, LGH),
    "conversion.closing-cta": ({"title": {"lead": "Ready for your", "emphasis": "next stage?"}, "cta": {"label": "Start a brief", "href": "/brief"}}, {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1", "buttonDesign": "button.design.light"}),
    "chrome.footer": ({"brandMark": G("brand.placeholder-mark", "Northlight Decks placeholder mark"), "languages": ["en"], "address": "Remote-first studio, fictional harbour town",
                       "navGroups": [{"title": "Explore", "links": LNK([("Projects", "/projects"), ("Studio", "/studio"), ("Journal", "/journal")])}],
                       "credentials": [{"title": "Placeholder credential A", "media": G("credential.placeholder-badge", "Placeholder badge"), "isPlaceholder": True}],
                       "legalLinks": LNK([("Legal notice", "/legal"), ("Privacy", "/privacy")]), "socials": [{"network": "linkedin", "href": X + "/social/linkedin"}], "showCopyrightYear": True, "seoModalTrigger": False},
                      {"surfaceTone": "backdrop.prm", "textTone": "color.lgh1", "accentColor": "color.drk1"}),
}
GEN_ORDER = [s for s in ORDER if s in GEN_CONTENT]
gen_spec = {"pageSpecVersion": VERSION, "mode": "generated", "template": "template.home", "route": "/", "locale": "en-GB", "theme": "light",
            "brand": {"name": "Northlight Decks", "isFictional": True}, "fonts": {"display": "font.family.text", "text": "font.family.text"},
            "nodes": [node(i + 1, s, *GEN_CONTENT[s]) for i, s in enumerate(GEN_ORDER)]}
dump("schema/examples/generated.home.pagespec.json", gen_spec)

# ----------------------------------------------------------------------------------- source identity registry (R2)
def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("assetRole", "kind", "network", "href", "src", "publishedAt"):
                yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


SHINGLE = 6


def shingles(text):
    w = norm(text).split()
    return {" ".join(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)}


ref_text = [s for n in ref_spec["nodes"] for s in strings(n["content"])]
sh = sorted({hashlib.sha256(x.encode()).hexdigest()[:16] for t in ref_text for x in shingles(t)})
TITLES = [f"{n['content']['title']['lead']} {n['content']['title']['emphasis']}" for n in ref_spec["nodes"] if isinstance(n["content"].get("title"), dict)]
TITLES += [f"{t['lead']} {t['emphasis']}" for t in REF_CONTENT["hero.statement"][0]["titleLines"]]
identity = {
    "$description": "Single registry of the source's identity and content (R2). Every pattern is taken from the real source (src/, CLONE_SPEC_*.md, schema/example.pagespec.json). Matching is done on normalised text (lower-case, accents stripped, punctuation folded) by schema/semantic_validate.py in mode=generated only.",
    "version": VERSION,
    "normalisation": "NFKD, strip accents, lower-case, fold any char outside [a-z0-9%+/'.:-] to a space",
    "sourceBrand": {"patterns": ["la boite a slides", "boite a slides", "laboiteaslides", "labas", "la boite a slide"], "legalMarks": ["®"],
                    "evidence": [cite("index.html", "<title>La boite à slides®"), cite(C + "hero/seoContent.js", "export default"), cite(C + "header/icons.jsx", "<title>Logo - la Boite à Slides</title>")]},
    "domains": ["laboiteaslides.fr", "laboiteaslides.com", "linkedin.com/company/laboiteaslides", "vimeo.com/laboiteaslides"],
    "assetPathPrefixes": ["/sk/uploads/", "/_nuxt/", "/_i18n/", "/assets/models/", "/assets/hdr/", "/assets/fonts/", "/fonts/FKScreamer/", "inline-svg:Logo"],
    "storePatterns": ["apps.apple.com", "itunes.apple.com", "play.google.com", "testflight.apple.com", "app store", "google play", "testflight", "disponible sur", "download on the"],
    "ctaStrings": ["Demander un devis", "Voir nos réalisations", "En savoir plus", "Nous connaître", "Voir toutes nos ressources", "Voir plus de questions", "Contactez-nous", "Découvrir"],
    "distinctivePhrases": sorted(set(TITLES + ["seule agence au monde certifiee", "on equipe ceux qui veulent faire bouger les lignes", "tirer parti des dernieres avancees", "toujours carres", "jamais formates",
                                               "une experience aussi bluffante", "pret a transformer votre impact", "activateur d'impact"])),
    "claimPatterns": ["iso 9001", "bureau veritas", "microsoft office specialist", "8 000 projets", "8000 projets", "85% de reachat", "85 % de reachat", "96% de stabilite", "depuis 2002", "0 retard", "+400"],
    "ratingPatterns": ["5/5", "5 etoiles", "google avis", "avis google", "note google"],
    "personNames": sorted({r["title"].strip() for r in REVIEWS} | {"Ulrich"}),
    "clientNames": ["Safran", "Adidas", "Marriott", "Mariott", "Lipton", "Ekaterra", "Kronenbourg", "Nissan", "Viridien", "Upciti", "Arcitek", "Ideuzo", "Caterpillar", "Essilor", "Bostik", "Vaudoise", "Syngenta",
                    "Nestle Waters", "San Pellegrino", "Perrier", "Engie", "Krys", "Unibail", "URW", "Forum des Halles", "Araymond", "Audiens", "Axa", "Babymoov", "Brico Depot", "CBRE", "Candriam", "Chanel", "Coface",
                    "Econocom", "Essity", "Flextone", "General Motors", "Liebig", "Limatech", "Mars Wrigley", "Nuxe", "Pukka", "Renault", "Saur", "Tishman Speyer", "TotalEnergies", "Total Energies", "Trivial Pursuit", "Upcoop", "Vittel"],
    "clientNamesEvidence": [cite(C + "Works.jsx", "const WORKS = ["), cite(C + "review-cards/data.js", "export const REVIEWS"), cite("src/scene/vr.js", "the 61 `small_*` thumbnails"), cite(C + "hero/seoContent.js", "export default")],
    "copyShingles": {"size": SHINGLE, "hash": "sha256(normalised 6-word shingle)[:16]", "count": len(sh), "values": sh,
                     "builtFrom": "every text field of schema/example.pagespec.json (the real copy of the reference page)"},
}
dump("policy/source-identity.json", identity)

# ----------------------------------------------------------------------------------- schemas
FONT_TOKENS = sorted(k for k in toks if k.startswith("font.family."))
defs = {
    "media": obj({"assetRole": {"type": "string", "enum": MEDIA_ROLES}, "src": {"type": "string", "minLength": 1, "maxLength": 300}, "alt": {"type": "string", "maxWords": 24}}, ["assetRole"]),
    "tokens": {"type": "object", "additionalProperties": False, "properties": {k: {"type": "string", "minLength": 1, "maxLength": 64} for k in policy["nodeSlots"]}},
}
for sid, sc in SECTIONS.items():
    defs[f"content.{sid}"] = sc["content"]
    defs[f"motion.{sid}"] = obj({"patterns": {"type": "array", "uniqueItems": True, "minItems": 1 if sc["motion"]["allowedPatterns"] else 0, "maxItems": max(len(sc["motion"]["allowedPatterns"]), 0),
                                              "items": {"type": "string", "enum": sc["motion"]["allowedPatterns"] or ["__none__"]}},
                                 "reducedMotionFallback": {"type": "string", "const": sc["motion"]["reducedMotionFallback"]}})
pagespec_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://design-repo.invalid/laboiteaslides-home/pagespec.schema.json",
    "title": "PageSpec (laboiteaslides FR homepage design-repo)", "description": "Generated by extraction/build_repo.py from sections/*.json (content/motion definitions are copied verbatim; verify_all checks they stay identical). 'maxWords' is a custom keyword enforced by schema/semantic_validate.py.",
    "type": "object", "additionalProperties": False,
    "required": ["pageSpecVersion", "mode", "template", "route", "locale", "theme", "brand", "fonts", "nodes"],
    "properties": {
        "pageSpecVersion": {"type": "string", "const": VERSION},
        "mode": {"type": "string", "enum": ["reference", "generated"]},
        "template": {"type": "string", "enum": sorted(templates["templates"])},
        "route": {"type": "string", "pattern": "^/[A-Za-z0-9/_-]*$"},
        "locale": {"type": "string", "pattern": "^[a-z]{2}-[A-Z]{2}$"},
        "theme": {"type": "string", "enum": ["light"]},
        "brand": obj({"name": {"type": "string", "minLength": 1, "maxWords": 6}, "isFictional": {"type": "boolean"}}),
        "fonts": obj({"display": {"type": "string", "minLength": 1, "maxLength": 64}, "text": {"type": "string", "minLength": 1, "maxLength": 64}}),
        "nodes": {"type": "array", "minItems": 1, "items": {"$ref": "#/definitions/node"}},
    },
    "definitions": {**defs, "node": {
        "type": "object", "additionalProperties": False, "required": ["id", "section", "variant", "content", "motion"],
        "properties": {"id": {"type": "string", "pattern": "^n[0-9]{2}$"}, "section": {"type": "string", "enum": ORDER}, "variant": {"type": "string", "enum": ["default"]},
                       "content": {"type": "object"}, "motion": {"type": "object"}, "tokens": {"$ref": "#/definitions/tokens"}, "retrievalEligible": {"type": "boolean"}},
        "allOf": [{"if": {"properties": {"section": {"const": s}}, "required": ["section"]},
                   "then": {"properties": {"content": {"$ref": f"#/definitions/content.{s}"}, "motion": {"$ref": f"#/definitions/motion.{s}"}}}} for s in ORDER]}},
}
dump("schema/pagespec.schema.json", pagespec_schema)

CAT_ENUM = ["BACKDROP", "CHROME", "HERO", "STORY", "PROOF", "OFFER", "CONTENT", "CONVERSION"]
E = obj({"cite": {"type": "string", "pattern": "^[^:\\s][^:]*:[0-9]+(-[0-9]+)?$"}, "needle": {"type": "string", "minLength": 1}})
contract_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#", "$id": "https://design-repo.invalid/laboiteaslides-home/section-contract.schema.json",
    "title": "Section contract", "type": "object", "additionalProperties": False,
    "required": ["id", "version", "title", "description", "source", "semantic", "retrievalEligible", "positionKind", "scrollStage", "variants", "content", "constraints", "motion", "responsive", "surfaceTones", "assetRoles", "generatedAssetRoles", "evidence"],
    "properties": {
        "id": {"type": "string", "pattern": "^[a-z]+\\.[a-z0-9-]+$"}, "version": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string", "minLength": 30},
        "source": obj({"id": {"type": "string"}, "file": {"type": "string"}, "tag": {"type": "string", "minLength": 3}, "lines": {"type": "string", "pattern": "^[0-9]+(-[0-9]+)?$"}, "citation": {"type": "string"}}),
        "semantic": obj({"id": {"type": "string"}, "category": {"type": "string", "enum": CAT_ENUM}}),
        "retrievalEligible": {"type": "boolean"}, "retrievalIneligibleReason": {"type": "string", "minLength": 30},
        "positionKind": {"type": "string", "enum": ["fixed", "in-flow"]}, "scrollStage": {"type": "boolean"},
        "variants": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "content": {"type": "object"}, "constraints": {"type": "object", "additionalProperties": False, "properties": {k: {"type": ["boolean", "string"]} for k in ("onePerPage", "mustBeFirst", "mustBeFirstInFlow", "mustBeLast", "mustPrecede")}},
        "motion": obj({"allowedPatterns": {"type": "array", "items": {"type": "string", "enum": sorted(PATTERNS)}}, "triggers": {"type": "array", "items": {"type": "string", "enum": ["scroll-scrub", "scroll-toggle", "load", "time", "hover", "click", "drag", "menu-toggle"]}},
                       "reducedMotionFallback": {"type": "string", "enum": sorted(FALLBACKS)}, "reducedMotionFallbackText": {"type": "string"}, "evidence": {"type": "array", "items": E, "minItems": 1}}),
        "responsive": obj({"desktop": {"type": "string"}, "tablet": {"type": "string"}, "mobile": {"type": "string"}, "evidence": {"type": "array", "items": E, "minItems": 1}}),
        "surfaceTones": {"type": "array", "items": {"type": "string", "enum": SURFACES}},
        "assetRoles": {"type": "array", "items": {"type": "string", "enum": sorted(ROLES)}}, "generatedAssetRoles": {"type": "array", "items": {"type": "string", "enum": sorted(ROLES)}},
        "evidence": {"type": "array", "items": E}, "generationNotes": {"type": "string"},
    },
    "if": {"properties": {"retrievalEligible": {"const": False}}}, "then": {"required": ["retrievalIneligibleReason"]},
}
dump("schema/section-contract.schema.json", contract_schema)

# ----------------------------------------------------------------------------------- allowlist
allow = {"$description": "Closed list of what a generator may place and set. Parity with sections/, primitives/, components/ is checked by verify_all.py (no phantom entries, no orphans); settable fields are re-derived from schema/pagespec.schema.json.",
         "version": VERSION,
         "sections": {s: {"settable": {"content": sorted(SECTIONS[s]["content"]["properties"]), "motion": ["patterns", "reducedMotionFallback"], "tokens": sorted(policy["nodeSlots"]), "node": ["id", "variant", "retrievalEligible"]},
                          "variants": SECTIONS[s]["variants"], "retrievalEligible": SECTIONS[s]["retrievalEligible"],
                          "assetRoles": {"reference": SECTIONS[s]["assetRoles"], "generated": SECTIONS[s]["generatedAssetRoles"]}} for s in ORDER},
         "primitives": sorted(p_["id"] for p_ in PRIMS), "components": sorted(c_["id"] for c_ in COMPS),
         "pageLevel": ["pageSpecVersion", "mode", "template", "route", "locale", "theme", "brand", "fonts"]}
dump("tokens/llm/component-allowlist.json", allow)
print("schemas + allowlist ok")

# ----------------------------------------------------------------------------------- measured values (from tracked raw captures)
def sha_file(rel):
    return hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()


raw_h = json.load(open(os.path.join(HERE, "raw-section-heights.json"), encoding="utf-8"))
raw_s = json.load(open(os.path.join(HERE, "raw-style-histogram.json"), encoding="utf-8"))
runs = [json.load(open(os.path.join(HERE, "parity", f), encoding="utf-8")) for f in ("results-run1.json", "results-run2.json")]
v1440 = raw_h["viewports"]["1440x900"]
heights = {"viewport": "1440x900", "measuredAt": raw_h["measuredAt"], "tool": raw_h["tool"], "rawFile": "extraction/raw-section-heights.json",
           "routes": {"/": {"documentHeightPx": v1440["documentHeightPx"], "sections": {k: {"heightPx": v["heightPx"], "topPx": v["topPx"], "positionKind": v["positionKind"]} for k, v in v1440["sections"].items()}}},
           "otherViewports": {vp: {"documentHeightPx": v["documentHeightPx"], "htmlFontSizePx": v["htmlFontSizePx"], "inFlowHeightsPx": {k: s["heightPx"] for k, s in v["sections"].items() if s["positionKind"] == "in-flow"}}
                              for vp, v in raw_h["viewports"].items() if vp != "1440x900"}}
# groundwork spot-check: ia.json y positions vs the measurement
ia = json.load(open(os.path.join(ROOT, "ia.json"), encoding="utf-8"))
spot = []
for sid, s in ia["sections"].items():
    m = re.search(r"y ≈? ?([0-9][0-9  ]*(?:\.[0-9])?)", s["description"])
    impl = s.get("implementedBy", "").split(" ")[0]
    impl_path = ("src/" + impl) if impl.startswith("scene/") else (C + impl)
    entry = {"iaSection": sid, "implementedBy": s.get("implementedBy"), "implementedByExists": os.path.exists(os.path.join(ROOT, impl_path))}
    if m:
        ia_y = float(m.group(1).replace(" ", "").replace(" ", ""))
        got = v1440["sections"].get(sid, {}).get("topPx")
        entry.update({"iaYpx": ia_y, "measuredTopPx": got, "agrees": got is not None and abs(got - ia_y) <= 1.5})
    spot.append(entry)
par_secs = sorted(runs[0]["sections"])
parity = {"harness": ["extraction/parity/capture.mjs", "extraction/parity/compare.py"], "metric": runs[0]["metric"],
          "runs": [{"label": r["label"], "file": f"extraction/parity/results-{r['label']}.json", "average": r["average"], "sectionsBelowGate": r["sectionsBelowGate"],
                    "liveDocumentHeightPx": r["capture"]["live"]["documentHeightPx"], "cloneDocumentHeightPx": r["capture"]["clone"]["documentHeightPx"], "consentOverlaysHidden": r["capture"]["live"]["consentOverlaysHidden"],
                    "capturedAt": r["capture"]["live"]["capturedAt"], "gl": r["capture"]["live"]["gl"]} for r in runs],
          "perSection": {s: {"run1": runs[0]["sections"][s]["score"], "run2": runs[1]["sections"][s]["score"], "absDelta": round(abs(runs[0]["sections"][s]["score"] - runs[1]["sections"][s]["score"]), 4)} for s in par_secs},
          "reproducibility": {"maxAbsDeltaBetweenRuns": max(round(abs(runs[0]["sections"][s]["score"] - runs[1]["sections"][s]["score"]), 4) for s in par_secs), "tolerance": 0.05},
          "captureState": "1440x900, GPU ANGLE, Math.random seeded identically on both sides, videos paused at t=0, consent overlays never clicked (hidden only if present: 0 found), same scrollY offsets taken from the clone geometry (live layout verified identical: 35 940 px, every section top equal).",
          "liveScreenshotsCommitted": False,
          "exceptions": [{"section": "story.vr", "scores": [runs[0]["sections"]["story.vr"]["score"], runs[1]["sections"]["story.vr"]["score"]], "gate": runs[0]["metric"]["gate"],
                          "cause": "Diagnosed from the live/clone/diff images: identical DOM layer (title, statement, CTA, header) but the WebGL sphere of 61 client thumbnails assigns textures/positions in a different order on the two sides (the texture-to-tile mapping and per-plane randomness are runtime-dependent), so most of the black frame is covered by different thumbnails. Not a layout or typography defect; cannot be fixed from the design-repo (src/ is read-only for this task) and must not be masked.",
                          "status": "pending human approval", "approvedBy": None}],
          "notes": "Sections between 0.80 and 0.90 (proof.method, proof.labels, chrome.footer) differ by time/random-driven WebGL (triangle bob, background wave, label-card random offsets); they pass the gate in both runs."}
HD = json.load(open(os.path.join(REPO, "extraction", "human-decisions.json"), encoding="utf-8"))
def decision_for(item):
    for d in HD["decisions"]:
        if item in d["items"]:
            return d
    return None
def approval_fields(item):
    d = decision_for(item)
    if not d:
        return {"status": "pending human approval", "approvedBy": None}
    return {"status": "approved", "approvedBy": d["decidedBy"], "approvedAt": d["decidedAt"], "decisionId": d["id"], "decisionVerbatim": d["verbatim"]}
for _e in parity["exceptions"]:
    _e.update(approval_fields("parity.exceptions:" + _e["section"]))
measured = {
    "$description": "Citation and measurement ledger. External evidence (the clone's src/, CLONE_SPEC_*.md, ia.json) is referenced here, never in registry.manifest.json entryPoints. verify_all.py re-checks every citation when the sibling source tree is present and degrades to a warning when it is not.",
    "version": VERSION,
    "sourceRoot": "the design-repo's parent folder (the clone); paths below are relative to it",
    "sourceCommit": "f6c2801",
    "sourcePins": {p: sha_file(p) for p in sorted({"src/App.jsx", "src/index.css", "tailwind.config.js", "CLONE_SPEC_A.md", "CLONE_SPEC_B.md", "CLONE_SPEC_A_ASSETS.md", "ia.json", "index.html", "README.md"} | {s["source"]["file"] for s in SECTIONS.values()})},
    "sectionHeights": heights,
    "wrapperGate": {"thresholdsPinnedIn": "extraction/wrapper_gate.py", "whitelist": [{
        "route": "/", "section": "hero.statement", "rule": "HERO_MAX_HEIGHT", "measuredHeightPx": v1440["sections"]["hero.statement"]["heightPx"], "maxHeightPx": 6350,
        "justification": "The hero is a 700lvh scroll-scrubbed opener: its visible content (3D two-part title, fixed subtitle, video widget) is drawn by the fixed WebGL backdrop and driven by scroll progress, so the DOM wrapper height is scroll distance, not content. It is the page-opening composition only (no other content inside); the source's fit layout on mobile is 1425px.",
        "reviewedBy": "Claude (AI agent) - agent attestation, not a human sign-off", **approval_fields("wrapperGate.whitelist:hero.statement")}]},
    "styleHistogram1440": {"rawFile": "extraction/raw-style-histogram.json", "measuredAt": raw_s["measuredAt"], "color": raw_s["histogram"]["color"], "fontFamily": raw_s["histogram"]["fontFamily"], "fontSize": raw_s["histogram"]["fontSize"],
                           "fontWeight": raw_s["histogram"]["fontWeight"], "borderRadius": raw_s["histogram"]["borderRadius"], "backgroundColor": raw_s["histogram"]["backgroundColor"]},
    "parity": parity,
    "iaReconciliation": {"iaFile": "ia.json", "iaSections": len(ia["sections"]), "contracts": len(SECTIONS),
                         "differences": ["footer#FOOTER (ia: chrome.footer) is split into conversion.closing-cta (title + Contactez-nous CTA, a conversion block) and chrome.footer (nav panel) for R6 category honesty; ia.json is left unchanged (outside this task's write scope)."],
                         "spotChecks": spot},
    "groundworkNotes": ["qa/fullsite/ and reference/ are gitignored in the clone and are never cited.",
                        "ia.json says 'bottom-half sections still in build'; every bottom-half section is present in src/App.jsx and measured here.",
                        "The source has no prefers-reduced-motion handling; reducedMotionFallback values are design-repo requirements grounded in the source's mobile 'fit' layouts."],
}
dump("extraction/measured-values.json", measured)

# ----------------------------------------------------------------------------------- policy + manifest
POLICY_FILES = ["tokens/llm/token-policy.json", "compatibility/graph.json", "schema/pagespec.schema.json", "schema/semantic_validate.py"]
chash = policy_hash.compute(REPO)
design_policy = {
    "$description": "Which common design policy governs this repo and why (R15). The classification is an agent proposal; only the human owner can ratify it.",
    "version": VERSION,
    "policyId": "n0-design-constraints-common", "policyVersion": "0.1.0", "commonIrVersion": "0.5", "enforcementMode": "hard-and-soft", "domain": "agency-marketing",
    "contentHash": chash, "contentHashComputedBy": "extraction/policy_hash.py", "enforcedBy": POLICY_FILES,
    "classification": {"category": "agency-marketing-site",
                       "evidence": ["Single marketing homepage of a presentation-design agency: services index, case studies, credentials, testimonials, FAQ (sections/*.json).",
                                    "Conversion is a quote request / contact link ('Demander un devis' -> /contact, 'Contactez-nous'), not a product sign-up or trial.",
                                    "No pricing tiers, no account or dashboard, no product integrations anywhere in src/.",
                                    "FAQ states projects are billed per day rate after a brief (src/components/faq/data.js)."]},
    "localExtension": {"id": "laboiteaslides-home-local", "rules": ["Generated pages never reproduce the source brand, clients, people, ratings, certifications, copy, URLs or media (schema/semantic_validate.py GENERATED_MODE_*).",
                                                                    "The licensed display typeface is reference-only (tokens/llm/token-policy.json licensedTokens).",
                                                                    "Pinned scroll stages are budgeted (compatibility/graph.json SCROLL_STAGE_BUDGET) and every motion has a reduced-motion fallback."]},
    "approval": ({"status": "approved-by-owner", "architectureDecisionRecorded": True, "decidedBy": decision_for("policy/design-policy.json:approval")["decidedBy"], "decidedAt": decision_for("policy/design-policy.json:approval")["decidedAt"], "decisionId": decision_for("policy/design-policy.json:approval")["id"], "decisionVerbatim": decision_for("policy/design-policy.json:approval")["verbatim"]}
                 if decision_for("policy/design-policy.json:approval") else {"status": "defined-pending-architecture-review", "architectureDecisionRecorded": False, "decidedBy": None, "decidedAt": None}),
}
dump("policy/design-policy.json", design_policy)

FILES = lambda d: sorted(f for f in os.listdir(os.path.join(REPO, d)) if f.endswith(".json"))
counts = {"tokens": len(toks), "sections": len(SECTIONS), "primitives": len(PRIMS), "components": len(COMPS), "templates": len(templates["templates"]), "routes": len(templates["routes"]),
          "assetRoles": len(ROLES), "generationSafeAssetRoles": sum(1 for r in ROLES.values() if r["availability"] == "generation-safe"),
          "retrievalIneligibleSections": sum(1 for s in SECTIONS.values() if not s["retrievalEligible"]), "motionPatterns": len(PATTERNS), "graphRules": len(graph["rules"]),
          "examplePageSpecs": 2}
manifest = {
    "repositoryId": "laboiteaslides-fr-home-design-repo",
    "repositoryVersion": VERSION, "pageSpecVersion": VERSION, "allowlistVersion": allow["version"], "tokenCatalogVersion": catalog["version"],
    "versionFieldNote": "allowlistVersion and tokenCatalogVersion are machine-checked by extraction/verify_all.py (must equal the files' own version fields); pageSpecVersion is enforced as a const by schema/pagespec.schema.json; repositoryVersion is documentation-only and hand-maintained.",
    "status": "design-review-pending", "productionApproved": False,
    "sourceProject": {"name": "La boîte à slides FR homepage clone", "origin": "https://laboiteaslides.fr/ (French homepage only)", "location": "parent folder of this design-repo", "commit": "f6c2801",
                      "realCompany": True, "handling": "Real, live agency site: keep private, never publish generated pages that reuse its identity (see assets/asset-roles.json, policy/source-identity.json)."},
    "sourceStack": {"documentationOnly": True, "detected": "React 18.3 + Vite 5 + Tailwind CSS 3.4; three r181 WebGL canvas; GSAP 3.13 (ScrollTrigger, SplitText, CustomEase); Lenis 1.3",
                    "note": "Recorded for provenance only; no token, section id, schema field or validator rule depends on it."},
    "category": "agency-marketing-site",
    "designPolicy": {"policyId": design_policy["policyId"], "policyVersion": design_policy["policyVersion"], "commonIrVersion": "0.5", "enforcementMode": "hard-and-soft", "domain": "agency-marketing",
                     "contentHash": chash, "file": "policy/design-policy.json", "approval": design_policy["approval"]["status"]},
    "defaultTheme": "light", "schemaValidatedThemes": ["light"],
    "routes": templates["routes"], "routesNotBuilt": "Every other href in the source points at the original site's routes; the clone serves only '/', so no template exists for them.",
    "counts": counts,
    "entryPoints": {"readme": "README.md", "changelog": "CHANGELOG.md", "pagespecSchema": "schema/pagespec.schema.json", "sectionContractSchema": "schema/section-contract.schema.json",
                    "referenceExample": "schema/example.pagespec.json", "generatedExample": "schema/examples/generated.home.pagespec.json", "semanticValidator": "schema/semantic_validate.py",
                    "adversarialTests": "schema/tests/adversarial_test.py", "templates": "templates/templates.json", "compatibilityGraph": "compatibility/graph.json",
                    "componentAllowlist": "tokens/llm/component-allowlist.json", "tokenCatalog": "tokens/llm/token-catalog.json", "tokenPolicy": "tokens/llm/token-policy.json",
                    "motionPatterns": "tokens/00-foundation/motion-patterns.json", "theme": "tokens/themes/light.json", "assetRoles": "assets/asset-roles.json", "sourceIdentity": "policy/source-identity.json",
                    "designPolicy": "policy/design-policy.json", "measuredValues": "extraction/measured-values.json", "verifyAll": "extraction/verify_all.py", "wrapperGate": "extraction/wrapper_gate.py",
                    "proveDrift": "extraction/prove_drift.py", "policyHash": "extraction/policy_hash.py", "builder": "extraction/build_repo.py", "measureSections": "extraction/measure_sections.mjs",
                    "parityCapture": "extraction/parity/capture.mjs", "parityCompare": "extraction/parity/compare.py"},
    "approval": {"productionApproved": False, "approvedBy": None, "humanDecisions": "extraction/human-decisions.json",
                 "pendingHumanApproval": [t for k, t in [("wrapperGate.whitelist:hero.statement", "wrapper gate whitelist: hero.statement 6300px (extraction/measured-values.json wrapperGate.whitelist)"),
                                                         ("parity.exceptions:story.vr", "parity exception: story.vr below 0.80 (extraction/measured-values.json parity.exceptions)"),
                                                         ("policy/design-policy.json:approval", "design-policy classification (policy/design-policy.json approval)")] if not decision_for(k)],
                 "approvedByOwner": [k for d in HD["decisions"] for k in d["items"]],
                 "productionApprovalNote": "Production approval is a separate human sign-off and has not been given."},
}
dump("registry.manifest.json", manifest)
print("measured-values, policy, manifest ok; policy hash", chash)

# ----------------------------------------------------------------------------------- README generated blocks
def counts_block(c):
    return "\n".join(f"| {k} | {v} |" for k, v in [("Field", "Count"), ("---", "---")] + list(c.items()))


def parity_block(p):
    rows = [("Section", "run1", "run2", "Δ"), ("---", "---", "---", "---")] + [(s, v["run1"], v["run2"], v["absDelta"]) for s, v in p["perSection"].items()]
    rows += [("**average**", p["runs"][0]["average"], p["runs"][1]["average"], "")]
    return "\n".join("| " + " | ".join(map(str, r)) + " |" for r in rows)


def fill(text, tag, body):
    return re.sub(rf"(<!-- {tag}:start -->\n).*?(<!-- {tag}:end -->)", lambda m: m.group(1) + body + "\n" + m.group(2), text, flags=re.S)


rp = os.path.join(REPO, "README.md")
rd = open(rp, encoding="utf-8").read()
rd = fill(fill(rd, "counts", counts_block(counts)), "parity", parity_block(parity))
open(rp, "w", encoding="utf-8").write(rd)
print("README blocks filled")
