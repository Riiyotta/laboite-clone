Source: https://laboiteaslides.fr/

# CLONE_SPEC_B — laboiteaslides.fr FR homepage, BOTTOM HALF (y 20 570 → 35 940 @ 1440x900)

Companion of `CLONE_SPEC_A.md` (top half). Everything global — rem clamp, `superFont/superGrid/superGlass/superDevice` decode, color tokens, the `Button` component + purple hover fill, the background gradient shader (layers 1–10), the `#SYNTHRA` three.js world (camera, renderer, glass triangles, RGB-shift pass), Lenis/GSAP setup, the custom `Timeline` class semantics and the `custom::out` ease — is defined in **CLONE_SPEC_A §0, §1.2, §3.4**. This file only adds what is new below y≈20 570.

Measurement method: computed styles + `getBoundingClientRect` from a headless Chromium (Playwright 1.63, swiftshader WebGL) at 1440x900 and 390x844, scroll-sampled with real wheel events (programmatic `scrollTo` does NOT fire the sticker/Lenis scroll handlers — label cards stay frozen), cross-checked against the original bundles in `reference/nuxt/*.js` and scoped CSS in `reference/original.html`. All motion numbers below are quoted from source and verified against the live probes unless marked otherwise.

---

## 0. Conventions used in this file

- **rem**: `html{font-size:clamp(7px,.6097560976vw,10.2777777778px)}` → **8.78049px at 1440**, 7px at 390. All sizes are given in rem as authored; px in parentheses are at 1440.
- Breakpoints: desktop/`@whole` = `(min-width:768px) and (min-height:435px)`; mobile = `(max-width:767.9px), (max-height:434.9px)`. On mobile **no scroll animations run at all** (every `animations` reactor is `react: e => !isMobile`), the two stickers fall back to `@fit` (`height:fit-content`, no pin) and the WebGL VR scene is not mounted.
- Page wrapper: `main#MAIN.superDevice` → `width:83vw; max-width:1480px; margin-inline:auto; padding-inline:3.2rem; margin-bottom:40rem` → content box x = 150.5, w = 1139 at 1440. `section#HOME` is a plain block inside it.
- `APP-FULL` (`_full_6udqo`): `display:block; flex-shrink:0; width:100vw` plus JS `transform: translateX(-rect.x)` (= −150.5px at 1440, recomputed on LOAD/RESIZE) to bleed to the viewport edges.
- `superPreAccents @step[.1em]` is added to every SplitText line/word wrapper: `padding-block:.1em; margin-block:-.1em` (keeps accents inside the overflow mask). SplitText line wrappers get class `line`, `.line{white-space:nowrap}`; masked lines are wrapped in `div.line-mask` (`position:relative`, overflow clip).
- **Default ease**: GSAP default `power1.out` (`1-(1-t)^2`) applies to every tween below unless an ease is named. Verified live (e.g. VR title y: 100 → 45.6 → 4 → −26 → −44 → −50 at p = 0/.05/.10/.15/.20/.25, exactly power1.out). The string ease `"ease"` used by LabelCards is not a GSAP ease and therefore also resolves to power1.out (verified).
- **"scrub true, default start/end"**: the helper `m(r)` sets `start ??= "0% 90%"`, `end ??= "0% 30%"`, `scrub = true` for every scroll-tween helper that is not on a Timeline. ScrollTrigger notation "A% B%" = trigger point A% of the trigger element meets B% of the viewport.
- Shared text-reveal helpers (`reference/nuxt/B6fTRVdz.js`) referenced below:
  - **WORDS_REVEAL** (export `d`): SplitText `{type:"lines,words", mask:"lines", linesClass:"line", wordsClass:"word"}`; tween `words {y:"130%", scale:1.05} → {y:"0%", scale:1}` **and** `.line>.word {color:#6630ff} → {color:<element's computed color>}`; standalone: `stagger:.07`, scrub, given trigger.
  - **LINES_REVEAL** (export `g`, "in"): SplitText lines (masked); `{y:"130%", scale:.97} → {y:"0%", scale:1}`, stagger .07, scrub.
  - **LINES_SLIDE** (export `c`, "in","y"): SplitText lines (not masked); `{y:20, autoAlpha:0} → {y:0, autoAlpha:1}` (px), stagger .07, scrub.
  - **FADE** (export `s`): `{autoAlpha:0|1} → {autoAlpha:1|0}`, stagger .1, scrub.
  - **BLUR** (export `a`): `{filter:"blur(100px)"} → {filter:"blur(0px)"}` ("in"), scrub.
  - **PARALLAX_Y** (export `u`, n px): `{y:n} → {y:-n}`, ease `"linear"` when standalone (timeline version uses default power1.out).
  - **WORDS_FADE_GREY** (export `v`): SplitText words; `autoAlpha 0→1` then `color #ffffff → #5f5f5f` (gry3).
  - **CARDS_POP** (export `o`): `{y:"25%", scale:.95} → {y:"0%", scale:1}`, `stagger:.1, duration:.7`, `scrub:false, end:undefined, toggleActions:"play none none reverse"` (time-based, plays once on enter, reverses on leave-back).
  - **MASK_WIPE** (export `_`, h, pct): `gsap.set(el,{mask:"linear-gradient(0deg, transparent calc(50% - h/2 px), red calc(50% + h/2 px)) 0% 0% / 100% calc(200% + h px) no-repeat"})` then `maskPosition "0% 100%" → "0% 0%"`, ease none, trigger el, `start "0% pct%"`, `end "100%+=h pct%"`, scrub.

### 0.1 Section map @1440x900 (document y, measured)

