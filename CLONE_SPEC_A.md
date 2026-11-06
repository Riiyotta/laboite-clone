Source: https://laboiteaslides.fr/

# CLONE_SPEC_A — laboiteaslides.fr FR homepage, TOP HALF (y 0 → 20 570 @ 1440x900)

Scope: fixed `#HEADER` + menu overlay + loader, and in `section#HOME`: hero header `_header_jx0rq`, tagline sticker, works, method (marquee), skills sticker — i.e. everything above `_expertises_jvwcv` (starts y = 20 570.5). The SEO modal (`_seoModal` / `_content_1uvg3`) is also documented (it sits in the DOM between hero and tagline but is a hidden dialog).
Companion file: `CLONE_SPEC_A_ASSETS.md` (inline SVG markup for logo/icons, full 22-triangle keyframe JSON, asset list).

How values were obtained: computed styles / rects from an isolated headless Chromium (Playwright, 1440x900 and 390x844, WebGL working), scroll-scrubbed screenshots at ~55 scroll positions, plus the shipped source (`reference/nuxt/*.js`, scoped CSS in `reference/original.html`, `public/_nuxt/style.B5ikKiSh.css`). Timeline numbers below are quoted from source and cross-checked against live computed transforms (e.g. widgets `--progress` at y=300 = 11.11 % = 300/2700, subtitle line 0 opacity .6775 at y=4400 = power1.out(.432)).

---------------------------------------------------------------------------------------------------

## 0. Global system

### 0.1 rem / breakpoints
- `html { font-size: clamp(7px, .6097560976vw, 10.2777777778px) }` → 8.78049px @1440, 7px @≤1148 (so 7px @390). Every value below is in rem unless marked px.
- `html { font-family: vInter,"sans-serif",arial; color:#120042; background:#fff; overflow-x:hidden }`, `html, body { width:100vw; overscroll-behavior:none }`.
- Formats: Desktop `min-width:1440px and min-height:435px`; Tablet `768–1439.9px`; Mobile `max-width:767.9px OR max-height:434.9px`. "Whole" (= full 3D/scroll-animated experience) = NOT mobile. On mobile none of the scroll timelines or 3D plugins are created.
- `.superDevice`: desktop/tablet `width:83vw; max-width:1480px; margin-inline:auto; padding-inline:3.2rem; box-sizing:border-box` → at 1440: x 122.4 → 1317.6, content 150.5 → 1289.5 (1139px). Mobile: `width:100vw; padding-inline:2rem`.
- `#MAIN` (superDevice) `margin-bottom:40rem; transition: opacity .3s ease-out`.

### 0.2 Utility decode (from style.B5ikKiSh.css)
- `superFont @size[N]` → `font-size:N/10 rem` (11 and 12 are `max(1.1rem,11px)` / `max(1.2rem,12px)`). `@weight[N]` → font-weight N. `@space[-.04em]` → letter-spacing -.04em (also -.03/-.02/-.01/0). `@height[75%]`→ lh .75, `[80%]`→.8, `[85%]`→.85, `[90%]`→.9, `[100%]`→1, `[104%]`→1.04, `[130%]`→1.3, `[140%]`→1.4, **`[150%]`→1.6** (sic), `@height[15]` → 1.5rem. `@family[fkscreamer]` → `font-family:FKScreamer; font-synthesis:none`; `@family[inter]` → `vInter; font-synthesis:none`. `@transform[uppercase]`, `@align[left|center|right]`. Colors `@color[lgh1|drk1|gry2|gry3|prm1|trt3|err1|iht(inherit)]`.
- `superGrid` → `display:grid; grid-template-columns:repeat(var(--gridColumns),minmax(0,1fr)); gap: var(--gridGapBlock) var(--gridGapInline); padding-inline: var(--gridMargin)`. `@columns[N]`; `@gb[0|8|16|24|32|56|103|200]` → 0/.8/1.6/2.4/3.2/5.6/10.3/20rem; `@gi[0|8|16|42|64]` → 0/.8/1.6/4.2/6.4rem; `@margin[16|25|48]` → 1.6/2.5/4.8rem, `@margin[mobile]` 2rem.
- `superGlass`: `@blur[7|24|90]` → `--glassBlur:7|24|90px`; non-glow: `backdrop-filter: blur(var(--glassBlur))`; `@background[lgh]` → `#ffffff1a`, `@background[drk]` → `#12004212`. (svg variant uses `fill`.)
- `superPreAccents @step[.1em]` (added by SplitText helper to every split line/word parent): `padding-block:.1em; margin-block:-.1em` (the `@noFix` variant has no negative margin).
- Fonts: `@font-face vInter: url(/fonts/Inter/Inter.woff2) format(woff2); font-weight:100 900; font-display:swap` and `FKScreamer: url(/fonts/FKScreamer/woff2/FKScreamerLegacy-Upright.woff2); font-weight:400` (only one face — weight 700/900 requested with `font-synthesis:none` renders the regular face, do NOT fake-bold).

### 0.3 Colors
`--lgh1 #FFFFFF, --drk1 #120042, --gry1 #CECECE, --gry2 #ACA6BD, --gry3 #5F5F5F, --prm1 #6630FF, --scd1 #01DAF6, --scd2 #FF61F8, --scd3 #62F740, --trt1 #29DAFF, --trt3 #70F74A, --err1 #D00000`. Background-shader pairs (top / bottom): LGH `#FFFFFF/#EDEDED`, PRM `#6630FF/#612EF1`, SCD `#62F740/#61ED40`, TRT `#29DAFF/#27CEF1`, DRK `#120042/#10003D`, GRY `#CECECE/#CBCBCB`, BLK `#080808/#080808`.

### 0.4 Libraries & shared motion primitives
- GSAP 3 + ScrollTrigger + CustomEase + SplitText, `gsap.ticker.lagSmoothing(0)`, `ScrollTrigger.config({autoRefreshEvents:""})`. Lenis 1.3.26 `new Lenis({autoRaf:false})` (all defaults: lerp .1), driven from the GSAP ticker.
- **GSAP default ease is used wherever none is given = `power1.out`** (verified numerically).
- Custom eases: `custom::out` = `CustomEase "M0,0 C.084,.61 .088,.874 .184,.944 .283,1.016 .374,1 1,1"`; `custom::out::back` = `"M0,0 C.08,.7 .1,1.05 .2,1.12 .35,1.08 .5,1 1,1"`; `home::custom::out` = `"M0,0 C0,1 0,0.903 1,1"`.
- Text split helpers (SplitText): lines get class `line` (+ `mask:"lines"` when masked), words `word`, chars `char`.
  - **linesSlide(el, in, axis)** (`I`): lines `{[axis]: 20px (or -20 for '-x'), autoAlpha:0}` → `{[axis]:0, autoAlpha:1}`.
  - **fade(el, in|out)** (`R`): `autoAlpha 0→1` / `1→0`.
  - **parallax(el, n)** (`z`): `y: n px → -n px`.
  - **wordsRise(el)** (`De`): split `lines,words` with line masks; words `{y:"130%", scale:1.05}` → `{y:"0%", scale:1}` and simultaneously word color `#6630FF → element's computed color`.
  - **charsIn(trigger, [els])** (`L`): split chars (mask chars); `{x:"100%", opacity:0}` → `{x:"0%", opacity:1}`, `stagger:.05, duration:1.7, ease custom::out`, ScrollTrigger `{trigger, start:"0% 100%", scrub:false, toggleActions:"play none none reverse"}`.
  - **maskReveal(el, size=200, at=90)** (`F`): `mask: linear-gradient(0deg, transparent calc(50% - 100px), red calc(50% + 100px)) 0 0 / 100% calc(200% + 200px) no-repeat`, tween `maskPosition "0% 100%" → "0% 0%"`, ease none, ScrollTrigger `{trigger:el, start:"0% 90%", end:"100%+=200 90%", scrub:true}`.
- **Section Timeline class** (used for every pinned/scrubbed section; reproduce exactly):
  ```
  tl = gsap.timeline({duration:1, scrollTrigger:{trigger, scrub:true,
        start: overflowStartPx ? `0%-=${overflowStartPx} 0` : `0% 0`,
        end:   overflowEndPx   ? `100%+=${overflowEndPx} ${lvh}` : `100% ${lvh}` }})
  T = end - start (scroll px); s = ovStartPx/T; c = ovEndPx/T; o = 1 - s - c
  item {start=0,end=1,overflowStart=0,overflowEnd=0}:
     tStart = o*start + s*(1 - overflowStart)
     tEnd   = s + o*end + c*overflowEnd          (timeline time, 0..1; scrollY = startPx + t*T)
  multi-target items with itemDuration k: each item lasts B*k where B = 1 - s*(1-overflowStart) - c*(1-overflowEnd);
     stagger = (tEnd - tStart - B*k)/(n-1).    With `stagger:x` instead: stagger = B*x.
  ```
  "Tracks" are onUpdate callbacks with the same start/end mapping and progress clamp 0..1. All scrub = `true` (no extra smoothing; Lenis supplies the smoothing).
- All scroll-px numbers in this spec are for 1440x900 (lvh = 900).

---------------------------------------------------------------------------------------------------

## 1. Fixed `#HEADER` (z-index 6)