| # | Element | y | height | gap after |
|---|---|---|---|---|
| 1 | `section._expertises_jvwcv_46.@whole` | 20 570.5 | 602.3 | 0 |
| 2 | `SECTION._sticker_1b402_46.@native._vr_wukvy_46.@whole` (style `height:600lvh`) | 21 172.7 | 5 400 | 0 |
| 3 | `section._spotlightItem_1bkwk_46._home__spotlightItem_jafgw_46` | 26 572.7 | 627 | 20rem (175.6) |
| 4 | `section._resourceCards_1ahqb_46._home__resourceCards_jafgw_46` | 27 375.4 | 739.1 | 20rem |
| 5 | `SECTION._sticker_1b402_46.@native._labelCards_ya4ut_46._home__labelCards_jafgw_46` (style `height:500lvh`) | 28 290.1 | 4 500 | 20rem |
| 6 | `section._reviewCards_1gm5k_46` | 32 965.7 | 678.2 | 20rem |
| 7 | `app-container[HOME-A1].superGrid@columns[12]@gi[16]` > `section._faq_h699x_46` | 33 819.5 | 728.2 | 40rem (#MAIN margin-bottom) |
| 8 | `footer#FOOTER` | 34 898.9 | 1 041.5 | — (doc height 35 940) |

`#HOME ._home__labelCards, ._home__resourceCards, ._home__reviewCards, ._home__spotlightItem { margin-bottom:20rem }`.

### 0.2 Background shader layers active in this half (see CLONE_SPEC_A §3.4 for the shader)

Layer colors (top/bottom): 7 = BLK `#080808/#080808`, 8 = LGH `#ffffff/#ededed`, 9 = DRK `#120042/#10003d`, 10 = LGH, footer "final" = PRM `#6630ff/#612ef1`. A transition rises the new gradient from the bottom with a domed edge (center higher), dome height = uCurveAmount (starts .3, flattens to 0).

| Layer | Driver | Range (scrollY @900) |
|---|---|---|
| 7 BLK | VR timeline track `.35–.45` `eEnter: uTransition7.value = 1`, `eLeaveBack: = 0` (hard cut, no wipe) | on at 22 748 |
| 8 LGH | VR timeline `uTransition8 0→1` and `uCurveAmount8 .3→0`, ease none, `start:.97, overflowEnd:.7` | 25 538 → 26 303 |
| 9 DRK | ScrollTrigger on `.home__labelCards`, `start "0% 100%"`, `end "0% 0%"`, scrub, ease none, uTransition9 0→1, uCurveAmount9 .3→0 | 27 390 → 28 290 |
| 10 LGH | same trigger, `start "100% 100%"`, `end "100% 0%"`, uTransition10 0→1, uCurveAmount10 .3→0 | 31 890 → 32 790 |
| final PRM | Footer: `uTransitionFinal 0→1`, `uCurveAmountFinal −.05→0`, trigger `#FOOTER`, `start "0% 100%"`, `end "0% 0%"`, scrub (default ease power1.out) | 33 999 → 34 899 |

Net page colour: white through expertises → black during the VR scene → white wipe at the end of VR (spotlight, resources on white) → navy `#120042` wipe while approaching label cards → white wipe as label cards leave (reviews, FAQ on white) → purple `#6630ff` rising under the footer (negative curve −.05 = edge very slightly concave, then flat).

Header colour logic (CLONE_SPEC_A §1.3): VR and LabelCards both broadcast a `light:true` region (their sticker element) to the header while mounted on desktop, and the footer does too → header turns light (white logo, glass buttons) over those three elements.

---

## 1. Expertises — `section._expertises_jvwcv_46.@whole` (y 20 570.5, h 602.3)

### 1.1 DOM (exact text)
```
section._expertises.@whole                       (box-sizing:border-box; no padding on desktop)
  h2._title._expertises__title  "Nos expertises"
     superFont @family[inter] @size[12] @weight[600] @height[15] @align[center] @transform[uppercase]
  app-full (100vw, translateX(-150.5px))
    nav.router._expertises__router superFont @size[164]     (display:flex; flex-direction:column; align-items:center; gap:.4rem)
      ul._list.@content > li._item.@content  (display:contents)  ×5
        a._link._expertises__router-route superFont @color[iht]  href=…   (display:flex; justify-content:center; position:relative; width:100%; overflow:visible)
          app-title._route__label  superFont @family[fkscreamer] @weight[700] @height[75%] @align[center] @transform[uppercase]
          img._route__image  (loading=lazy, srcset; src = large_*)
```
Routes (label → href → image):
1. "Présentations" → `/expertises/presentations-powerpoint` → `/sk/uploads/large_Presentation_e945d6b799.png` (alt "Presentation.png")
2. "Communication 360" → `/expertises/communication-360` → `/sk/uploads/large_Communication_360_7a5ef30bda.png` (alt "Communication-360.png")
3. "Navigation App Like" → `/expertises/navigation-interactive-powerpoint` → `/sk/uploads/large_FDH_URW_navigation_interactive_87d42a0822.jpg` (alt "Un homme cliquant sur la présentation interaction du Forum des halles sur un ipad")
4. "Séminaire VR" → `/expertises/seminaire-realite-virtuelle` → `/sk/uploads/large_Immersion_VR_e950803a61.png` (alt "Immersion-VR.png")
5. "Solutions IA" → `/expertises/solutions-ia-powerpoint` → `/sk/uploads/large_Assistance_IA_LABAS_bot_1963bf7998.jpg` (alt "Bot Assistance IA La boite à slides")
(medium_/small_/thumbnail_ variants of the same names exist in `public/sk/uploads/` for srcset.)

### 1.2 Typography / layout (computed)
- Kicker h2: vInter 600, `font-size:max(1.2rem,12px)` = 12px, `line-height:1.5rem` (13.2px), uppercase, centered, color `#120042`, `margin-bottom:4rem` (35.1px).
- Router font-size 16.4rem (144px). Labels: FKScreamer 700, line-height .75 → 12.3rem (108px), uppercase, centered, color inherit `#120042`. Each row is 108px tall, rows separated by `gap:.4rem` (3.5px). Measured label widths: 599.7 / 831.9 / 795.5 / 518.9 / 523.5 px.
- **Rest state:** `._route__label{opacity:.07}` (near-invisible outline of the words on white).

### 1.3 Hover (pure CSS + random vars)
- `a:hover ._route__label { opacity:1; transition:opacity .2s ease }` (no transition on un-hover → snaps back to .07).
- Image CSS:
  ```css
  ._route__image{position:absolute;top:50%;left:calc(50vw + min(888px,50vw));z-index:-1;
    width:37.7rem;height:25.3rem;object-fit:cover;object-position:center;border-radius:1.6rem;
    transform:translate3d(-100%,-50%,0) rotate(calc(var(--r,0rad)*2)) scale(1.2);opacity:0;
    transition:transform 2s cubic-bezier(.06,.93,.07,.93),opacity .03s}
  a:hover ._route__image{transform:translate3d(calc(-100% + var(--vx)),calc(-50% + var(--vx)),0) rotate(var(--r,0rad)) scale(1);opacity:1}
  ```
  (yes, the original uses `--vx` for both x and y in the hover state; `--vy` is set but unused.) The anchor is 100vw wide, so `left` = 1440px at 1440 → the image hugs the right viewport edge, vertically centred on the hovered row, behind the text (z −1).
- On mount (`onMounted` → `h()`), for every image: `--vx = (Math.random()-.5)*50 + "px"`, `--vy = (Math.random()-.5)*30 + "px"`, `--r = (Math.random()-.5)*Math.PI*.07 + "rad"` (±0.11 rad).
- Net effect: on hover the word goes from 7% to 100% opacity and a photo pops in at the right (opacity snaps in over 30ms) while it settles from 1.2× scale/double rotation to 1× with a very long-tail ease (2s).

### 1.4 Scroll motion
`propTweens.tweens_add("F/T", labels, {y: () => lvh*.17}, {y:0, stagger:.3, scrollTrigger:{trigger: nav.router, start:"0% 83%", end:"100% 83%", scrub:.5}})` — 5 labels, each tween default duration .5 + stagger .3 (total 1.7 units mapped onto the scrub range), default ease power1.out, `scrub:.5` (0.5s catch-up smoothing). Initial y = 0.17 × 900 = 153px (measured `matrix(1,0,0,1,0,153)`). Range at 900: scrollY 20 449 → 21 003.

### 1.5 Mobile (390)
Non-`@whole`: section `padding-block:20rem` (140px), router `@size[96]` (9.6rem = 67.2px), labels `line-height:80%` (53.8px rows), gap .4rem (2.8px), images `display:none`, labels opacity **1** (the `.07` rule is scoped to `.@whole`; measured opacity 1 on mobile), no scroll motion.

---

## 2. VR sticker — "DÉPASSEZ TOUTES LES LIMITES DE POWERPOINT" (y 21 172.7, h 5 400 = 600lvh)

### 2.1 DOM (exact text)
```
SECTION._sticker_1b402_46.@native._vr_wukvy_46.@whole   style="height:600lvh"   (position:relative; pointer-events:none)
  app-container[STICKER-A1].@wrapper._sticker__track._vr__track
        (position:sticky; top:0; height:100lvh; overflow:hidden; display:flex; justify-content:center; padding-top:15.2rem; width:100%; box-sizing:border-box; children pointer-events:auto)
    h2._vr__track-title superFont @family[fkscreamer] @size[112] @weight[700] @height[80%] @align[center] @transform[uppercase]
        "Dépassez toutes les " <strong class="superFont @color[prm1]">limites de PowerPoint</strong>
        (width:65rem; max-width:100%; word-break:break-word; color inherits #120042)
    app-container[VR-A1]  (position:absolute; top:50%; left:50%; transform:translate3d(0,-50%,0); display:block; width:100%)
      p._vr__track-content superFont @color[gry3] @family[inter] @size[52] @weight[600] @space[-.04em] @height[104%]
        "Une expérience aussi bluffante, vous n’êtes pas prêt de l’oublier. Votre public non plus."
        (width:60.9rem; max-width:100%; margin-bottom:3.2rem; left-aligned)
      a._cta._vr__track-cta  href="/expertises/conferences-interactives"   (UIActionCTA, design "light")
        APP-BUTTON @round @hover @left @lgh @color[drk1] (5.6rem circle, white) > arrow icon
        APP-BUTTON @hover @bottom @lgh @color[drk1] > span "En savoir plus"
  iframe._iframe (intersection/resize sensor, hidden)
```
The DOM sits on top of the WebGL canvas (`canvas#SYNTHRA` fixed, z −1); everything visual besides the text is WebGL.

### 2.2 Typography (computed @1440)
- Title: FKScreamer 700, 11.2rem (98.3px), lh .8 (78.7px), uppercase, centered; 3 lines at 570.7px width ("DÉPASSEZ TOUTES / LES LIMITES DE / POWERPOINT"); `strong` `#6630ff`, rest `#120042`. Title top at 133.5px (15.2rem) inside the pinned track.
- Content: vInter 600, 5.2rem (45.7px), line-height 1.04 (47.5px), letter-spacing −.04em (−1.83px), color `#5f5f5f` (gry3) at rest; box starts at x = 720 (viewport centre), width 534.7px, vertically centred (top 50%, −50%).
- CTA buttons: height 5.6rem (49.2px), radius 2.4rem, circle 5.6rem; text vInter 1.5rem/500/lh 1.4, `#120042` on `#fff`; text button `padding-inline:3.2rem`; arrow icon 1.6rem (14px) (`<svg viewBox="0 0 17 17"><path d="M6.26469 4.13384L10.1749 8.22174L6.08703 12.1319" stroke="currentColor" stroke-miterlimit="16" stroke-linecap="round" stroke-linejoin="round"/></svg>`). The two buttons sit side by side with 0 gap (measured x 720 and 769.2).

### 2.3 Timeline (`VR`, custom Timeline class — CLONE_SPEC_A §0.4)
`propTimeline.update({name:"VR", trigger: sticker, getOverflowStart:()=>lvh, getOverflowEnd:()=>lvh, scrub:true})`
⇒ ScrollTrigger start `"0%-=900 0"`, end `"100%+=900 900"` ⇒ scrollY **20 272.7 → 26 572.7** (T = 6 300; s = c = 900/6300 = .1429, o = 4500/6300 = .7143).
Mapping: timeline position p ∈ [0,1] ↔ **scrollY = 21 172.7 + 4 500·p** (the pinned range). `overflowStart:k` pulls a start k·900px earlier; `overflowEnd:k` pushes an end k·900px later (into the un-pin phase).

DOM tweens (all default ease power1.out; "words" = SplitText words of the title, 7 words; "lines" = 3 masked lines):

| What | Tween | Timeline range (p) | scrollY @900 |
|---|---|---|---|
| Title words | WORDS_REVEAL: `y 130%→0%, scale 1.05→1, color #6630ff→computed (#120042 / strong #6630ff)` | start 0, end .17, stagger .013 | 21 173 → 21 938 |
| Title lines (reversed order: last line first) | FADE out `autoAlpha 1→0` | .17 → .25, stagger .013 | 21 938 → 22 298 |
| Title block | `y:100 → y:-50` (px) | 0 → .25 | 21 173 → 22 298 |
| Content words | WORDS_FADE_GREY: `autoAlpha 0→1` stagger .005; then `color #fff→#5f5f5f` stagger .005 | .63 → .83 ; colour .73 → .85 | 24 008 → 24 908 ; 24 458 → 25 003 |
| CTA | PARALLAX `y 5→-5` px | .70 → 1 | 24 323 → 25 673 |
| CTA | FADE in | .70 → .85 | 24 323 → 24 998 |
| Content `<p>` | FADE out | .90 → .99 | 25 223 → 25 628 |
| `[VR-A1]` container | FADE out | .91 → 1 | 25 268 → 25 673 |

Live probes (wheel-scrolled): p .05 → title y 45.6, first word scale 1.0135 / color rgb(53,20,146); p .10 → y 4; p .20 → lines fading; p .25 → title `visibility:hidden`; p .65 → 4/14 content words visible; p .70 → all words visible, CTA opacity .04; p .745 → first word rgb(180,180,180); p .80 → CTA y −.56 / opacity .89; p .945 → A1 opacity .381; p ≥ 1 → A1 opacity 0 (content gone before the section un-pins).

**Auto-scroll snap**: the track `{start:.25, end:.6}` has `eEnter → if natural scroll: Lenis.scrollTo(V.getTop(.65), 150)` and `eEnterBack → Lenis.scrollTo(V.getTop(.2), 200)` (`$Scroll.__scroll_toMotion(top, 150|200)`), i.e. entering the headset zone going down auto-scrolls to p .65 (scrollY 24 098); entering it going up auto-scrolls back to p .2 (22 073). (In headless wheel tests the snap did not visibly fire; implement per source.)

### 2.4 WebGL — what is on screen (verified by screenshots)
| p | Screen |
|---|---|
| < 0 | White background, glass triangles leaving (from skills section) |
| 0 → .25 | Title reveals on white; a VR headset (GLB) rises from below and swings up toward the camera; the RGB-shift post pass starts at .25 |
| .25 → .6 | Headset flies into/through the camera (we pass through the lens hole); background hard-cuts to near-black `#080808` at .35; lens meshes and glass visor fade out (.35–.45); headset hidden at .6 |
| .4 → .71 | A sphere of 80 project thumbnails (Fibonacci sphere) scales up from 0 and swings in from the right, ending centred, slowly spinning |
| .5 → .9 | Each thumbnail pushes radially outward to 1.7× radius → camera ends up inside the sphere, thumbnails all around |
| .65 → 1 | A black full-screen plane in front of the camera darkens the images (opacity 0→.5 at .65–.7, .5→1 at .8–.9) behind the content text; sphere hidden at .9; plane fades 1→0 at .9–1 (black bg remains) |
| .97 → 1+.7 | White background (layer 8) wipes up from the bottom with a dome edge (scrollY 25 538 → 26 303), over which the spotlight section scrolls in |

### 2.5 WebGL recipe (source: `DqzInzYb.js` index component + `BYyf5AQZ.js` data + `Co2d9rFw.js` plugins)
All objects live in the shared `#SYNTHRA` scene/camera (CLONE_SPEC_A §3.4). Timeline `V` (= the VR timeline above) drives "tracks" `{start,end,overflowStart,overflowEnd,eUpdate(progress)}`; inside a track `progress` is linear 0→1 across its range, easing is applied manually where noted.

**Camera** (looks at origin every update): already at `p7 = [-20,0,0]` (set by the skills timeline); VR track `{start:.99,end:1}`: lerp `p7 → p8 = [0,0,1]` (linear).

**VR headset** — GLB `/assets/models/DECIMATE v2_compressed-compressed.glb` (DRACO, decoder path `/draco/gltf/`, `type:"wasm"`), all `scene.children` added to group `VR_MASK_3D`. Meshes named `Object_183`, `Object_181`, `Object_157` (lenses) get `transparent:true` and are faded; mesh `Object_195` (visor) gets a replacement `MeshPhysicalMaterial({color:0xffffff, metalness:0, roughness:.1, transparent:true, transmission:1, ior:2, thickness:.5, specularIntensity:1, envMap:<scene env>, envMapIntensity:1, clearcoat:1, clearcoatRoughness:.1, depthWrite:false, side:DoubleSide})`.
Initial: position `p0 [17,-38,0]`, rotation `r0 [0,0,π/2-.3]`, scale `s0 [50,50,50]`, `visible=false`.
| Track (p) | Update |
|---|---|
| 0 → .15 | visible on enter / hidden on leave-back; position p0→p1 `[17,-27,0]`, rotation r0→r1 `[0,0,π/2-.5]` (linear) |
| .13 → .25 | position p1→p2 `[-11.24,-2.43,4.3]`, rotation r1→r2 `[0,0,0]` |
| .25 → .6 | RGB-shift uniform `amount = .00128 + sin(π·(1-(1-n)^1.7))/30`; headset hidden on leave (.6), re-shown on enter-back; auto-scroll snap (§2.3) |
| .25 → .35 | position p2→p3 `[-26.5,-1.7,4.8]` |
| .35 → .45 | on enter `uTransition7 = 1` (BLK bg; 0 on leave-back); position p3→p4 `[-30,-1.5,5]`; lens meshes opacity `1 - n²`; visor opacity `(1-n)^5` |
| .45 → .6 | position p4→p5 `[-40,-1.7,5.2]` |

**Image sphere** (`SPHERE` plugin): 80 planes (`__LENGTH = 80`), each `PlaneGeometry(3, 1.6875, 5, 3)` (16:9) with vertex z bulge `z = sqrt(x²+y²)*.1`, `MeshStandardMaterial({side:DoubleSide, depthWrite:true})` (cloned per plane). Placement (golden-angle sphere, radius 10): for i in 0..79: `y' = 1 - i/79*2; r = sqrt(1-y'²); θ = π(3-√5)·i; pos = [cos θ·r·10, y'·10, sin θ·r·10]`, rotation = lookAt(outward normal) with up (0,1,0). Textures: the 61 `small_*` images listed in §9.2, loaded with `TextureLoader`, `colorSpace = SRGBColorSpace`, `wrapS/wrapT = RepeatWrapping`; plane i gets texture `i % 61`.
Group initial: position `[85.8,0,.475]`, rotation `[0,0,0]`, scale `[0,0,0]`, hidden.
| Track (p) | Update |
|---|---|
| .4 → .6 | enter: show + start spin; leave-back: hide + stop spin. scale 0→1 with `i = 1-(1-n)²` |
| .4 → .71 | position → `[-10,0,0]`, rotation → `[0,-π,0]`, both with `i = 1-(1-n)²` |
| .5 → .9 | every plane position lerps from its sphere point P to 1.7·P with `o = n²`; enter-back: show+spin, leave: hide+stop |
| spin | while shown, every frame `rotationY_extra = dt -= delta*.1` (−0.1 rad/s, accumulates) |

**Darkening plane** (`MASK` plugin): `PlaneGeometry(1,1)` + `MeshBasicMaterial({color:#080808, opacity:0, transparent:true, depthWrite:false, depthTest:false})`, child of the camera at z −1, scaled to fill the viewport, renderOrder 2. Tracks: `.65–.7` enter→visible, opacity `= n*.5`; `.8–.9` opacity `.5 + n*.5`; `.9–1` opacity `1 - n`, hidden on leave.

**Clone guidance**: the sphere + darkening + background cuts are straightforward three.js; the headset needs the GLB (present at `public/assets/models/DECIMATE v2_compressed-compressed.glb`) and DRACO decoder files (`/draco/gltf/` — check they exist in `public/`; if not, use three's `examples/jsm/libs/draco/gltf/`). Exact lighting/env/RGB-shift come from the shared scene (Spec A).

### 2.6 Mobile (390)
`@fit` non-whole variant, no WebGL: section `display:flex; justify-content:center; align-items:center; margin:0 -2rem 20rem; background:#120042; padding-inline:2rem (superDevice)`; track `max-width:93rem; padding-block:15.2rem` (106.4px) column centred; title `@color[lgh1]` (white) FKScreamer 11.2rem (78.4px) lh .8, centred, strong `#6630ff`, `margin-bottom:3.2rem`; content `@color[lgh1] @size[40] @weight[500]` (4rem = 28px, lh 1.04, ls −.04em = −1.12px) **centred**, margin-bottom 3.2rem; CTA centred. Measured section height 635px.

---

## 3. Spotlight — "TOUJOURS CARRÉS. JAMAIS FORMATÉS." (y 26 572.7, h 627)

### 3.1 DOM
```
section._spotlightItem_1bkwk_46._home__spotlightItem   (display:flex; margin-bottom:20rem)
  app-container[SPOTLIGHT_ITEM-A1] superFont @align[center]
      (display:flex; flex-direction:column; justify-content:center; align-items:center; flex:1; max-width:50%; min-height:70.1rem; padding:8rem; box-sizing:border-box; text-align:center)
    app-icon._icon @size[5]._spotlightItem__icon superFont @color[trt3]   (svg height 4.8rem; margin-bottom:3.2rem; color #70f74a)
       <svg class="triangleMirror" viewBox="0 0 32 32" fill="currentColor"><path d="M32 16L16 6.99382e-07L16 16L32 16Z"/><path d="M16 16L3.49691e-06 16L16 32L16 16Z"/></svg>
    h2._spotlightItem__title superFont @family[fkscreamer] @size[112] @weight[700] @height[80%] @transform[uppercase]
       "Toujours carrés. " <strong class="superFont @color[prm1]">Jamais formatés.</strong>     (width:100%; margin-bottom:2.4rem)
    p._spotlightItem__content superFont @family[inter] @size[15] @weight[500] @height[140%]   (padding-inline:2.4rem)
       "Une équipe de spécialistes qui réunit sans concession une culture de la réflexion et le goût de l’inattendu. Ça donne la première agence Powerpoint en France."
    a._cta._spotlightItem__cta  href="/nous-connaitre"   (margin-top:4rem; design darkGlass)
       round button (superGlass @blur[24] @background[drk]) + text button "Nous connaître"
  img._spotlightItem__image  src=/sk/uploads/large_Labas_20f4ebe642.jpg  alt="logo la boite à slides"
      (flex:1; max-width:50%; min-height:70.1rem; height:100%; align-self:center; object-fit:cover; object-position:center; border-radius:1.6rem)
```
### 3.2 Computed @1440
- A1 column 569.5 × 627, padding 8rem (70.2px). Icon 42.1px square at top (y +70). Title 98.3px/lh 78.7px, 3 lines "TOUJOURS / CARRÉS. JAMAIS / FORMATÉS." (429px wide), color `#120042` + strong `#6630ff`. Paragraph vInter 1.5rem (13.2px)/500/lh 2.1rem (18.4px), `#120042`, 412px wide. CTA top margin 35.1px.
- Image: x 720, w 569.5, h 615.5 (70.1rem), radius 14px.
- darkGlass buttons: `background:#12004212; backdrop-filter:blur(24px)`; text `#120042`.
### 3.3 Motion (ScrollTrigger tweens, trigger = section, scrub true)
| Target | Helper | start → end |
|---|---|---|
| title | WORDS_REVEAL (stagger .07) | `"0% 50%"` → `"0% 0%"` |
| icon | BLUR in (100px → 0) | `"0% 50%"` → `"0% 10%"` |
| paragraph | LINES_SLIDE in (y 20→0, autoAlpha 0→1, stagger .07) | `"0% 40%"` → `"0% 0%"` |
| CTA | FADE in | `"0% 30%"` → `"0% -10%"` |
| image | PARALLAX_Y 300 (y 300px → −300px, ease linear) | `"0% 100%"` → `"100% 0%"` |
### 3.4 Mobile
`.@column`: `flex-direction:column`; A1 `max-width:100%; min-height:0; margin-bottom:5.6rem; padding:0`; image `width:100%; max-width:100%; min-height:0`; title 11.2rem (78.4px) on 2 lines + strong.

---

## 4. Resource cards — "NOS DERNIÈRES RESSOURCES" (y 27 375.4, h 739.1)

### 4.1 DOM
```
section._resourceCards_1ahqb_46._home__resourceCards
  header._resourceCards__header  (display:flex; flex-direction:column; align-items:center; gap:1.6rem; width:52.4rem; max-width:100%; margin-inline:auto; margin-bottom:5.6rem)
    h2 superFont @family[fkscreamer] @size[112] @weight[700] @height[80%] @align[center] @transform[uppercase]
       "Nos dernières " <strong @color[prm1]>ressources</strong>
    a._cta href="/ressources"  darkGlass  "Voir toutes nos ressources"
  nav.router._resourceCards_g3l72_46 superGrid @columns[3] @gb[16] @gi[16]   (grid 3×1fr, gap 1.6rem)
    a._resourceCard.@article.@background[drk] superFont @color[lgh1]  href="/ressources/gamification-et-powerpoint-mettez-du-jeu-dans-vos-formations"
       app-tag "Article"; time datetime=2025-01-12 "12/01/2025"; h3 "Gamification et PowerPoint : mettez du jeu dans vos formations !"
    a._resourceCard.@client  href="/ressources/ideuzo-presentation-commerciale"
       app-tag "Cas client"; time "18/03/2026"; h3 "Ideuzo- Présentation commerciale"; img /sk/uploads/large_presentation_equipe_0eebf6541e.jpeg alt "équipe qui applaudit"
    a._resourceCard.@whitePaper  href="/ressources/gagner-en-autonomie-sur-powerpoint"
       app-tag @color[drk1] "Livre blanc"; time @color[drk1] "27/01/2026"; app-white-paper > h3 "Gagner en autonomie sur PowerPoint"
```
### 4.2 Styles (desktop)
- Header title: 11.2rem/lh .8, 2 lines (394.6px wide) "NOS DERNIÈRES / RESSOURCES"; CTA below (gap 1.6rem).
- Grid columns 370.3px, gap 14.05px.
- Card: `display:flex; flex-direction:column; align-items:center; min-width:0; aspect-ratio:448/556; padding:3.2rem 3.2rem 3.2rem; box-sizing:border-box; border-radius:3.2rem` (measured 370.3 × 459.6). Article: `background:#120042` (articles alternate drk/prm: 1st `#120042`, 2nd `#6630ff`). Client: `background:#120042; position:relative; z-index:1; overflow:hidden`, `::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,#00000073,#00000073)}`, img absolute inset 0, 100%×100%, z −2, cover. White paper: `background:#12004212; padding-inline:2.8rem; padding-bottom:0; overflow:hidden`.
- Tag (`app-tag._tag_1er0k`): `width:fit-content; height:4rem; display:flex; align-items:center; gap:.8rem; padding-inline:1.6rem; border:max(.1rem,1px) solid; border-radius:1.6rem; white-space:nowrap`; vInter 1.5rem/500/lh 1.4; `@color[lgh1]` → text #fff, border `#fff3`; `@color[drk1]` → text #120042, border `#12004212`. `margin-bottom:3.2rem`.
- Date: vInter 1.5rem/500/lh 1.4, `margin-bottom:1.6rem` (white paper: 4rem).
- Card title: FKScreamer 700, 6.4rem (56.2px), lh .85 (47.8px), uppercase, centred, `flex:1; width:100%; display:-webkit-box; -webkit-line-clamp:7; overflow:hidden`.
- White paper mockup (`app-white-paper`, flex:1, width 100%): A1 `position:relative; z-index:1; width:100%; transform:rotate(3.13deg); aspect-ratio:390.93/418.47; filter:drop-shadow(10.346px 20.692px 31.038px rgba(0,0,0,.12))`; A1 `::before` white sheet `position:absolute; top:5.65%; left:4.56%; z-index:-1; width:93.29%; aspect-ratio:364.7/445.61; transform:rotate(2.2deg); background:#fff; border-radius:2.13%`; B1 cover `position:relative; z-index:1; width:93.29%; aspect-ratio:364.7/476.52; padding:7.95%; overflow:hidden; border-radius:2.13%; background:#6630ff url(/assets/images/whitePaper/2.png) 50%/cover no-repeat`; cover h3 FKScreamer 5.2rem (45.7px)/700/lh .9/uppercase/#fff, left-aligned. The sheet is cropped by the card's bottom edge.
### 4.3 Motion
- Title: WORDS_REVEAL, trigger section, default `"0% 90%" → "0% 30%"` scrub.
- Header CTA: FADE in, trigger section, `"0% 50%" → "0% 20%"`.
- Cards: CARDS_POP (`y 25%→0, scale .95→1, stagger .1, duration .7`, power1.out), trigger = grid nav, `start "0 100%"`, toggleActions `play none none reverse` (measured initial `matrix(.95,0,0,.95,0,114.9)`).
### 4.4 Mobile
Grid `@columns[2] @gb[8] @gi[8]` (gap .8rem = 5.6px; 2 cols of 178.2px; 3rd card wraps to row 2). Card `border-radius:1.6rem; padding:3.2rem 1.6rem 1.6rem` (white paper `padding-inline:1.6rem`), category margin-bottom 1.6rem, card title `@size[40]` (4rem = 28px, lh .85), white-paper title `@size[32]`.

---

## 5. Label cards sticker — "ENGAGÉS POUR LA QUALITÉ" (y 28 290.1, h 4 500 = 500lvh)

### 5.1 DOM
```
SECTION._sticker_1b402_46.@native._labelCards_ya4ut_46._home__labelCards   style="height:500lvh"   (margin-bottom:20rem)
  APP-FULL._full._sticker__track._labelCards__track superFont @color[lgh1]
     (position:sticky; top:0; height:100lvh; overflow:hidden; width:100vw; translateX(-150.5px);
      display:flex; justify-content:center; align-items:center; padding-block:20rem; box-sizing:border-box; color:#fff)
    h2._labelCards__title.@block superFont @family[fkscreamer] @size[252] @weight[700] @height[75%] @align[center] @transform[uppercase]
       "Engagés pour " <strong class="superFont @color[prm1]">la qualité</strong>     (strong display:block)
    ul._list.@content > li.@content ×3 >
      section._labelCard_1gue8_46.superGlass.@blur[90].@background[lgh]._list__labelCard   (position:absolute; left:100%)
        h3._labelCard__title.@block superFont @family[fkscreamer] @size[40] @weight[700] @height[90%] @align[center] @transform[uppercase]
        img._labelCard__image  (20rem × 20rem, object-fit:contain)
        app-container[LABEL_CARD-A1].@wrapper > app-tag (lgh1)
```
Cards (title / image / tag):
1. "5 étoiles Google Avis" / `/sk/uploads/Badge_Google_avis_labas_149fc344c9.png` (alt "illustration du badge 5 étoiles avis google") / "Notation 2026"
2. "Certifié ISO 9001:2015 Bureau Veritas" (U+2028 line separator → renders as a line break after "Certifié") / `/sk/uploads/Badge_ISO_9001_labas_49c6d38cef.png` / "Certification 2025"
3. "Microsoft Office Specialist" / `/sk/uploads/Badge_MOS_labas_83992cf13f.png` / "Depuis 2020"
(`thumbnail_Badge_*` variants exist; the `Logo_simple_*`/`Badge_simple_MOS_*` SVGs are used by the FOOTER, not here.)

### 5.2 Styles (desktop)
- Title: FKScreamer 700, 25.2rem (221.3px), lh .75 (166px), uppercase, centred, white; strong `#6630ff` on its own line → "ENGAGÉS POUR / LA QUALITÉ", block 876.8 × 354px centred in the viewport.
- Card: `display:flex; flex-direction:column; align-items:center; gap:.8rem; padding:7.8rem 7.5rem 4rem; box-sizing:border-box; aspect-ratio:448/498; width:44.8rem (393.4px); border-radius:3.2rem; background:#ffffff1a; backdrop-filter:blur(90px)`. Card title FKScreamer 4rem (35.1px)/lh .9 (31.6px)/uppercase/centred/white. Image 20rem square (175.6px). `[LABEL_CARD-A1]{display:flex; flex:1; align-items:flex-end}` → tag pinned to the card bottom. Tag as §4.2 (white, border `#fff3`).
- Background behind = navy layer 9 (`#120042` → `#10003d` gradient with noise/vignette), so the blurred glass reads as a lighter violet panel catching the purple "LA QUALITÉ" through the blur.

### 5.3 Motion
**Sticker scroll value** (component `Sticker`, `ChMElkfr.js`): on every Lenis SCROLL while the sticker intersects the viewport:
`e = (clamp(scrollY, top - lvh, top + H) - top) / (H - lvh)` with top = 28 290.1, H = 4 500 ⇒ `e = (scrollY - 28 290.1)/3 600`, clamped to [−.25, 1.25].
(`propFragCount:3, propFragHeight:300, propFragGap:100/300` ⇒ height = 300 + 300·(1/3)·2 = **500lvh**, `t = 300/500 = .6`.)

**Cards** (`LabelCards.ae(e, t=.6)`), per card r = 0,1,2:
```
e' = (e - .17) / .83
a  = (e' - 100*r/500) / .6            // = (e' - .2r)/.6, NOT clamped (extrapolates)
E  = innerWidth + firstCard.getBoundingClientRect().width   // measured once on LOAD/resize, with its current transform (≈ 1440 + ~470 = ~1910 at 1440)
T  = E * (lvh / innerWidth)
x  = -( E * (1.5*a*(1-a) + a**3) )                   // cubic Bezier x: 0, .5E, .5E, E
y  = .1*T * ((1-a)**3 + a**3) + rnd_r                 // cubic Bezier y: .1T, 0, 0, .1T ; rnd_r = Math.random()*100-50 (px, per card, fixed)
c  = cos(i_r)                                          // i_r = Math.random()*-.1 - .05  (rad, per card, fixed)
s  = lerp(sin(i_r), sin(-i_r), a)                      // = sin(i_r)*(1-2a)
el.style.transform = matrix3d(c, -s, 0, 0,  s, c, 0, 0,  0, 0, 1, 0,  x, y, 0, 1)
```
Cards start at `left:100%` of the 100vw track (just off the right edge), vertically centred (flex static position), and sweep left along a shallow U-curve (high at both ends, lowest mid-screen), rotating from ≈ +|i| clockwise to −|i| (|i| ∈ [.05,.15] rad); because cos/sin are linearly lerped, values outside a∈[0,1] also skew/scale slightly. Card r is delayed by .2 in e' (= 720px of scroll). Probe (x of card left edge in viewport): e .29 → 868 / 1689 / 3240; e .51 → 197 / 695 / 1360; e .71 → −724 / 103 / 613; e 1.0 → −4254 / −1836 / −491. Card 0 crosses the viewport centre at e ≈ .45 (scrollY ≈ 29 910); the last card leaves the left edge at e ≈ 1.1.

**Title** (ScrollTriggers, trigger = sticker):
- PARALLAX_Y 50: `y 50 → -50` px, `start "0% 100%"`, `end "100% 0%"` (27 390 → 32 790), scrub, power1.out (verified: y 35.9 at 27 785; −1 at 29 010; −47.2 at 31 890).
- LINES_REVEAL in: `y 130%→0%, scale .97→1`, stagger .07, `start "0% 0%"`, `end "0% -100%"` (28 290 → 29 190), scrub (verified: lines at 0 by 29 348).
So the title is hidden (masked) while the navy wipe comes up (27 390 → 28 290), then rises in during the first 900px of pin, then cards fly across it.

### 5.4 Mobile
`@fit` (no pin): track `flex-direction:column; gap:1.6rem; background:#120042; padding-block:20rem`; title `@size[112] @height[80%]` (78.4px, lh 62.7), `max-width:93rem; margin-inline:auto; margin-bottom:4rem`; list `superGrid @columns[2] (3 if crushed) @margin[mobile] @gb[16] @gi[16]`, `overflow:hidden; width:100%`; cards static in grid (175.4px wide), `justify-content:space-between; padding:7.8rem 1.6rem 4rem; border-radius:2.4rem`, image 13.2rem square (92.4px), card title strong `@size[96]`.

---

## 6. Review cards — "ILS NOUS FONT CONFIANCE" (y 32 965.7, h 678.2)

### 6.1 DOM
```
section._reviewCards_1gm5k_46 superFont @color[drk1]._home__reviewCards
    (display:grid; grid-template-columns:1fr auto auto; grid-template-rows:auto 1fr auto; gap:5.6rem 1.6rem; overflow:visible)
  h2._reviewCards__title superFont @family[fkscreamer] @size[112] @weight[700] @height[80%] @transform[uppercase]
     "Ils nous font " <strong @color[prm1]>confiance</strong>       (grid-row:1; grid-column:1; max-width:53.3rem when viewport height ≥ 850px; left-aligned)
  app-swiper._swiper.@content (display:contents)
    nav._swiper__nav.@start._reviewCards__nav   (grid-row:1; grid-column:2; align-self:flex-end; display:flex; gap:.8rem)
      BUTTON @round @hover @right darkGlass ._swiper__nav-stepper.@prev  (arrow @rotate[180])
      BUTTON @round @hover @left  darkGlass ._swiper__nav-stepper.@next  (arrow @rotate[0])
    SWIPER-TRACK._swiper__track._reviewCards__track
        (grid-column:1/4; grid-row:2; display:flex; flex-wrap:nowrap; gap:1.6rem; width:100%; height:47rem; max-height:47rem; min-height:0; z-index:0; transform:scale(1))
      ul.@content > li.@content > article._reviewCard.superGlass.@blur[24].@background[drk]  ×7
```
No CTA is rendered on the home page (no `reviewCards.CTA` in data).
`.@start` nav: `.@prev{opacity:.2; pointer-events:none}`; `.@end` → `.@next` same. `.@off` (during inertia throw) → nav `pointer-events:none`.

Review card markup:
```
article#<documentId>._reviewCard   (width:42.4rem; height:100%; flex-shrink:0; display:flex; flex-direction:column; justify-content:space-between; gap:5.6rem; padding:3.2rem; border-radius:2.4rem; background:#12004212; backdrop-filter:blur(24px); box-sizing:border-box)
  header._reviewCard__header superFont @family[inter] @weight[500] @height[140%]   (display:grid; grid-template-columns:auto 1fr; grid-template-rows:auto auto; gap:0 1.2rem)
    img._reviewCard__header-image (5.6rem square; grid-column:1; grid-row:1/3; background:#fff; border-radius:2rem; object-fit:cover)
    h3._reviewCard__header-title superFont @size[15]   (grid-row:1; align-self:flex-end)   — 1.5rem/500/lh 1.4
    p._reviewCard__header-role superFont @size[12]      (grid-row:2)                         — max(1.2rem,12px)/500/lh 1.4
  p._reviewCard__content superFont @size[18]   (overflow:hidden)  — vInter 1.8rem (15.8px), weight 400, line-height normal, color #120042
     text = ` “${content}” ` (curly quotes added by the component; newlines in content are preserved as spaces in HTML)
```
Cards (logo → name → role → quote):
1. `/sk/uploads/thumbnail_logo_Caterpillar_c129772a64.png` — "Teddy G." — "Product Consultant" — “Merci beaucoup ! Super boulot de votre part ! Vous pouvez être fiers du travail accompli car le défi était loin d'être facile par rapport aux autres toolkits ! Bravo !”
2. `/sk/uploads/thumbnail_logo_safran_2088913497.png` — "Marion T." — "SVP Performance & Transformation" — “Merci encore pour le travail de grande qualité, tant sur la forme que sur le fond, que vous avez apporté sur nos slides à l'occasion de notre journée transformation digitale chez SED. La journée a été un succès, et le professionnalisme de la présentation a été particulièrement salué. Un grand merci à toute l'équipe chez vous qui a travaillé sur ces slides.”
3. `/sk/uploads/thumbnail_logo_essilor_4f286cb915.png` — "Julie N." — "Directrice de la communication" — “Merci pour la qualité de ce travail (...) félicites les équipes pour le superbe job réalisé. L'enchaînement des animations est encore plus réussi que l'an passé et rend le bilan plus fluide et dynamique. Je suis très contente. Je ne suis jamais déçue avec La boite à slides ! Merci c'est bon de pouvoir compter sur vous !”
4. `/sk/uploads/thumbnail_logo_bostik_5b01f5c5a7.png` — "Alexandra V" — "Global Marketing & Communication Manager" — “Merci beaucoup, c'est top comme d'habitude. L'équipe américaine et l’Europe veulent déjà s'en servir sur d’autres activités ! Le look and feel a servi de base pour tous nos supports. Ca level up vraiment l'ensemble du marketing et de la com sur cette activité. Ce n'est pas uniquement des slides pour une présentation donnée, ça rayonne sur plein d'autres choses, donc merci ! Cela confirme ce que je dis souvent aux personnes qui ne voient que le prix par slide ou à la prestation, c'est qu'on ne paye pas que des slides.” (overflows; clipped by `overflow:hidden` on the content p, card height fixed)
5. `/sk/uploads/thumbnail_logo_vaudoise_8647c5fc66.png` — "Andres A." — "Directeur Prévoyance et Assurances de Personnes" — “Suite à notre événement "feuille de match PAP 2026", vos slides ont rajouté un bel effet de surprise et des « woooaaahhh trop cool » ! (...) Un immense MERCI pour tout votre travail et votre créativité !”
6. `/sk/uploads/thumbnail_Syngenta_43c016de86.png` — "Christian L." — "Head Global Supply Chain Management Disease Control" — “I just wanted to thank you for the excellent job you did on those slides. I really like the design you came up with and the slides worked very well during the webinar yesterday. Great job and very well appreciated from our side.”
7. `/sk/uploads/thumbnail_Nestle_waters_8a22365e28.jpg` — "Eva M." — "Global Brand Manager SAN PELLEGRINO" — “Je jump pour te remercier pour la prez. C'est canon ! Et les quelques personnes qui l'ont vu nous ont félicité donc bravo à la team”

### 6.2 Computed @1440
Title 2 lines (468px wide) "ILS NOUS FONT / CONFIANCE" at x 150.5. Nav at x 1170.1 (2 × 49.2px buttons, gap 7px), bottom-aligned with the title. Track y = title bottom + 5.6rem, 1139px wide, 412.7px (47rem) tall; cards 372.3 × 412.7, gap 14px → cards 1–3 fully visible, card 4 cut by the viewport edge (track is `overflow:visible`; the page clips at 100vw). Content paragraphs sit at the card bottom (space-between).

### 6.3 Behaviour (component `Swiper`, `CfSd5rt5.js`)
- GSAP `Draggable.create(track, {type:"x", inertia:true, bounds:{minX: -(track.scrollWidth - track.offsetWidth), maxX:0}, edgeResistance:.7, onDrag/onThrowUpdate: update index & @start/@end, onDragStart: kill step tween, onDragEnd: nav @off until throw complete})`.
- Snap points = each slide's `offsetLeft` (capped at max scroll; last reachable index F).
- Prev/next click: `gsap.to(track, {x: -offsetLeft[index±1], duration:.7, ease:"power2.out"})`, ignored while a throw is in progress.
- Nav state classes: `@start` when x ≥ 0, `@end` when x ≤ −max, both → prev/next at opacity .2.
- Button hover: CLONE_SPEC_A §1.2 (`@right` = fill sweeps from the left, `@left` from the right).
### 6.4 Motion
- Title: WORDS_REVEAL, trigger section, default `"0% 90%" → "0% 30%"`.
- Cards: CARDS_POP (`y 25%→0, scale .95→1, stagger .1, duration .7`), trigger = track, `start "0% 100%"`, toggleActions play/reverse.
### 6.5 Mobile
Section gets `superDevice` (100vw, padding-inline 2rem) and `margin-inline:-2rem; overflow:hidden`; grid rows `auto auto 1fr auto`, gap `3.2rem 1.6rem`; title row 1 full width; nav row 2 (right); track row 3; card width 42.4rem (296.8px), padding 3.2rem (22.4px), radius 2.4rem; role `@size[12]` = 12px (lh 16.8).

---

## 7. FAQ — "DES QUESTIONS? ON VOUS RÉPOND" (y 33 819.5, h 728.2)

### 7.1 DOM
```
app-container[HOME-A1].@wrapper superGrid @columns[12] @gi[16]          (12 cols × 82px, col-gap 14.05px)
  section._faq_h699x_46._home__faq   (grid-column:3/11 → x 342.7, w 754.6)
    span._faq__ontitle superFont @color[drk1] @family[inter] @size[12] @weight[600] @height[15] @align[center] @transform[uppercase]  " FAQ "   (display:block; margin-bottom:2.4rem)
    h2._faq__title superFont @color[drk1] @family[fkscreamer] @size[112] @weight[700] @height[80%] @align[center] @transform[uppercase]
       "Des questions? " <strong @color[prm1]>On vous répond</strong>    (width:52.4rem; max-width:100%; margin-inline:auto; margin-bottom:4.8rem)
    ul._list._faq__questions   (padding-bottom:6.4rem)
      li.@content > app-dropdown._dropdown superFont @family[inter] @height[140%]._faq__questions-question.(@show|@hide)  (@hide → display:none)
        button._dropdown__trigger superFont @color[iht] @size[18] @weight[500] @align[left]  aria-expanded
          (width:100%; height:7.2rem; display:flex; justify-content:space-between; align-items:center; gap:.8rem; padding-inline:.8rem 1.6rem; background:none)
          span._dropdown__trigger-title (display:-webkit-box; -webkit-line-clamp:2; overflow:hidden) — QUESTION
          app-icon @size[1] > svg._disclosure (16×16, stroke currentColor, round caps): <line x1="8" y1="2.66992" x2="8" y2="13.3399"/><line x1="2.67188" y1="8" x2="13.3419" y2="8"/>
        dropdown-region._dropdown__region role=region style="--dropdownContentHeight:<px>"  (display:block; overflow:hidden; max-height:0; transition:max-height .27s ease-out)
          p._dropdown__region-content superFont @size[15] @weight[400]  (position:relative; opacity:.7; padding-inline:.8rem; padding-bottom:2.4rem) — " " + ANSWER
        svg._musicString._dropdown__musicString viewBox="0 0 100 100" preserveAspectRatio="none"  (position:absolute; bottom:-7.2rem; left:0; z-index:-1; width:100%; height:14.4rem; pointer-events:none; stroke:#12004233)
          <path d="M0,50 Q{x},{y} 100,50" fill="none" stroke-width="1" vector-effect="non-scaling-stroke"/>
    button._cta._faq__cta.@show  (UIActionCTA darkGlass, arrow rotated 90° = chevron down; margin-inline:auto; transition:opacity .23s ease-out; .@hide → opacity:0!important; pointer-events:none)
       "Voir plus de questions"
```
Typography: ontitle 12px/600/lh 13.2px uppercase `#120042`. Title 98.3px/lh 78.7, 2 lines "DES QUESTIONS? / ON VOUS RÉPOND" (460px). Trigger: **no font-family is set on the `<button>`** → it uses the UA button font; Chromium computes `font-family: Arial` (rendered as Arial in screenshots) at 1.8rem (15.8px) / 500 / line-height normal, color inherit `#120042`, left. To match pixel-for-pixel set `font-family: Arial, sans-serif` on the trigger. Answer: vInter 1.5rem (13.2px)/400/lh 1.4 (from `@height[140%]` on the dropdown), opacity .7. Row height 7.2rem (63.2px); the visible separators between rows are the music-string paths (1px `#12004233` line at the row's bottom edge: svg centred on the bottom edge, path at y 50%).

Questions (16, in order; 6 shown initially, "Voir plus de questions" reveals +6 per click, CTA hides when all shown):
1. Comment se déroule une collaboration avec vous ? — Pour nous, chaque collaboration est avant tout une relation de confiance. Nous prenons le temps de comprendre vos attentes, nous élaborons une solution sur mesure, puis nous avançons avec vous en toute transparence. Notre équipe reste disponible à chaque étape pour vous accompagner et répondre à vos questions.
2. Que dois-je vous envoyer pour avoir un devis rapidement ? — Envoyez-nous en une seule fois un maximum d’informations : Objectif de la présentation, nombre de slides estimé, deadline, niveau de complexité (avec ou sans template existant, mise en page simple ou avancée, etc).⏎Dites-nous si vous avez besoin d’aide pour le contenu, le design, ou les deux ? Des Exemples de style souhaité (si vous en avez).⏎Nous échangeons toujours avec nos clients pour nous assurer que ce qu’ils demandent correspondent à leur besoin. Une de nos chefs de projets vous contacte pour un échange de vive voix. 20 minutes suffisent pour lancer votre projet !
3. Avec quel type d’entreprises travaillez-vous ? — Nous travaillons principalement avec de grandes entreprises nationales et internationales, car notre méthode et notre proposition de valeur sont davantage adaptées à des projets d’envergure ou fort enjeu stratégique.
4. Quels sont vos délais de réalisation ? — Le temps nécessaire pour réaliser une présentation dépend de sa complexité et de vos besoins. Après analyse de votre cahier des charges, nous estimons la durée de chaque intervention et vous proposons un planning adapté à vos contraintes
5. Comment fonctionne votre tarification ? — Nos prestations sont facturées au Tarif Journalier Moyen (TJM), modulé selon le type d’intervention. Notre expérience acquise depuis 2002 nous permet d’évaluer précisément le temps nécessaire à chaque réalisation.
6. Comment garantissez-vous la confidentialité de ma présentation ? — La confidentialité de vos présentations est une priorité absolue. Sur demande, nous signons des accords de confidentialité (NDA), travaillons sur des serveurs sécurisés, machines cryptées, serveurs VPN, et chacun de nos collaborateurs est tenu par une clause de confidentialité inscrite dans son contrat de travail. Nous pouvons même créer une cellule hermétique avec un accès restreint à un nombre limité de collaborateurs.
7. Pourquoi choisir la boite à slides ? — Contrairement à des approches uniquement visuelles ou uniquement narratives, chaque projet est pensé comme un outil de communication complet. Templates, contenus, formation et accompagnement sont conçus pour rendre les équipes autonomes et garantir la cohérence des prises de parole dans la durée. La valeur est dans la capacité à transformer PowerPoint en levier opérationnel, pas en simple support de mise en forme
8. Êtes-vous capables de gérer des projets de gros événements ? (narrow no-break space U+202F before "?") — Notre réseau de 40 experts et notre expertise nous permettent de piloter efficacement des missions complexes, avec un haut niveau d’exigence et de qualité.
9. Intervenez-vous sur les contenus ? — Nos experts en conception-rédaction anglophones et francophones prennent en charge vos contenus, de la rédaction complète au rewriting léger, selon vos besoins et votre niveau d’accompagnement.
10. Puis-je intervenir sur les contenus et la mise en page générale ? — Nous livrons nos présentations au format PowerPoint, vous donnant la liberté d’adapter facilement textes, visuels, design, pictogrammes, etc. selon vos besoins.
11. Utilisez-vous d’autres logiciels que PowerPoint ? — Nous sommes résolument centrés sur PowerPoint, nous délivrons également sur Google Slides, et pouvons nous adapter à tout type de solution de présentation comme Canva, ou Prezi. En complément, nous utilisons les logiciels de la suite Office 365 de Microsoft ainsi que ceux de la suite Adobe (Photoshop, Illustrator, Indesign, Premier…). Ajoutez à cela tous les logiciels maîtrisés par notre réseau étendu à 40 spécialistes autour de la présentation. Ces outils sont indispensables pour concevoir et livrer des présentations performantes.
12. Avec qui serais-je en contact pendant le projet ? — Vous serez accompagné par une cheffe de projet dédiée, votre interlocutrice principale, qui assurera la coordination, le suivi et la qualité du livrable. Si nécessaire, nos directeurs artistiques et graphistes PowerPoint interviendront pour garantir encore plus de fluidité.
13. Est-ce que je peux avoir ma présentation dans une semaine ? — C’est tout à fait possible. En fonction de nos disponibilités, nous pouvons faire appel à notre réseau pour renforcer les équipes de production et travailler + vite. Nous pouvons également étendre nos horaires de travail si nécessaire. Nous sommes cela dit fiers d'annoncer que notre organisation nous permet dans la majeure partie des projets de livrer sans dépasser les heures d'ouverture de l'agence.
14. Faites-vous des A/R illimités ? — Notre expérience acquise depuis 2002 nous permet d’évaluer précisément le temps nécessaire pour chaque projet, y compris pour les allers-retours. Cela garantit un projet efficace, sans perte de temps, tout en maintenant la qualité attendue
15. Je veux ma présentation sous 48h, savez-vous gérer ? — Notre réseau de 40 experts nous permet de prendre en compte toutes les demandes urgentes.
16. Proposez-vous des créations gratuites ? — Notre temps et notre savoir-faire sont entièrement dédiés aux projets de nos clients. Si le planning le permet, nous pouvons investir de notre temps pour travailler sur des pistes créatives.
(⏎ = newline in the CMS text; rendered as whitespace in the `<p>`.)

### 7.2 Accordion behaviour
- Single-open: FAQ holds `openIndex` (−1 = none); clicking a trigger toggles its own state and sets `openIndex = open ? i : -1`; every dropdown receives `propOpen = openIndex === i`, so opening one closes the previous.
- Open: `.@open ._dropdown__region{max-height:var(--dropdownContentHeight)}` where the variable = the content `<p>`'s measured height in px (resize-observed via the hidden iframe sensor, 50ms debounce); `transition:max-height .27s ease-out` both ways.
- Icon: `line{transform-origin:center; transition:transform .27s ease-out}`; open → first (vertical) line `rotate(90deg)`, last (horizontal) line `rotate(-180deg)` ⇒ "+" becomes "−".
- `aria-expanded`, `aria-controls`, region `aria-labelledby`, `aria-hidden=!open`.
### 7.3 Music-string interaction (`UIUtilMusicString`)
Control point (cx, cy) in the 0–100 viewBox, rest (50, 50):
- mousemove over the questions list (event forwarded to every dropdown): if the pointer is inside this svg's rect: `r = (pageY - svgTop)/svgHeight*100`; if `|cy - r| > 15` → release; else `gsap.to(cx, {value: (clientX - left)/width*100, duration:.1})`, `gsap.to(cy, {value: 50 + (r - 50)*.4, duration:.1})` → the line bends toward the cursor ("plucking" a string).
- release / mouseleave: `gsap.to(cx,{value:50,duration:.7})`, `gsap.to(cy,{value:50,duration:.7,ease:"elastic.out(1.5, .3)"})` (string vibrates back).
- On scroll while the FAQ is in view: `gsap.to(cy, {value: 50 + clamp(scrollDeltaY, -15, 15), duration:.15})` (string sags with scroll velocity).
- Desktop only ("earthquake" reactor off on mobile).
### 7.4 Scroll motion (trigger = FAQ section unless noted)
| Target | Helper | start → end |
|---|---|---|
| " FAQ " ontitle | BLUR in (100px → 0) | `"0% 90%"` → `"0% 50%"` |
| title | WORDS_REVEAL | default `"0% 90%"` → `"0% 30%"` |
| questions `<ul>` | MASK_WIPE h=200, pct=90 → mask `linear-gradient(0deg, transparent calc(50% - 100px), red calc(50% + 100px)) 0% 0% / 100% calc(200% + 200px) no-repeat`, `maskPosition 0% 100% → 0% 0%`, ease none, trigger = the ul | `"0% 90%"` → `"100%+=200 90%"` |
| CTA | FADE in | `"100% 100%"` → `"100% 60%"` |
The mask wipe reveals the list top-to-bottom with a 200px soft edge (visible in screenshots as the 6th question still fading).
### 7.5 Mobile
`grid-column:1/13; justify-self:center; width:100%; max-width:min(93rem,100%)`.

---

## 8. Footer — `footer#FOOTER.superDevice.superFont.@color[lgh1]` (y 34 898.9, h 1 041.5)

### 8.1 DOM
```
footer#FOOTER  (position:relative; z-index:5; min-height:100vh/100svh; padding-block:20rem 3.2rem; superDevice → width 83vw (1195.2), padding-inline 3.2rem; color #fff)
  app-title._footer__title superFont @family[fkscreamer] @size[164] @weight[700] @height[75%] @align[center] @transform[uppercase]
     "Prêt à transformer votre " <strong class="superFont @color[drk1]">impact?</strong>     (display:block; width:97.5rem; max-width:100%; margin-inline:auto; margin-bottom:3.2rem)
  a._cta._footer__cta href="/contact"  (light design: white buttons, #120042 text) "Contactez-nous"   (margin-inline:auto; margin-bottom:12.5rem)
  app-container[FOOTER-A1] superGrid @columns[12] @margin[48] @gi[16] superGlass @glow @blur[24] @background[lgh]
     (grid 12 cols; padding-inline 4.8rem (gridMargin); padding-block:4.8rem; border-radius:3.2rem; grid-template-rows:repeat(3,auto); position:relative; overflow:hidden)
    [FOOTER-B1] (grid-column:1/13; grid-row:1; display:flex; gap:3.2rem)
      [FOOTER-C1] (flex:2; flex-direction:column; display:flex; gap:2.4rem)
        a._footer__logo href="/" (width:fit-content) > svg logo 124×48 viewBox (white) — same SVG as the header logo (Spec A)
        ul._langSwitcher.@light (display:flex; flex-wrap:wrap)
          button._langSwitcher__option.@current "fr"  superFont @family[inter] @size[11] @weight[700] @height[15] @transform[uppercase]  (height:2rem; padding-inline:.8rem; border-radius:4rem; background:#fff; color:#120042)
          button._langSwitcher__option "en"  (opacity:.5; background:none; color:#fff)
        address superFont @family[inter] @size[15] @weight[400] @style[normal] @height[140%]  "Paris, Bordeaux, Verdun, Aix-en-Provence, Rennes, Strasbourg"
      nav._footer__explore (flex:1)   — title "Explorer"; routes @size[24] @weight[500] @space[-.02em] @height[130%]:
          Réalisations /realisations · Nous connaître /nous-connaitre · Notre méthode /la-methode-labas · Ressources /ressources · Contact /contact · Offres d'emploi /nos-offres-d-emploi
      [FOOTER-C2].@wrapper (flex:1; display:flex; gap:3.2rem)
        nav._footer__expertises — title "Expertises"; routes @size[15] @weight[500] @height[140%]:
          Communication 360 /expertises/communication-360 · Navigation App Like /expertises/navigation-interactive-powerpoint · Animatiques /expertises/Animatiques-powerpoint · Conférences Interactives /expertises/conferences-interactives · Séminaire VR /expertises/seminaire-realite-virtuelle · Solutions IA /expertises/solutions-ia-powerpoint · Formations & Coaching /expertises/formations-powerpoint-coaching-labas-agence-powerpoint
        nav._footer__expertises — title "Présentations"; routes (`<strong>Présentation</strong> xxx`, strong weight inherit):
          Présentation commerciale …/presentation-commerciale · Présentation corporate …/presentation-corporate · Présentation événementielle …/presentation-evenementielle-labas-agence-powerpoint · Présentation appel d’offre …/presentation-appel-offre · Présentation ressources humaines …/presentation-ressources-humaines · Masque PPT …/masque-ppt-labas-agence-powerpoint · Présentation marketing …/presentation-marketing · Présentation financière …/presentation-financiere   (all under /expertises/presentations-powerpoint/)
    ul._footer__labels (grid-column:1/13; grid-row:4; display:flex; flex-wrap:wrap; gap:2.4rem; margin-block:1.6rem 3.2rem)
      app-tooltip._footer__labels-label ×3  (display:flex; flex-direction:column-reverse; width:fit-content; transition:opacity .2s ease-out)
        tooltip-slot._label__slot tabindex=0 (4.8rem × 4.8rem, inline-block) > img._label__icon (100%, contain)
        tooltip-bubble role=tooltip (position:relative; width:100%; height:3.2rem; margin-bottom:1.5rem; opacity:0; transition:opacity .2s ease-out)
          bubble-title superGlass @blur[24] @background[lgh] superFont @color[lgh1] @family[inter] @size[12] @weight[500] @height[140%]
             (position:absolute; top:0; left:0; height:100%; display:flex; align-items:center; padding-inline:16px; border-radius:48px; white-space:nowrap; bg #ffffff1a; blur 24px)
          svg._tooltip__bubble-arrow superGlass (13×8, absolute top:100%; left:50%; translateX(-50%); width:1.3rem; fill #ffffff1a) path "M7.27611 7.04478C6.87592 7.53733 6.12408 7.53733 5.72389 7.04478L-2.54292e-07 -1.82822e-07L13 9.53674e-07L7.27611 7.04478Z"
      labels: 1 `/sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg` "Certifié ISO 9001:2015 Bureau Veritas" (alt "Certification ISO9001 LABAS"); 2 `/sk/uploads/Badge_simple_MOS_LABAS_d0815bc7cf.svg` "Microsoft Office Specialist"; 3 `/sk/uploads/Logo_simple_Avis_Google_LABAS_f10bfef852.svg` "5 étoiles Google Avis" (alt "Avis Google LABAS")
    [FOOTER-B2] (grid-column:1/5; grid-row:5; display:flex; align-items:center; gap:.8rem)
      small.copyright superFont @family[inter] @size[15] @weight[500] @height[140%] "©2026"
      button.seoModalTrigger superFont @color[lgh1] (opacity .5) > info icon @size[1] — opens the SEO modal (Spec A §8)
    [FOOTER-B3] (grid-column:5/13; grid-row:5; display:flex; justify-content:space-between)
      nav._footer__socials (display:flex; gap:1.6rem) > a LinkedIn https://www.linkedin.com/company/laboiteaslides/ , a Vimeo https://vimeo.com/laboiteaslides?fl=pp&fe=sh  (icons @size[3] = 2.4rem; 20×20 viewBox SVGs, fill currentColor)
      nav._footer__legals (display:flex; gap:2.4rem) > "Mentions légales" /mentions-legales · "Politique de confidentialité" /politique-de-confidentialite · "Cookies" #   (superFont @color[iht] @family[inter] @size[15] @weight[500] @height[140%]; white-space:nowrap)
```
Nav titles (`._nav__title`): vInter `max(1.2rem,12px)`/600/lh 1.5rem uppercase, opacity .5, margin-bottom `max(1.2rem,12px)`. Route link `display:block; width:fit-content`; `._nav__route-title{display:inline-block; transition:transform 1.5s cubic-bezier(.13,.93,.13,.93) .03s, color 1.5s cubic-bezier(.13,.93,.13,.93) .03s}`, hover → `transform:matrix(1,0,0,1,10,0)` (slides 10px right).

### 8.2 Computed @1440
- Title: FKScreamer 16.4rem (144px)/lh .75 (108px), 2 lines "PRÊT À TRANSFORMER / VOTRE IMPACT?" width 856px, white; strong `#120042`. Starts 175.6px below the footer top.
- CTA 49.2px tall, centred, 109.8px (12.5rem) above the glass panel.
- Glass panel: x 150.5, w 1139, h 420.4, padding 42.1px (4.8rem) all round, radius 28.1px. Columns 75px, col-gap 14px. Row 1 (B1) 189.5px: C1 396.6px | explore 198.3px | C2 403.6px (two lists 158 + 217.5, gap 28px). Explore routes 2.4rem (21.1px)/500/lh 1.3 (27.4px)/ls −.02em (−0.42px). Expertise routes 1.5rem (13.2px)/500/lh 18.4px. Labels row: icons 42.1px, gap 21px. Bottom row y +357: ©2026 13.2px/500; socials 21.1px icons gap 14px at x 548.9; legals right-aligned ending at x 1247.3, gap 21px.
- `@glow` glass (CLONE_SPEC A/global CSS): `::before`/`::after` absolute inset z −1, both `background-color:#ffffff0d`; `::before` `backdrop-filter:blur(24px)` + `background:radial-gradient(circle at center, hsl(220 90% 60% / calc(var(--glassIntensity)*.13)) 0, rgba(165,165,243,.07) 11%, rgba(224,213,246,.03) 19%, transparent 37%) var(--glassBackgroundRX) var(--glassBackgroundRY)/200% 200% no-repeat`; `::after` `backdrop-filter:blur(calc(var(--glassGlowBlur)*var(--glassIntensity)))` masked by `radial-gradient(circle at center,#000 0,rgba(0,0,0,.7) 19%,transparent 43%) var(--glassMaskRX) var(--glassMaskRY)/200% 200%`. JS `Glower`: on mouseenter target intensity 1 (leave 0); per tick `intensity += (target-intensity)*.03`, `bgRX/RY += (mouse% - cur)*.05`, `maskRX/RY += (mouse% - cur)*.07`, where mouse% = `clamp(1 - (clientX-left)/width,0,1)*100` (and same for Y) → a soft light spot follows the cursor across the panel.
### 8.3 Hover
- Labels: hovering/focusing label n sets `.@highlight` on the list and `.@target` on n → other labels `opacity:.3` (.2s ease-out); bubble of n fades to opacity 1 (.2s ease-out).
- Lang switcher: current pill white bg / drk text; other .5 opacity.
- Buttons: Spec A §1.2.
### 8.4 Motion
- Background final layer (PRM): see §0.2 (33 999 → 34 899).
- Title: WORDS_REVEAL (colour prm1 → white / strong prm1 → drk1), trigger footer, `"0% 70%"` → `"0% 10%"`.
- CTA: FADE in, `"0% 40%"` → `"0% 0%"`.
- Footer glass triangles (WebGL): `TRIANGLES` plugin group (glass material, same triangles as the hero; data `BGRTs5Rh.js` export `t` = positions/rotations list S, length R), group initial position `[TRIANGLE_SIZE/2, -100, -47]`, rotation `[π, .5, .3]`, hidden. Timeline `H` (`trigger:#FOOTER, getOverflowStart:()=>lvh, scrub:true`, eEnter → show + start tick, eLeaveBack → hide): track `{end:1, overflowStart:1}`: `i = 1-(1-t)²; K = t²` (material opacity), `q = 1 + (1-i)*2` (spread factor), group y lerps `-100 → 3` with i. Per tick: `J += delta*.3`; when J reaches 1 → J = 0, Y = (Y+1) % R — every triangle moves from slot (t+Y−1) to slot (t+Y) over 1/0.3 s (a slow conveyor of glass triangles), positions x/z multiplied by q and rotation by q. This is what fills the purple background behind the footer in screenshots.
### 8.5 Mobile
`#FOOTER{background-color:#6630ff}` (solid, no WebGL); title `@size[112] @height[80%]` (78.4px), `max-width:93rem`; A1 `max-width:93rem; grid-template-rows:repeat(6,auto); row-gap:3.2rem; margin-inline:auto`; B1, C2 and B3 `flex-direction:column`; B2 `grid-column:1/13; grid-row:6`; B3 `grid-column:1/13; align-items:center; gap:3.2rem`; expertise lists `column-count:2`; expertise routes `@size[20]`; address `@size[20]`. Measured footer height 1 490px.

---

## 9. Assets

### 9.1 Images / SVG / models used in this half (all present under `public/`)
| Path | Where |
|---|---|
| `/sk/uploads/large_Presentation_e945d6b799.png`, `large_Communication_360_7a5ef30bda.png`, `large_FDH_URW_navigation_interactive_87d42a0822.jpg`, `large_Immersion_VR_e950803a61.png`, `large_Assistance_IA_LABAS_bot_1963bf7998.jpg` (+ medium_/small_/thumbnail_) | Expertises hover images (37.7×25.3rem, cover) |
| `/assets/models/DECIMATE v2_compressed-compressed.glb` | VR headset (DRACO) |
| 61 × `/sk/uploads/small_*.jpg` (§9.2) | VR sphere textures |
| `/sk/uploads/large_Labas_20f4ebe642.jpg` | Spotlight image |
| `/sk/uploads/large_presentation_equipe_0eebf6541e.jpeg` | Resource card "Cas client" bg |
| `/assets/images/whitePaper/2.png` | White-paper cover bg |
| `/sk/uploads/Badge_Google_avis_labas_149fc344c9.png`, `Badge_ISO_9001_labas_49c6d38cef.png`, `Badge_MOS_labas_83992cf13f.png` | Label cards (20rem, contain) |
| `/sk/uploads/thumbnail_logo_Caterpillar_c129772a64.png`, `thumbnail_logo_safran_2088913497.png`, `thumbnail_logo_essilor_4f286cb915.png`, `thumbnail_logo_bostik_5b01f5c5a7.png`, `thumbnail_logo_vaudoise_8647c5fc66.png`, `thumbnail_Syngenta_43c016de86.png`, `thumbnail_Nestle_waters_8a22365e28.jpg` | Review avatars (5.6rem, white bg, radius 2rem) |
| `/sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg`, `Badge_simple_MOS_LABAS_d0815bc7cf.svg`, `Logo_simple_Avis_Google_LABAS_f10bfef852.svg` | Footer label icons (4.8rem) |
| Fonts `/fonts/FKScreamer/woff2/FKScreamerLegacy-Upright.woff2` (family `FKScreamer`), `/fonts/Inter/Inter.woff2` (family `vInter`, variable) | all text |

### 9.2 Sphere texture list (load order as requested by the page; plane i uses texture i % 61)
small_Adobe_Stock_206118370_5ab61dcb89, small_Brasseries_kronenbourg_2_ef3160d1cb, small_Brico_Depot_9265283144, small_Econocom_1_bbf2deda06, small_Candriam_d7ec4211ac, small_Brasseries_kronenbourg_3_2c511aaf16, small_Brasseries_kronenbourg_c4aa37d707, small_Live_cam_powerpoint_66ba77a3d6, small_Live_cam_Realite_Augmentee_powerpoint_1_326712230e, small_Econocom_2_b5451e30d7, small_Econocom_3_09b37caa26, small_Econocom_4_d6a171dce4, small_Limatech_0200a6e1da, small_Live_cam_Realite_Augmentee_powerpoint_2_0da8adf478, small_qui_veut_gagner_des_millions_7ec0f870fa, small_Trivial_Pursuit_8a4b25c1ca, small_Maison_Perrier_Award_219180308a, small_Maison_Perrier_6c1d185c63, small_Maison_Perrier_Chic_2e80303fbc, small_Trivial_Pursuit_5_Trivial_Pursuit_6_34207ab249, small_Trivial_Pursuit_5_e5e59ced1f, small_Trivial_Pursuit_3_7f9cf56cb4, small_Trivial_Pursuit_2_6fafb6e677, small_Trivial_Pursuit_4_07eee46f2f, small_twix_snickers_a4c29b83f1, small_Araymond_4eb84ffff0, small_Vaudoise_0b797b5987, small_Adidas_20ec508fa3, small_Audiens_b499a54b85, small_Axa_aide_a_la_vente_a02a510b23, small_Axa_ed688ebfaa, small_Babymoov_cb337e2d48, small_Caterpillar_2278246ff0, small_Chanel_f654a93dae, small_CBRE_00fce42506, small_Coface_144ab51cdd, small_Essity_9872bcbd26, small_JDM_PRES_PPT_04_1_e2c5eec858, small_Flextone_1839960e8e, small_General_Motors_0fde66cf2b, small_M_and_Ms_mini_e4ae435636, small_Liebig_2b76ec3546, small_Marie_9cca944ff8, small_Nissan_aa945746e2, small_Nuxe_72b8bd830c, small_Mars_wrigley_ac9f9d1412, small_Pukka_9c6a08bda9, small_Renault_electric_dcecf4d28c, small_Renault_dd9391e8d8, small_Saur_cbcd180b87, small_Safran_bc185c343c, small_The_edge_1_5cf73378d2, small_The_edge_1_2_bef5289ffc, small_Renault_ev_forum_f11bc1287b, small_Ship_up_73ecf0f94b, small_Total_energies_8ec1dc0287, small_Upcoop_f8ef861fe9, small_wolf_oil_e2c4402e3a, small_Viridien_bbd464d417, small_Vittel_980cb8f103, small_Tishman_speyer_10c8fc2359 — all `.jpg` under `/sk/uploads/`. (These are requested in parallel, so the network order is not guaranteed to be the CMS order; the CMS order lives in `__NUXT_DATA__` `sphere` — any stable order is visually equivalent.)

---

## 10. Not measurable / caveats
- WebGL output (headset shading, env map, RGB-shift strength, sphere lighting) can only be compared visually; recipe values are from source. Headless swiftshader renders were used for the screenshots.
- `E` in the label-card path depends on the first card's rotated bounding-box width at LOAD time (it is measured with the card's current transform); live values back out to E ≈ 1 910–1 930 at 1440. Replicating the formula (measure after first applying the transform) gives the same behaviour.
- Random values (expertise `--vx/--r`, label-card `rnd_r`/`i_r`, sphere spin start) differ per page load on the original too.
- The VR auto-scroll snap (`__scroll_toMotion`) did not trigger under synthetic wheel input; behaviour is documented from source only.
- FAQ answers are also present as JSON-LD (`FAQPage`) in `reference/original.html`; the clone should emit the same `@graph` FAQPage schema if SEO parity matters.