### 1.1 DOM
```
header#HEADER  (position:fixed; top:0; left:0; z-index:6; width:100vw; isolation:isolate; pointer-events:none)
  app-loader (§2)
  div.[HEADER-A1].superDevice   (display:grid; grid-template-columns:0 1fr 0; grid-template-rows:1fr; align-items:center; height:12rem)   children pointer-events:auto
    a[href="/"].header__reload        (width:fit-content)  > svg logo 12.4rem x 4.8rem (viewBox 0 0 124 48; see assets), color lgh1|drk1
    button.header__menuTrigger  (Button, @hover @bottom, justify-self:center; z-index:3; padding-left:2.4rem)
       app-icon size 3 (child height 2.4rem) > svg.points (3 circles)
       div.[HEADER-B1] (position:relative; white-space:nowrap)
          div.[HEADER-C1] "Menu"
          div.[HEADER-C2] "Fermer"   (position:absolute; top:50%; left:0; transform:translate3d(0,-50%,0))
    a[href="/contact"].header__cta  (Button @hover @bottom, justify-self:right; white-space:nowrap) "Demander un devis"
  section._menu (§1.4)
```
Measured @1440 (y=0 state): header box 0,0 1440x105.4 (12rem). Logo 150.5,30.6 108.9x42.1. Menu trigger 663.6,28.1 112.8x49.2. CTA 1111.5,28.1 178x49.2 (right edge 1289.5).

### 1.2 Buttons (component `Button`)
- Base: `display:flex; justify-content:center; align-items:center; gap:.8rem; height:5.6rem; border-radius:2.4rem; padding-inline:3.2rem` (round variant: width 5.6rem, aspect 1/1, no padding). Text: `vInter 1.5rem / 500 / line-height 1.4` (13.17px / 18.44px @1440).
- Designs: `light` = bg #FFFFFF color #120042; `dark` = bg #120042 color #FFF; `primary` = bg #6630FF color #FFF; `lightGlass` = backdrop-filter blur(24px), bg #ffffff1a, color #FFF; `darkGlass` = blur(24px), bg #12004212, color #120042.
- Hover (`@hover @bottom`): `::before` (absolute, inset 0, size calc(100%+1px), z-index -1, radius 2.4rem, transform translate3d(-.5px,-.5px,0)) painted with
  `background-image: radial-gradient(ellipse 50% 12.5% at 50% 37.5%, #6630ff 100%, transparent 0), linear-gradient(180deg, transparent 37.5%, #6630ff 0); background-size:100% 400%; background-position:50% var(--button-hover-y)` and
  `mask: linear-gradient(180deg, red 75%, transparent 0), radial-gradient(ellipse 50% 12.5% at 50% 75%, transparent 100%, red 0); mask-size:100% 400%; mask-position:50% var(--button-hover-y); mask-composite:intersect`.
  mouseenter: `gsap.fromTo(btn, {"--button-hover-y":"0%"}, {"--button-hover-y":"50%", duration:2.5, ease:"custom::out"})` + class `@hovered` (`color:#fff !important`, `transition: color .25s ease-out`). mouseleave: `to {"--button-hover-y":"100%", duration:.4}` then set back to `0%`. Effect: purple fill rises from bottom with a domed top edge, exits upward on leave. (`@left/@right` variants use the 90deg-rotated equivalents.)
- Header-specific transitions: CTA / trigger / logo `transition-duration:.37s,.37s,.25s; transition-timing-function:ease-out`; CTA & trigger `transition-property: backdrop-filter, background-color, color`.

### 1.3 Header color logic (light vs dark)
`light = true` → logo color #FFF, CTA design `light`, trigger `lightGlass`. `light = false` → logo #120042, CTA `dark`, trigger `darkGlass`. Menu open → logo drk1, CTA `dark`, trigger `light`. While the loader is animating the trigger is `lightGlass`.
Rule: probe line = scrollY + headerHeight/2 (52.7px). (a) If it lies inside a registered "light" DOM region → light. The only region in scope: the works cards grid `nav._workCardsPanoramic` (y 11 644.8 → 13 822.4), so light for scrollY ∈ [11 592, 13 770]. (b) else take the top-most background-shader layer whose transition ≥ G (G = 1 − headerH/lvh/2 = 0.9414); light if luminance(.299R+.587G+.114B of its top color, 0..1) < .5. PRM (.344) → light; LGH/SCD/TRT → dark.
Measured switches: light for y < ~2000 (purple bg), dark from 2160 (white sweep complete at 2160), light 11 861–13 700 (cards), dark elsewhere through 20 570.

### 1.4 Menu trigger text swap + icon
- Closed (`@close`): C1 `clip-path: polygon(0 0,100% 0,100% 100%,0 100%)`, C2 `polygon(100% 0,100% 0,100% 100%,100% 100%)`. Open (`@open`): C1 `polygon(0 0,0 0,0 100%,0 100%)`, C2 full. `transition: clip-path .4s ease-out` → text wipes left→right between "Menu" and "Fermer".
- Icon: open → `animation: aIconIntro .2s ease-out forwards` (0% none, 50% rotate(15deg) scale(.9), 100% rotate(31deg)); close → `aIconOutro .2s ease-out forwards` (reverse).
- `@hidden` (before app state ready): `visibility:hidden; opacity:0; pointer-events:none`; base `transition: opacity .5s ease-out .7s`.
- Load intro (desktop only, on LOAD): logo `gsap.from({x:-7})`, CTA `gsap.from({x:7})`, both `duration 7, delay .7, ease custom::out`.

### 1.5 Menu overlay `section._menu_1qvgh` (inside #HEADER, after A1)
Layout (desktop, `:not(.@mobile)`):
- `position:absolute; top:.8rem; left:.8rem; z-index:2; width:calc(100vw - 1.6rem); height:calc(100dvh - 1.6rem)`; hidden until loaded (`:not(.@loaded){visibility:hidden}`), `.@show{pointer-events:auto}`. Measured 7,7 1425.9x885.9.
- `app-background` absolute inset, z -1, `perspective:100rem; transform-style:preserve-3d` > `background-panel` `background:#fff; border-radius:3.2rem; transform-origin:bottom; backface-visibility:hidden`. The purple seen around the panel (0.8rem frame) is the loader panel (§2) which closes over the page when the menu opens.
- `[MENU-A1]` = `superGrid @columns[12] @margin[25] @gi[16]`, `position:relative; padding-block:11.5rem 3.2rem` (measured padding 100.98px 21.95px 28.1px), overflow visible.
- Lang switcher `ul` absolute `top:3.2rem; right:3.2rem`: options `vInter max(1.1rem,11px) / 700 / lh 1.5rem uppercase`, `height:2rem; padding-inline:.8rem; display:flex; align-items:center`; current: `bg #120042; color #fff; border-radius:4rem`; other: `opacity .5; color #120042`. Text "fr", "en". Measured 1348,35.1.
- Widgets `ul.menu__widgets` = `superGrid @columns[2] @gb[16] @gi[16]`, `grid-column:1/6; grid-template-rows:repeat(2,1fr); height:calc(100svh - 16.3rem); perspective:100rem; transform-style:preserve-3d`. Measured 29,108 567.7x756.9. Items (`overflow:hidden`):
  1. Expertise widget (`grid-column:span 2`, 567.7x371.4) link `/expertises/conferences-interactives`: section `position:relative; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; overflow:hidden; background:#080808; border-radius:2.4rem`. Title "Conférences Interactives" `FKScreamer 6.4rem / 700 / lh .85 / center / uppercase / #fff`, margin-bottom 1.6rem. CTA = UIActionCTA lightGlass: round 5.6rem arrow button + pill "Découvrir" (gap 0, measured buttons 49.2 + 118.1 wide). Image `/sk/uploads/large_Presentation_augmentee_1d02882a38.jpg` absolute cover, `opacity:.32`, z -1.
  2. Resource widget "Livre blanc" (276.8x371.4) link `/ressources/4-conseils-pour-capter-lattention-en-1-minute`: `padding:2rem; border-radius:3.2rem; background:#12004212`. Tag "Livre blanc" (tag: `height:4rem; padding-inline:1.6rem; border:max(.1rem,1px) solid #12004212; border-radius:1.6rem; vInter 1.5rem/500/1.4; color drk1`). White paper: wrapper `margin-top:3.8rem; width:100%`; A1 `transform:rotate(3.13deg); aspect-ratio:390.93/418.47; filter:drop-shadow(10.346px 20.692px 31.038px rgba(0,0,0,.12))`; `::before` white sheet `top:5.65%; left:4.56%; width:93.29%; aspect-ratio:364.7/445.61; transform:rotate(2.2deg); border-radius:2.13%`; B1 cover `width:93.29%; aspect-ratio:364.7/476.52; padding:7.95%; border-radius:2.13%; background:#6630ff url(/assets/images/whitePaper/2.png) 50%/cover`. Cover title "4 conseils pour capter l’attention en 1 minute" `FKScreamer 3.2rem/700/lh .9/uppercase/#fff`.
  3. Resource widget "Cas client" (276.8x371.4) link `/ressources/arcitek-presentation-corporate`: `background:#120042`, `::before` overlay `#00000073`, image `/sk/uploads/large_Adobe_Stock_206118370_5ab61dcb89.jpg` cover z -2; tag "Cas client" (white text, border #fff3); title "Arcitek - Présentation corporate" `FKScreamer 4rem/700/lh .9/uppercase/#fff`, `display:block; margin-top:1.3rem`.
- `[MENU-B1]` `grid-column:7/10; display:flex; flex-direction:column; justify-content:space-between; gap:1.6rem; padding-block:2.4rem` (727,108 335x756.9):
  - nav "Explorer": title `vInter max(1.2rem,12px)/600/lh 1.5rem/uppercase, opacity .5, margin-bottom max(1.2rem,12px)`; routes `vInter 3.2rem/500/lh 1.3` (28.1/36.5px), color drk1: Réalisations `/realisations`, Nous connaître `/nous-connaitre`, Notre méthode `/la-methode-labas`, Ressources `/ressources`, Contact `/contact`, Offres d'emploi `/nos-offres-d-emploi`. Item `overflow:hidden`; nav padding-right 3.1rem. Hover: inner title `transform: matrix(1,0,0,1,10,0); color:#6630ff; transition: transform,color 1.5s cubic-bezier(.13,.93,.13,.93) .03s`.
  - `[MENU-C1]` (flex column gap 1.6rem): address "Paris, Bordeaux, Verdun, Aix-en-Provence, Rennes, Strasbourg" `vInter 1.5rem/400/1.4, white-space:pre-wrap`; `hr` `border:max(.1rem,1px) solid rgba(18,0,66,.2)`; socials (LinkedIn https://www.linkedin.com/company/laboiteaslides/, Vimeo https://vimeo.com/laboiteaslides?fl=pp&fe=sh) icons 2rem, gap 1.6rem.
- Expertises nav `grid-column:10/12; padding-block:2.4rem; padding-left:4.8rem` (1076,108): title "Expertises" (as above); routes `vInter 1.5rem/500/1.4`: Présentations `/expertises/presentations-powerpoint`, Communication 360 `/expertises/communication-360`, Navigation App Like `/expertises/navigation-interactive-powerpoint`, Animatiques `/expertises/Animatiques-powerpoint`, Conférences Interactives `/expertises/conferences-interactives`, Séminaire VR `/expertises/seminaire-realite-virtuelle`, Solutions IA `/expertises/solutions-ia-powerpoint`, Formations & Coaching `/expertises/formations-powerpoint-coaching-labas-agence-powerpoint`.

Menu motion (desktop). Open → simultaneously: loader closes over page (§2 "show", .7s power2.out); `W` timeline (paused, restart):
```
reset state: panel progress 0; lang {scale:1.07, autoAlpha:0}; titles {autoAlpha:0}; explore routes {y:"130%", scale:1.05};
             expertise routes {x:15, scale:1.05, autoAlpha:0}; address {x:-10,y:-10,scale:.95,autoAlpha:0};
             separator {x:-20, scaleX:0, autoAlpha:0} (transform-origin left); socials {x:-10,y:-10,scale:.95,autoAlpha:0}
W.to(panelProgress,{progress:1, duration:2, ease:"custom::out"}, 0)
 .to(lang,{scale:1, autoAlpha:1, duration:1.7, ease:"custom::out"}, .35)
 .to(titles,{autoAlpha:.5, duration:2, ease:"custom::out"}, .15)
 .to(exploreRoutes,{y:"0%", scale:1, duration:2.7, stagger:.09, ease:"custom::out"}, "<+=.07")
 .to(expertiseRoutes,{x:0, scale:1, autoAlpha:1, duration:2.7, stagger:.09, ease:"custom::out"}, "<")
 .to(address,{x:0,y:0,scale:1,autoAlpha:1, duration:2.3, ease:"custom::out"}, .3)
 .to(separator,{x:0, scaleX:1, autoAlpha:1, duration:2.3, ease:"custom::out"}, .35)
 .to(socials,{x:0,y:0,scale:1,autoAlpha:1, duration:2, stagger:.05, ease:"custom::out"}, .4)
G = gsap.timeline({paused:true, delay:.1}); widget i: G.to(wProg[i],{progress:1, duration:2.9, ease:"custom::out"}, .2*i)
```
3D swing applied as inline transform `matrix3d(1,0,0,0, 0,A,-O,0, 0,O,A,0, 0,TY,TZ,1)` with `A = lerp(cos θ0, 1, p)`, `O = lerp(sin θ0, 0, p)`, `TY = cubicBezier(y0,y1,y2,y3; p)`, `TZ = cubicBezier(z0..z3; p)`:
- background panel: θ0 = −0.15 rad; TY control points = [−1.5, −1.7, 0.1, 0] × lvh; TZ = [0, −1000, 100, 0] px → drops in from ~1.5 screens above, tilted, swinging forward.
- each widget: θ0 = +0.1 rad; TY = [1, 0, 0, 0] × lvh; TZ = [0, 0, 100, 0] px → rises from one screen below.
Close → `gsap.fromTo(menu,{y:"0%",scale:1},{y:"-100%",scale:.95,duration:.5,ease:"power2.out"})`, then reset; loader reopens page (§2 hide with 1.5s power2.out). Lenis is stopped while open.
Mobile menu: only `fromTo(menu,{y:"-100%",scale:.95},{y:"0%",scale:1,duration:.5,ease:"power2.out"})` (reverse on close); layout single column (`grid-column:1/13`, rows: B1, expertises, widgets; A1 `overflow-y:auto` with top fade mask `linear-gradient(180deg,transparent 0,red 3.2rem)`; B1 gap 4.8rem; lang switcher `left:3.2rem`).

---------------------------------------------------------------------------------------------------

## 2. Loader `app-loader._loader_3fgap` (first child of #HEADER, z-index 1)

- `position:fixed; top:0; left:0; z-index:1; width:100vw; height:100lvh; --loaderRadiusX:100%; --loaderRadiusY:min(150rem,100vh)`; `.@show{pointer-events:auto}`.
- Two `loader-panel` children (both identical purple, absolute, 100%×100%, `background-color:#6630ff`), the last one is `display:flex; center` and contains the spinner. Panel mask (exact):
```
mask-image:
 radial-gradient(ellipse var(--loaderRadiusX,100%) var(--loaderRadiusY,0) at 50% calc(33.33333% + var(--loaderRadiusY,0px)*2/6), red 100%, transparent 100%),
 linear-gradient(180deg, transparent calc(33.33333% + var(--loaderRadiusY,0px)*2/6), blue calc(33.33333% + var(--loaderRadiusY,0px)*2/6),
                 blue calc(66.66667% - var(--loaderRadiusY,0px)*2/6 + var(--loaderRadiusY,0px)), transparent calc(66.66667% - var(--loaderRadiusY,0px)*2/6 + var(--loaderRadiusY,0px))),
 radial-gradient(ellipse var(--loaderRadiusX,100%) var(--loaderRadiusY,0) at 50% calc(66.66667% - var(--loaderRadiusY,0px)*2/6 + var(--loaderRadiusY,0px)), transparent 100%, green 100%);
mask-position:50% 50%; mask-size:100% calc(300% + var(--loaderRadiusY,0px)*2); mask-repeat:no-repeat; mask-composite:add,intersect;  (-webkit-: source-over,source-in,xor)
```
  (a 3-screen-tall mask whose middle third is opaque with a domed top edge and a dome-shaped hole at the bottom edge).
- Spinner `panel-spinner` (3.1rem square, `animation: aLoad 3.5s infinite, delay -1.4s`; hidden + paused unless `@animated`): `::before`/`::after` are 0×0 boxes with `border:1.55rem solid` forming two white right triangles: before `top:-1.55rem;left:-1.55rem;border-color:transparent #fff #fff transparent; animation aBeforeLoad`; after `top:1.55rem;left:1.55rem;border-color:#fff transparent transparent #fff; animation aAfterLoad`. Keyframes: aLoad `0% {timing cubic-bezier(.87,.07,.87,.07)} 50% {rotate(180deg); timing cubic-bezier(.13,.93,.13,.93)} 100% {rotate(1turn)}`; aBeforeLoad 50% `translate3d(-7px,-7px,0) rotate(-45deg)`; aAfterLoad 50% `translate3d(7px,7px,0) rotate(-45deg)`, both back to `translateZ(0) rotate(0)` at 100%.
- Sequence: page shows the purple panel + spinner until the app LOAD event (measured: window load ≈5.1s, hide tween start ≈5.7–6.0s on a cold load). Hide (initial load): `gsap.fromTo(panels.reverse(), {"--loaderRadiusX":"70%","--loaderRadiusY":`${min(lvh,1500)}px`, maskPosition:"50% 50%"}, {"--loaderRadiusX":"100%","--loaderRadiusY":"0px", maskPosition:"50% 100%", duration:1, ease:"power2.in"})`; onComplete re-set `{70%, min(lvh,1500)px, maskPosition:"50% 0%"}` (parked above). Visually: the purple sheet slides up off the page and its bottom edge is a dome (convex) that flattens as it leaves; underneath, the 3D intro (§3.5) is already playing. Hide after menu close: same tween but `duration:1.5, ease:"power2.out"`. Show (menu open): `gsap.to(panels,{"--loaderRadiusX":"100%","--loaderRadiusY":"0px", maskPosition:"50% 50%", duration:.7, ease:"power2.out"})` (comes down from the parked `50% 0%` position).

---------------------------------------------------------------------------------------------------

## 3. Hero `header._header_jx0rq` (y 0 → 6 300) + WebGL scene

### 3.1 DOM / CSS (desktop `@whole`)
```
section#HOME
  header._header_jx0rq.superFont.@whole.@color[drk1]   height:700lvh (6300px); pointer-events:none
    app-title.header__title  FKScreamer 16.4rem/700/lh .75/uppercase — position:absolute; opacity:0  (SEO only; the visible title is 3D)
        span "Les meilleures idées font " + strong.@color[drk1] "l'avenir"
        span.@align[right] "Quand elles sont bien " + strong.@color[drk1] "présentées"
    h1.header__subtitle  position:fixed; top:50%; left:50%; transform:translate3d(-50%,-50%,0); width:65rem; max-width:100%
        vInter 5.2rem / 600 / letter-spacing -.04em / line-height 1.04 / center / color #120042
        "La boite à slides® :<br>seule agence au monde<br>certifiée ISO 9001<br>qui transforme Powerpoint<br>en un puissant levier d'impact<br>pour votre business"
        (measured 434.6,298.5 570.7x293.9; 6 lines of 47.5px, line boxes start y 303/350.5/398/445.5/493.6/542.2)
    app-widgets (§3.2)
```
Header element itself scrolls normally (not sticky); the visible hero is the fixed canvas + fixed subtitle + fixed widgets.

### 3.2 Hero widget (video) — `app-widgets._widgets_p9yei.@whole`
- `position:fixed; top:0; left:0; width:100vw; height:100dvh; padding:2.4rem; box-sizing:border-box; display:flex; align-items:flex-end; justify-content:space-between; backdrop-filter:blur(0)`; `--transformer-height:22rem`.
- Mask (scroll reveal-away):`mask-image: radial-gradient(ellipse 70% 20% at 50% 60%, transparent 100%, red 0), linear-gradient(180deg, red 60%, transparent 0); mask-position:50% var(--progress,0); mask-size:100% 250%; mask-composite:intersect`. `::after { content:""; position:absolute; top:0; left:0; width:100%; height:100%; z-index:2; transform:translate3d(0, calc(100% - var(--progress,0%)),0) }`.
- `[WIDGETS-A1]` flex, align center, gap 1.2rem (21.1,685.8 323.1x193.2):
  - `app-transformer` 30rem × 22rem (263.4x193.2), z 1, `position:relative`; container absolute `transform-origin:top left`; inner A2 `position:relative; max-width:max-content`.
  - `video` (`/sk/uploads/home_video_SD_79c96be094.mp4`, autoplay, loop, muted, playsinline, preload eager, mounted 3 frames after LOAD): `width:100%; height:100%; border-radius:1.2rem; object-fit:contain; background:#ffffff1a; cursor:pointer` (rendered 257.5x193.2, 4:3).
  - "go" round button 5.6rem `lightGlass` with plus icon (1.6rem), aria-label "Afficher en pleine écran" (295,757.8).
- Scroll badge (last child, bottom-right, 1302.9,780.5): svg (see assets) `width:11.1rem; color:#ffffff80; transform:translate3d(0,2rem,0); animation: rotate to 1turn 2s cubic-bezier(.36,.84,.72,.28) infinite`.
- Motion:
  - Intro: `gsap.fromTo(A1,{y:20,scale:1.03,autoAlpha:0},{y:0,scale:1,autoAlpha:1, delay:max(3.5 − secondsSinceAppAlive,0), duration:7, ease:"custom::out"})` once the video has metadata (A1 has class `@hide` = visibility hidden until then).
  - Scroll (header timeline track 0 → .5 ⇒ scrollY 0 → 2700): `--progress = p*100 %`, `transform: scale(1 + .15p)`; on leave (y>2700) class `@hide` → `display:none`.
  - Click video/go → fullscreen: Transformer tweens container to the widgets' inner rect (inset 2.4rem, full viewport) `{x,y,width,height, duration:2, ease:"custom::out"}`; widgets get `@up` (z-index 6, `background-color:#12004280`, transitions .7s ease-out, mask forced to `50% 0`, scale 1), video unmuted, Lenis stopped; close button (round lightGlass, xmark, top 2.4rem right 2.4rem, label "Fermer") reverses to `(0,0,100%,100%)`.

### 3.3 Hero timeline (`HEADER`), trigger = header, start `0% 0`, end `100%+=900 900` ⇒ scrollY 0 → 6300; s = 0, o = .857, c = .143
| Item | timeline | scrollY |
|---|---|---|
| Background layer 2 (white) uTransition2 0→1, uCurveAmount2 .3→0, ease none | 0 → .4 | 0 → 2160 |
| Widgets `--progress` / scale | 0 → .5 | 0 → 2700 |
| Title A mask-out, line 2 "L'AVENIR" (constant step(1)→step2(1)) | .08 → .16 | 432 → 864 |
| Title A mask-out, line 1 "IDÉES FONT" | .10 → .18 | 540 → 972 |
| Title A mask-out, line 0 "LES MEILLEURES" | .12 → .20 | 648 → 1080 |
| Title B line 0 "QUAND ELLES" rises z: H−LH → −LH | .26 → .33 | 1404 → 1782 |
| Title B line 1 "SONT BIEN" rises | .28 → .35 | 1512 → 1890 |
| Title B line 2 "PRÉSENTÉES" rises | .30 → .37 | 1620 → 1998 |
| Title B mask-out line 2 / 1 / 0 | .48→.55 / .50→.57 / .52→.59 | 2592→2970 / 2700→3078 / 2808→3186 |
| Both 3D titles visible | 0 → .75 | 0 → 4050 (hidden after) |
| Camera P0→P1 / P1→P2 / P2→P3 | 0→.4 / .4→.6 / .6→.9 | 0→2160 / 2160→3240 / 3240→4860 |
| Camera P3→P4 | start 1, overflowEnd 1 | 5400 → 6300 |
| Triangles children $(1): p0→p1, r0→r1 | 0 → .6 | 0 → 3240 |
| Triangles children $(2): p1→p2 (frame layout), r1→r2 | .6 → .9 | 3240 → 4860 |
| Triangles group rotation r0→r1 with ease t³ | .6 → .9 | 3240 → 4860 |
| Subtitle lines linesSlide(y): {y:20,autoAlpha:0}→{0,1}, itemDuration .15 (power1.out) | .75 → .99 | 4050 → 5346; each of 6 lines lasts 810px, stagger 97.2px |
| Subtitle fade out (autoAlpha 1→0) | start 1, overflowEnd .7 | 5400 → 6030 |
All 3D mask/rise tweens use default ease power1.out. Lerps in tracks are linear in progress unless noted.

### 3.4 Scene recipe (three r181)
Renderer & camera
- `<canvas id="SYNTHRA">` `position:fixed; top:0; left:0; width:100vw; height:100lvh; z-index:-1` (behind #MAIN). `WebGLRenderer({antialias:true, powerPreference:"high-performance"})`, `outputColorSpace = LinearSRGBColorSpace`, `toneMapping = NoToneMapping`, `localClippingEnabled = true`, `setPixelRatio(min(devicePixelRatio, Windows/Linux ? 2 : 1.5))`, size = innerWidth × lvh.
- `PerspectiveCamera(45, vw/lvh, 0.1, 500)`, always `lookAt(0,0,0)` after every position change (Euler order 'XZY'). Mouse parallax: camera additive rotation `x = J(clientY/lvh), y = J(clientX/vw)` with `J(e)= (e<.5 ? (2e)²−1 : 1−(1−2(e−.5))²)·1e-3` rad (tiny).
- Post: `EffectComposer(renderer, WebGLRenderTarget(vw,lvh,{samples:min(2,maxSamples)}))` → `RenderPass` → `ShaderPass(RGBShiftShader)` with `angle = 2`, `amount = 0.00128` (always on desktop; that is the magenta/cyan fringing visible on the title and triangle edges).
- Environment: `RGBELoader().load('/assets/hdr/studio_small_08_1k.hdr')`, `mapping = EquirectangularReflectionMapping`, `scene.environment = tex`. No lights.
- **Transform smoothing (important for feel):** every animated object stores target = canonical + noisy + shaken + physical offsets; each frame `value += (target − value)·(1 − e^(−10·dt))` (dt in s). Tracks set targets; the render lags ~0.1s behind scroll.

Background gradient (fullscreen quad inside the same scene: `PlaneGeometry(2,2)`, ShaderMaterial, `depthWrite:false, depthTest:false, frustumCulled:false, renderOrder:-10`; it is what the glass refracts)
- Vertex: `gl_Position = vec4(position.xy, 0., 1.)`, pass `vUv`.
- Uniforms: `uTime += dt (s)`, `uSpeed .06, uCurveSharpness 10, uNoiseStrength .12, uWaveFrequency 2.3, uWaveAmplitude .59, uWaveSpeed .06, uParallax .15`; base layer top `#FFFFFF` bottom `#EDEDED`.
- Fragment (verbatim logic):
```glsl
vec3 linearToSrgb(vec3 l){ return mix(l*12.92, pow(l, vec3(1./2.4))*1.055-.055, step(.0031308, l)); }
float computeCurvedLineMask(float transition, float curveSharpness, float curveAmount, float uvX, float uvY){
  if (transition <= 0.) return 0.;
  float nx = (uvX-.5)*2.; float curveOffset = nx*nx*curveAmount;
  float baseHeight = mix(-abs(curveAmount), 1., transition);
  float curveHeight = clamp(baseHeight - curveOffset, 0., 1.);
  float edgeSmooth = .015*(10.-curveSharpness);            // = 0 → hard edge
  return 1. - smoothstep(curveHeight-edgeSmooth, curveHeight+edgeSmooth, uvY); }
float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453123); }
float noise(vec2 p){ vec2 i=floor(p), f=fract(p); float a=hash(i), b=hash(i+vec2(1,0)), c=hash(i+vec2(0,1)), d=hash(i+vec2(1,1));
  vec2 u=f*f*(3.-2.*f); return mix(a,b,u.x)+(c-a)*u.y*(1.-u.x)+(d-b)*u.x*u.y; }
void main(){
  float wave1 = sin((vUv.x + uTime*uWaveSpeed)*uWaveFrequency)*uWaveAmplitude;
  float wave2 = sin((vUv.x*1.7 - uTime*uWaveSpeed*1.3)*(uWaveFrequency*.6) + vUv.y*3.14159)*(uWaveAmplitude*.6);
  float waveOffset = wave1 + wave2;
  float scroll = fract(vUv.y + waveOffset + uTime*uSpeed); float curvedScroll = pow(scroll, 1.2);
  vec3 g = mix(linearToSrgb(uColorBottomInitial), linearToSrgb(uColorTopInitial), curvedScroll);
  // for each layer k in order:  g = mix(g, mix(linearToSrgb(uColorBottom_k), linearToSrgb(uColorTop_k), curvedScroll),
  //                                    computeCurvedLineMask(uTransition_k, uCurveSharpness, uCurveAmount_k, vUv.x, vUv.y));
  float grain = noise(vec2(vUv.x*4. + waveOffset*2., vUv.y*4. + uTime*.25)); g += (grain-.5)*uNoiseStrength;
  float vignette = smoothstep(1.1, .35, distance(vUv, vec2(.5))); g *= mix(.85, 1.05, vignette + uParallax*waveOffset);
  gl_FragColor = vec4(g, 1.); }
```
  Colors are `new THREE.Color('#hex')` uniforms (linear), converted back by `linearToSrgb` → exact hex on a LinearSRGB output.
- Home layers (in this order; each has its own uTransition_k, init 0, and uCurveAmount_k, init .3): 1 PRM, 2 LGH, 3 SCD, 4 LGH, 5 TRT, 6 LGH, 7 BLK, 8 LGH, 9 DRK, 10 LGH. Layer 1 starts at transition 1, curve 0 (page top = solid purple gradient). Each transition rises a new gradient from the bottom with a domed edge (center higher by `curve`), the dome flattening as curve → 0.
- Layer schedule in my scope (ease none): L2 white 0→2160 (hero); L3 green 5670→6840 (tagline: end .15, ovStart .7); L4 white 9900→10800 (tagline: start 1, ovEnd 1); L5 cyan 14630→15656 (skills: end .1, ovStart .7); L6 white 19221→20120 (skills: start 1, ovEnd 1). (L7–L10 belong to VR / label cards, other agent.)

3D title (plugin TITLE) — two groups, A = "LES MEILLEURES / IDÉES FONT / L'AVENIR", B = "QUAND ELLES / SONT BIEN / PRÉSENTÉES" (strings from i18n, `.toUpperCase()`), both at the origin.
- Font `FontLoader('/assets/fonts/FK Screamer Legacy Upright_Regular.json')`. `TextGeometry(text,{font, size:9.5, depth:0.1, curveSegments:8, bevelEnabled:false})`, then `computeBoundingBox(); translate(−(max.x+min.x)/2, −B, 0)`.
- Metrics (from ascender 1275 / descender −253 / resolution 1000): `HEIGHT = (1275+253)/1000·9.5 = 14.516`; `B = HEIGHT/2 + (−253/1000·9.5) = 4.8545`; `LINE_HEIGHT = .71·HEIGHT = 10.30636`.
- Lines: material `MeshBasicMaterial({side:FrontSide, transparent:false, depthWrite:true, depthTest:true, clipShadows:true})`, `renderOrder 2`, rotation `[−π/2, 0, 0]` (lying flat, readable from the camera above). Positions: line0 `[0, .99, −LH]`, line1 `[0, 1, 0]`, line2 `[0, 1.01, +LH]`.
  Colors: A = `#FFFFFF, #FFFFFF, #120042`; B = `#120042, #120042, #6630FF`.
- Each line has one clipping plane `Plane(normal (0,0,−1), constant)` (visible where z < constant). `maskStep(i) = LH·(.5+i) + (HEIGHT−LH)/2` ⇒ i=−1: −3.04836, i=0: 7.25800, i=1: 17.56436; `maskStep2(i) = maskStep(i) − HEIGHT` ⇒ −17.56436 / −7.25800 / 3.04836.
  - "Rise in": animate line `position.z` from `z+HEIGHT` → `z` (text slides up from under its own mask edge).
  - "Wipe out": animate plane `constant` from maskStep(i) → maskStep2(i) (mask edge moves up over the text while the text stays put).
- Group B lines start at `z+HEIGHT` (hidden) and rise during the hero scroll (§3.3).

Glass triangles (plugin TRIANGLES) — group `TRIANGLES_3D` with 22 meshes sharing ONE material.
- Shape: right isosceles triangle with legs 10 (pts (0,0),(10,0),(0,10)); each edge shortened by .05 at both ends and corners closed with `quadraticCurveTo(vertex)` (tiny rounding). `ExtrudeGeometry(shape,{depth:1, bevelEnabled:true, bevelThickness:.045, bevelSize:.3, bevelSegments:5, curveSegments:20})`. Origin = the right-angle corner (pivot is NOT centered). `castShadow = true`, `renderOrder = 1`.
- Material: `MeshPhysicalMaterial({color:0xffffff, metalness:0, roughness:.2, transparent:true, transmission:1, ior:1.7, thickness:6, specularIntensity:1, envMapIntensity:.6, clearcoat:1, clearcoatRoughness:.1, dispersion:0, attenuationColor:0xffffff, attenuationDistance:3.5, iridescence:0, iridescenceIOR:1.3, depthWrite:true})`. Opacity of the shared material is animated (fade out in works, fade in in skills).
- Idle bob: every frame `t += dt`; each triangle i adds a noisy position `y = .5·sin(phase_i + t)`, `phase_i = random()·2π`.
- Group keyframes (`DATA_TRIANGLES_3D`): p0 [0,0,0], p1 [−40,0,0], p2 [17,5,0], p3 [3,5,0], p4 [27,0,−11]; r0 [π/2,0,0], r1 [π−.5667292175235062,0,0], r2 [π,0,0], r3 [π,.5,−.1], r4 [π,.15,0].
- Per-child keyframes p0…p11 / r0…r11: see `CLONE_SPEC_A_ASSETS.md` (JSON). Camera keyframes (`DATA_CAMERA_3D`): P0 [0,80,1], P1 [0,60,30], P2 [0,40,60], P3 [0,35,55], P4 [0,25,35], P5 [−20,22,33], P6 [−5,−3,−20], P7 [−20,0,0], P8 [0,0,1].
- `$(k[, fade])` = per child lerp `p(k−1)→pk`, `r(k−1)→rk` by progress; fade `'out'` sets material.opacity = 1−p, `'in'` = p, otherwise forces opacity 1.

### 3.5 Load intro (runs once on LOAD if the hero timeline progress < 1; concurrent with the loader hide)
Initial "grid" layout (function `zt`): b = bounding size of one triangle mesh (≈10.6×10.6); `cw = b.x+1.7`, `ch = b.y+1.7`, `pitchX = cw+1.2`, `pitchY = ch+1.2`, `x0 = (−pitchX·5+1.2)/2`, `y0 = (−pitchY·3+1.2)/2`; maxD = |(x0+4·pitchX, y0+2·pitchY)|. 15 slots (5 columns × 3 rows, slot t → col t%5, row ⌊t/5⌋); slot→(childA, childB) pairs `[-1,-1, 3,13, 12,9, 21,19, -1,-1, 10,1, 11,18, 14,17, 4,8, 2,5, -1,-1, 20,16, 6,0, 15,7, -1,-1]` (−1 = empty: the 4 corner slots). For slot t: `gx = x0 + (t%5)·pitchX`, `gy = y0 + pitchY·⌊t/5⌋`, `dz = (t odd ? −13 : 13)`:
- A: grid offset target `p1 = (gx, gy, −55) − canonical p0`; start `p0 = p1 + (gx<0 ? −6 : 6, gy<0 ? −2 : 2, dz)`; rotation offset `r0 = (near(rX)−rX, near(rY)−rY, near(rZ)−rZ)` where `near(v)` = whichever of {0, 2π} is closer to v (so the grid pose is flat/unrotated); `delay = |(gx,gy)|/maxD·.07 + ((A·17+7)%97)/97·.055`.
- B: at `(gx+cw, gy+ch)`; start offset `(0, y<0 ? −2 : 2, dz)`; rZ offset uses whichever of {π, 3π} is closer (B is flipped 180° so A+B form a square); `delay = |(gx+cw, gy+ch)|/maxD·.07 + ((B·17+16)%97)/97·.055 + .007`; `duration = 1 − delay`.
(Grid lives in group-local z = −55, i.e. world y ≈ +55 because the group is rotated π/2 about X → a flat checkerboard of glass squares just under the camera.)
Tweens (on `{progress}` proxies, default ease power1.out unless noted), all start at intro t=0:
1. 7.7s: group shaken position `(0, −10e, 3e)`, `e = (1−p)³`.
2. 1.5s: each child shaken position = lerp(start, grid, n), `n = 1−(1−p)³` (squares settle into the grid).
3. delay 1.1s, 7s: per child `i = clamp((p−delay)/duration)`, `a = 1 − home::custom::out(i)`; shaken position = gridOffset·a, shaken rotation = r0·a → squares split into two triangles each and fly out to their scattered canonical p0 poses (center first).
4. delay .9s, 4.7s: title A shaken position `(0, 50e, 15e)`, shaken rotation `(−1.3e, 0, 0)`, `e = (1−p)⁴` (title starts nearer the camera, lower and tilted, settles).
5. Title A lines `position.z` from `z+HEIGHT` → `z`: duration 4.3s, ease custom::out, delays .9 / 1.1 / 1.3 s for lines 0/1/2.
Settled hero (y=0): purple gradient, 22 glass triangles scattered around, 3-line title centered (white, white, dark), video widget fading in bottom-left, scroll badge bottom-right (screenshot cross-check: f010–f032 frames).

### 3.6 Scroll story (what is on screen)
- 0–1080: camera rises/tilts P0→P1; title A wiped out bottom-up line by line (L'AVENIR first, 432–864); triangles drift p0→p1; white gradient dome rises from bottom (0–2160), widget masked away with the same dome motion.
- 1404–1998: title B "QUAND ELLES / SONT BIEN / PRÉSENTÉES" (drk1, drk1, prm1) rises into view on the now-white background; header turns dark ≈2000.
- 2592–3186: title B wiped out. 3240–4860: camera to P3, triangle group rotates (t³ ease) and children animate into the **frame layout** (screen-edge border of triangles/squares around an empty center). Frame layout (`layoutFrame`, recomputed on resize, writes children p2 in group-local x/y): `[w,h] = visible rect at distance |P3|=√(35²+55²)=65.19 minus depth 1` (fov 45, current aspect); `ax = max(w/2, 10·2+1.4·3)`, `ay = max(h/2, 10·2+1.4·2)`; corners k=0..3 with signs `(sx,sy) = (−1,1),(−1,−1),(1,−1),(1,1)` and child indices per corner `[18,11,16,10,1,−], [3,20,12,13,14,9], [19,8,21,2,4,−], [7,17,15,5,0,6]`; with `X=ax·sx, Y=ay·sy, x1=X−10·sx, y1=Y−10·sy`: c0 → (X,Y); c1 → (x1−1.4sx, y1−1.4sy); c2 → (x1−2.8sx, Y); c3 → (X, y1−2.8sy); for odd k: c4 → (−.7, y1−1.4sy), c5 → (.7, y1−1.4sy); for even k: c4 → (X−1.4sx, 0).
- 4050–5346: subtitle lines fade/slide in inside the frame; 5400–6030 subtitle fades; camera P3→P4 (5400–6300).

---------------------------------------------------------------------------------------------------

## 4. Tagline sticker `section._sticker_1b402._tagline_x672m.@whole` (y 6 300 → 10 800, 4500px)

### 4.1 DOM / CSS
```
section.sticker.@native.tagline (position:relative; pointer-events:none; height:500lvh)   — Sticker: fragCount 1, fragHeight 500
  div.[STICKER-A1].sticker__track.tagline__track.superGrid @columns[12] @gb[32] @gi[16] superFont @family[inter]
     position:sticky; top:0; height:100lvh; overflow:visible!important; padding-top:15.2rem; padding-bottom:5.6rem; children pointer-events:auto
     h2.tagline__track-title  grid-column:1/7 — vInter 5.2rem / 600 / -.04em / lh 1.04, color #120042
        "Notre agence PowerPoint amplifie le retentissement des présentations stratégiques des leaders. On équipe ceux qui veulent faire bouger les lignes, dans tous les secteurs"
        (7 lines @1440: "Notre agence PowerPoint" / "amplifie le retentissement" / "des présentations" / "stratégiques des leaders. On" / "équipe ceux qui veulent faire" / "bouger les lignes, dans tous" / "les secteurs"; line boxes 562.5 wide, 47.5 tall, first line top = track top + 133.5)
     p.tagline__track-content  grid-column:9/12; align-self:flex-end — vInter 1.5rem / 500 / lh 1.4, color #120042
        "Nos clients ont des idées fortes, des stratégies à partager, des messages complexes à faire passer.\nAvec des contenus interactifs et des expériences captivantes, ils offrent à leur cible ce qu’il y a de plus puissant : l’évidence."
        (919.2 x, 274.2 wide, 113.3 tall, bottom 5.6rem above viewport bottom)
  iframe (about:blank; used only as intersection/resize sentinel — not needed in clone)
```
Pinned (sticky) from scrollY 6 300 to 9 900.

### 4.2 Timeline (`TAGLINE`) trigger = sticker; overflowStart = overflowEnd = lvh ⇒ scrollY 5 400 → 10 800 (T 5400; s = c = .1667, o = .6667)
| Item | scrollY |
|---|---|
| BG L3 green in (uTransition3 0→1, curve .3→0) | 5670 → 6840 |
| Triangles group p0→p1 [−40,0,0] (end 0, ovStart .7) | 5670 → 6300 |
| Children $(3) p2→p3 | 5670 → 6300 |
| Camera P4→P5 (start 0, ovEnd .7) | 6300 → 10530 |
| Group p1→p2 and r1→r2 | 6300 → 10530 |
| Children $(4) p3→p4 (row along x, "fence") | 6300 → 7200 |
| Children $(5) p4→p5 (all rotations converge to r5 [−1.129,1.421,2.433]) | 7200 → 9000 |
| Title lines linesSlide '-x' ({x:−20,autoAlpha:0}→{0,1}), start .15 end .63 itemDuration .27 | 6840 → 8568; each line 972px, stagger 126px |
| Content lines linesSlide 'y' ({y:20,autoAlpha:0}→0/1), .35 → .7, itemDuration .17 | 7560 → 8820; each line 612px |
| Content parallax y 20 → −20 (power1.out) | 7560 → 9900 |
| Title + content fade out (autoAlpha 1→0), .87 → 1 | 9432 → 9900 |
| BG L4 white in (start 1, ovEnd 1) | 9900 → 10800 |
Visual: green gradient fills from bottom while triangles swing into a single row of upright glass panes ("fence") running across the lower half in perspective; text appears top-left, small paragraph bottom-right; white dome rises again at the end.

---------------------------------------------------------------------------------------------------

## 5. Works `section._works_15dfr.@whole` (y 10 800 → 13 822.4)

### 5.1 DOM / CSS
```
section.works.@whole.superGrid @columns[12] @gb[56] @gi[16]   padding-top:60vh (540px); margin-bottom:10.9rem
  h2.works__title  grid-column:7/12; word-break:break-word — FKScreamer 11.2rem / 700 / lh .8 / uppercase, color #120042
     "Un seul outil, des " + strong.superFont.@color[prm1] "possibilités infinies"
     lines @1440: "UN SEUL OUTIL," / "DES POSSIBILITÉS" / "INFINIES" (line height 78.7px, width 466.4; top 11 340, height 255.7)
  nav.workCardsPanoramic.superGrid @columns[2] @gb[8] @gi[8]   grid-column:1/13 (top 11 644.8, 1139 x 2177.6)
     a.workCardsPanoramic__link (grid-column:span 1) > section.workCard  ×8
```
Cards (each 566.1 × 539.3 @1440, `aspect-ratio:569/542`; rows at 11 644.8 + n·546.3):
| # | title (h3) | tag | href | img (origin) | --bgImage (thumbnail) |
|---|---|---|---|---|---|
|0|Safran Electronics & Defense|Corporate|/realisations/Safran-Electronics-Defense-presentation-corporate|/sk/uploads/Safran_0239f5157e.jpg|thumbnail_Safran_0239f5157e.jpg|
|1|Adidas|Masque|/realisations/adidas-masque-powerpoint|Adidas_2_20aaceff99.jpg|thumbnail_Adidas_2_20aaceff99.jpg|
|2|Marriott|Commerciale|/realisations/marriott-presentation-commerciale-interactive|Touchscreen_Mariott_la_boite_a_slides_agence_powerpoint_0415bcab60.jpg|thumbnail_…|
|3|LIPTON|Évènement|/realisations/lipton-presentation-evenement-selling-story|Ekaterra_Tea_Lipton_43f10e2e06.jpg|thumbnail_…|
|4|Brasseries Kronenbourg|Interactions Live|/realisations/brasseries-kronenbourg-presentation-evenementielle-gamification|Brasseries_kronenbourg_sceno_72f519a001.jpg|thumbnail_…|
|5|Nissan|Marketing|/realisations/nissan-presentation-marketing|Nissan_ef41272a76.jpg|thumbnail_…|
|6|Viridien|Finance|/realisations/viridien-presentation-financiere-resultats-annuels|Viridien_e87722da36.jpg|thumbnail_…|
|7|Upciti|Masque|/realisations/upciti-masque-powerpoint|Upciti_82768aec88.jpg|thumbnail_…|
Card CSS: `display:flex; flex-wrap:nowrap; align-items:flex-end; gap:1.6rem; padding:3.2rem; border-radius:3.2rem; overflow:hidden; position:relative; z-index:1; aspect-ratio:569/542`; `::before` bottom gradient `bottom:0; height:20rem; width:100%; background:linear-gradient(0deg, rgba(0,0,0,.7) 0, transparent); z -1`; `[WORK_CARD-A1]` `max-width:60%; flex-shrink:0; overflow:hidden`; title `FKScreamer 4rem / 700 / lh .9 / uppercase / #fff`; categories `display:flex; flex-wrap:wrap; gap:.8rem 1.6rem`; tag `height:4rem; padding-inline:1.6rem; gap:.8rem; border:max(.1rem,1px) solid #fff3; border-radius:1.6rem; vInter 1.5rem/500/1.4; #fff; white-space:nowrap`. `[WORK_CARD-A2]` absolute inset, z −2: `::before` = `background:var(--bgImage) 50%/cover; transform: matrix(calc(1+var(--scale)),0,0,calc(1+var(--scale)),calc(var(--x)*-2),calc(var(--y)*-2))`, `::after` = `backdrop-filter:blur(var(--blur))`; `img` `object-fit:cover; border-radius:3.2rem; transform: matrix(calc(1-var(--scale)),0,0,calc(1-var(--scale)),var(--x),var(--y))`.
Card hover (desktop): mouseenter → targets `scale .3, blur 50px`; mousemove → `x = (offsetX − w/2)·.03`, `y = (offsetY − h/2)·.03` (px); mouseleave → after 250ms all targets 0. Each frame `v += (target − v)·(1 − e^(−7·dt))` written to CSS vars `--x --y --scale --blur(px)` (photo shrinks to 70% while its blurred thumbnail fills behind, parallax-follows cursor). Title hover: split words; clone placed after; on enter words `y:100% → 0%` while clone words `0% → −100%, opacity 1→0`, `duration 2.5, stagger .045, ease custom::out`.

### 5.2 Motion
Timeline `WORKS`, trigger = section, overflowStart = overflowEnd = lvh ⇒ 9 900 → 13 822.4 (T 3922.4; s = c = .2295; o = .541):
| Item | scrollY |
|---|---|
| Title `y: −lvh/2 (−450px) → 0` (end .1, ovStart .7, power1.out) | 10170 → 11012 |
| Title wordsRise (6 words, stagger .05·B; color #6630FF → own color) | 10170 → 11225 (word 367px, stagger 137.6px) |
| Triangles group p2→p3, r2→r3, eased `1−(1−t)³` (end .5, ovStart 1) | 9900 → 11861 |
| Children $(6,'out') p5→p6 + material opacity 1→0 | 9900 → 11861 |
| Camera P5→P6 (.6 → .9) | 12073 → 12710 |
Cards (tween, not timeline): `gsap.fromTo(links, {y:"25%", scale:.95}, {y:"0%", scale:1, stagger:.1, duration:.7, ease power1.out, scrollTrigger:{trigger:nav, start:"0% 100%" (=10 745), toggleActions:"play none none reverse"}})`.
After 11 861 no triangles are visible; background white.

---------------------------------------------------------------------------------------------------

## 6. Method `section._method_1bww9.@whole` (y 13 918.1 → 15 163.8)

### 6.1 DOM / CSS
```
section.method.@whole.superGrid @columns[12] @gb[103] @gi[16]   grid-template-rows:1fr auto auto auto 1fr; padding-top:20rem; margin-bottom:11rem
  app-marquee.method__marquee  grid-column:1/13; grid-row:2; width:100%; display:flex; justify-content:center; align-items:center  (layout top 14 184.1, height 210.2)
    marquee-clipper (position:relative; width:100vw; flex-shrink:0; overflow:hidden; display:flex; align-items:center)
      marquee-track (display:flex; width:fit-content; backface-visibility:hidden; transform matrix3d(..., tx, 0, 0, 1))
        marquee-driver ×2 (min-width:100vw; white-space:nowrap; width:fit-content)
          h2.method__marquee-title  display:flex; align-items:flex-start; padding-right:4rem — FKScreamer 25.2rem / 700 / lh .75 / uppercase / #6630FF
             app-icon size 8 (child height 20rem) .title__icon (overflow:hidden; margin-right:4rem; color #70F74A) > svg.triangleMirror (32x32, two triangles)
             app-title "Depuis 2002 ● ISO 9001 ● 5/5 Note Google Avis ● +8 000 projets ● 85% de réachat ● MOS PowerPoint"
             (.word:not(:last-child)::after { content:" "; white-space:pre })     one driver = 7 478.8px wide @1440
  p.method__tagline  grid-column:1/7; grid-row:3 — vInter 5.2rem / 600 / -.04em / lh 1.04 / #120042
     "Tirer parti des dernières avancées technologiques et intelligences artificielles pour valoriser vos messages les plus importants"
     (5 lines: "Tirer parti des dernières" / "avancées technologiques et" / "intelligences artificielles pour" / "valoriser vos messages les" / "plus importants")
  div.[METHOD-A1]  grid-column:8/13; grid-row:4; align-self:flex-end; display:block   (x 823.1, w 466.4)
     p  vInter 2.4rem / 500 / -.02em / lh 1.3 — "À la boite à slides, on maximise l'engagement de votre public depuis 2002. On repousse les limites de PowerPoint pour vous faire gagner en impact, en performance et en autonomie. Pour votre plus grande satisfaction."
     ul.method__metrics  display:flex; flex-direction:column; gap:.8rem; margin-top:1.6rem; padding-top:1.6rem; border-top:max(.1rem,1px) solid rgba(18,0,66,.07) — vInter 1.5rem/500/1.4
        li (display:flex; gap:.8rem) icon size 2 (2rem) svg.checkmarkBadge + text:
          "La seule agence PPT au monde certifiée ISO 9001" / "85% de réachat" / "5/5 Note Google Avis" / "Certifiés Microsoft Office Specialist PowerPoint"
```
Rows @1440 (layout, without transforms): marquee 14 184.1–14 394.3; tagline 14 484.7 (+120 parallax at start); METHOD-A1 bottom aligned to row 4.

### 6.2 Motion
- Marquee loop: track `translateX` from 0 to −(trackWidth/2) every 30 s (linear, restart), only while intersecting; transform written as `matrix3d(1,0,0,0, 0,1,0,0, 0,0,1,0, D + X, 0, 0, 1)` with `D = (vw − trackWidthOfOneDriverAtRotation0)/2` (≈0 for wide text). 
- Marquee chars: charsIn on each title (icon + chars), trigger = marquee, start "0% 100%", toggle play/reverse (§0.4).
- Timeline `METHOD`, trigger = section, overflowStart = overflowEnd = lvh ⇒ 13 018 → 15 163.8 (T 2145.7; s = c = .4194; o = .1611):
| Item | scrollY |
|---|---|
| Marquee parallax y 200 → −200 (ovStart .6, ovEnd .5) | 13378 → 14713 |
| Tagline parallax y 120 → −120 (ovStart .5, ovEnd .7) | 13468 → 14894 |
| Content `p` parallax y 40 → −40 (ovStart .2, ovEnd 1) | 13738 → 15164 |
| Tagline lines linesSlide '-x', itemDuration .7 (ovStart .25, ovEnd .2) | 13693 → 14444 (line 525px, stagger 56.4px) |
| Content lines linesSlide 'y', itemDuration .7 (ovStart .05, ovEnd .4) | 13873 → 14624 (line 525.7px) |
- Metrics: maskReveal(ul, 200, 90) (scrub, start "0% 90%", end "100%+=200 90%").
- No 3D content (background white).

---------------------------------------------------------------------------------------------------

## 7. Skills sticker `app-sticker._skills_18hah.@whole` (y 15 260.5 → 20 120.5; + margin-bottom 50vh → expertises at 20 570.5)

### 7.1 DOM / CSS
```
app-sticker.sticker.@native.skills.@whole (height:540lvh = 4860px — fragCount 3, fragHeight 180 ⇒ 180 + 180·2; margin-bottom:50vh)
  div.[STICKER-A1].sticker__track.skills__track.superGrid @columns[2] @gb[103] @gi[16]  (sticky top 0, height 100lvh, overflow hidden)
     div.[SKILLS-A1] (grid-column:1; grid-row:1; empty — the 3D pinwheel occupies this half)
     ul > li.skills__track-skill ×3 (grid-column:2; grid-row:1 — all stacked; display:flex; flex-direction:column; gap:3.2rem; align-self:center)  x 727, w 562.5
        h3.skill__title  vInter 5.2rem / 600 / -.04em / lh 1.04 / #120042; padding-right:3.2rem
        ul.skill__labels (display:flex; flex-wrap:wrap; gap:.8rem) > li.superGlass @blur[24] @background[lgh]  padding:.8rem 3.2rem; border-radius:1.6rem (bg #ffffff1a, blur 24px)
             app-icon size 6 (6.4rem tall) img, `filter: brightness(.8) sepia(1) invert(1) hue-rotate(45deg)`
             icons: /sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg (alt "Certification ISO9001 LABAS"), Badge_simple_MOS_LABAS_d0815bc7cf.svg, Logo_simple_Avis_Google_LABAS_d3f7b5bccc.svg (alt "Avis Google")
        (item 3 only) a.cta → /realisations : UIActionCTA darkGlass (round 5.6rem arrow + pill "Voir nos réalisations"; bg #12004212, blur 24px, color #120042)
```
Texts: 1 "0 retard sur +8 000 projets. Nous utilisons la rigueur de l'ISO 9001 pour sécuriser vos calendriers." (labels ISO, MOS, Google) — 2 "96% de stabilité de l'enveloppe budgétaire. Notre méthode vise la justesse dès le départ pour respecter votre budget." (same 3 labels) — 3 "La preuve ultime d'un rendu maîtrisé ? Un taux de réachat de 85% auprès des directions marketing, qui nous renouvellent leur confiance au cours de l'année." (CTA). Measured item 1: 727,305.9 562.5x288.2 (title 199 tall, labels 70.2 tall each 102–110 wide).

### 7.2 Motion — timeline `SKILLS`, trigger = sticker, overflowStart = overflowEnd = lvh ⇒ 14 360.5 → 20 120.5 (T 5760; s = c = .15625; o = .6875). Step = .08, frag = .92/3 = .30667.
| Item | timeline | scrollY |
|---|---|---|
| BG L5 cyan in (end .1, ovStart .7) | | 14630 → 15656 |
| Camera P6→P7 (end .08, ovStart .5) | | 14810 → 15577 |
| Group p3→p4 (end .2, ovStart .7) | | 14630 → 16052 |
| Group r3→r4, children $(7,'in') p6→p7 + opacity 0→1 (end .08, ovStart .5) | | 14810 → 15577 |
| Children $(8) p7→p8 (pinwheel assembles) | .08→.15 | 15577 → 15854 |
| Children $(9) p8→p9 | .3867→.4567 | 16792 → 17069 |
| Children $(10) p9→p10 | .6933→.7633 | 18006 → 18283 |
| Children $(11) p10→p11, then group hidden on leave (start 1, ovEnd .7) | | 19221 → 19850 |
| Skill k title: linesSlide 'x' ({x:20,autoAlpha:0}→{0,1}), itemDuration .14, ease power2.out | i=.08+.30667k → i+.2 | k0 15577→16369, k1 16792→17584, k2 18006→18798 |
| Skill k labels + CTA fade in, itemDuration .14, ease power2.in | i+.03 → i+.2 | k0 15749→16369, … |
| Skill k fade out (whole li), ease power2.in | (i+.28667−.14) → (i+.28667) | k0 16158→16713, k1 17372→17927, k2 18587→19141 |
| BG L6 white in (start 1, ovEnd 1) | | 19221 → 20120 |
Visual: cyan gradient; on the left half 4 glass triangles (children 18–21) arranged as a pinwheel/square, re-arranging slightly at each skill step; the other 18 triangles are parked off-screen at [80|100,0,200]; text on right half swaps item by item.

---------------------------------------------------------------------------------------------------

## 8. SEO modal (`app-modal._modal_1jk12.@stillReadable._seoModal_1lyt7` containing `section._content_1uvg3`)
Hidden dialog opened from the footer info trigger (other agent). `position:fixed; top:0; left:0; width:100vw; height:100dvh; overflow:hidden auto; background:#120042c4; backdrop-filter:blur(24px); transition: opacity .17s ease-in`; hidden state `z-index:-3; visibility:hidden; opacity:0`; shown `z-index:6`. `[MODAL-A1]` `superDevice superGrid @columns[12] @gi[16]`; close button round 5.6rem, `top:3.2rem; right:3.2rem`, xmark 2rem. Content `grid-column:3/11; padding-block:20rem` (mobile `1/13; max-width:93rem; margin-inline:auto`), `vInter 1.6rem/400/lh 1.6, color #fff`. Rich text: `h2 FKScreamer 6rem/700/lh 1/uppercase, margin-block 2.4rem`; `h3 3rem/500/lh 110%, margin-block 2rem`; `h4 2.4rem/500/.02em/130%, margin-block 1.6rem`; `p margin-bottom 4rem; p+p margin-top −2rem`; lists `padding-left 2.4rem; margin-bottom 2.4rem; li margin-block .4rem`; `a color #6630ff; 500; underline`; media `margin-block 7.2rem; border-radius 1.6rem`; blockquote `border-left .4rem solid #29daff; padding .4rem 3.2rem`. Text content: copy from `reference/original.html` (section `_seoModal__content_1lyt7_46`, starts with h2 "La boite à slides®, agence PowerPoint et activateur d'impact.").

---------------------------------------------------------------------------------------------------

## 9. Mobile (390×844, html 7px) — differences
- No 3D scene content and no scroll timelines/animations (all gated on "whole"); the canvas still renders only the base background gradient (#FFF → #EDEDED). Marquee still loops. Menu = simple slide (§1.5).
- Header: grid `auto auto; justify-content:space-between`, CTA hidden (`display:none`), A1 padding 0 2rem (14px). Logo 14,24.2 86.8x33.6; trigger 286,22.4 90x39.2. Header height 84px.
- Hero (`:not(.@whole)`): `position:relative; min-height:100lvh; margin-inline:-2rem; padding:20rem 2rem; background:#6630ff; color #fff` (height 1425.3). HTML title visible: FKScreamer 16.4rem (114.8px) / 700 / **lh .8** / uppercase / white, `max-width:93rem; margin-inline:auto; margin-bottom:10.3rem; word-break:break-word`; blocks `display:block; max-width:min(55rem,100%)`, first block `margin-bottom:10.3rem`, second block `margin-left:auto; text-align:right`; strong (l'avenir / présentées) `display:block; color #120042`. Subtitle 4rem (28px) / 600 / -.04em / 1.04 / center / white (y 1110.6). Widgets: `position:absolute; width:100%; height:calc(100% + 22rem + 2.4rem); clip-path: polygon(0 0,100% 0,100% calc(100% − 22rem − 2.4rem),0 calc(100% − 22rem − 2.4rem))`; A1 `position:sticky; top:calc(100svh − 22rem − 2.4rem)` (video card 30rem×22rem bottom-left), no go button, no scroll badge.
- Tagline: `margin:0 -2rem 20rem; padding:0 2rem 15.2rem; background:#62f740` (y 1425.3, h 662.5); track `@gb[103]`, `grid-template-rows:1fr auto auto 1fr; max-width:93rem; margin-inline:auto; padding-top:15.2rem`; title (4rem) and content full width rows 2/3; height fit-content (not pinned).
- Works: title `grid-column:1/13; max-width:93rem; margin-inline:auto` (4.0 → 11.2rem FKScreamer = 78.4px); cards 1 column (`@columns[1]`), each 362×344.8; second (duplicate) title hidden.
- Method: marquee 16.4rem lh .8, `justify-content:flex-start; margin-inline:-2rem`, icon size 7 (13.2rem); tagline and A1 `grid-column:1/13; justify-self:center; width:100%; max-width:93rem`; tagline 4rem.
- Skills: `display:flex; justify-content:center; align-items:center; margin-inline:-2rem; padding-block:15.2rem; background:#29daff` (y 6203.1, h 1128.4, not pinned); track `width:100%; max-width:93rem`; SKILLS-A1 hidden; items span 2, even items `align-items:flex-end; text-align:right`; title max-width 80%; 4rem.
- Order/ys @390: header 0–1425, tagline 1425–2088, works 2228–5316, method 5392–6126, skills 6203–7331, expertises 7331.

---------------------------------------------------------------------------------------------------

## 10. Notes / not reproducible from measurement
- The GLB (`DECIMATE v2…glb`, a VR headset; 24 meshes, KHR_mesh_quantization, webp textures, no Draco) is loaded at init but only appears in the VR section timeline (y ≥ 21 172, other agent). Its recipe for reference: group VR_MASK p0 [17,−38,0] r0 [0,0,π/2−.3] s0 [50,50,50] → p1 [17,−27,0] r1 [0,0,π/2−.5] → p2 [−11.24,−2.43,4.3] r2 0 → p3 [−26.5,−1.7,4.8] → p4 [−30,−1.5,5] → p5 [−40,−1.7,5.2]; meshes Object_183/181/157 made transparent; Object_195 gets the glass MeshPhysical (envMap = HDR, transmission 1, ior 2, thickness .5, roughness .1, clearcoat 1, depthWrite false, DoubleSide).
- Exact loader timing depends on network (the app waits for all assets + `__app_addWait` promises); measured ≈0.9s between window `load` and loader hide on a cold load.
- Triangle idle bob uses `Math.random()` phases and the intro uses random-free hashed delays; positions are otherwise deterministic.
- Header cards "light" region and frame layout depend on viewport size; recompute on resize.
