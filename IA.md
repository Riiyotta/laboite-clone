# https://laboiteaslides.fr/ (FR homepage) → clone at /src (React + Vite + Tailwind v3, three r181, GSAP, Lenis)

Source: https://laboiteaslides.fr/ (FR homepage) → clone at /src (React + Vite + Tailwind v3, three r181, GSAP, Lenis)
Status: **measured-from-live-site; bottom-half sections still in build**
1 routes · 1 templates · 18 unique sections

> Generated from `ia.json` by `build.mjs`. Edit the JSON, not this file.

## Shape of the site

The largest 1 template (Homepage (FR)) accounts for 1 of 1 routes (100%). The remaining 0 routes span 0 templates.

| template | routes | share |
|---|---:|---:|
| Homepage (FR) | 1 | 100% |

## Page chrome

**1 routes carry chrome = `full`** — Homepage (FR).

## Sections by reuse

How widely a section is shared determines whether it belongs in a shared
component library or stays local to its page.

| section | category | templates | routes | implementation | scope |
|---|---|---:|---:|---|---|
| `backdrop.webgl-scene` | BACKDROP | 1 | 1 | `scene/Scene.jsx (engine.js, home.js, background.js, triangles.js, title.js)` | Present on the one homepage route, behind every other section; on mobile only a static white-to-grey gradient is drawn. |
| `chrome.header` | CHROME | 1 | 1 | `Header.jsx` | Fixed at the top of the one homepage route for its full length. |
| `chrome.loader` | CHROME | 1 | 1 | `header/Loader.jsx` | Shown once on first load of the homepage route and reused as the purple frame behind the menu overlay. |
| `chrome.menu-overlay` | CHROME | 1 | 1 | `header/Menu.jsx` | Overlay available from the header on the one homepage route. |
| `chrome.seo-modal` | CHROME | 1 | 1 | `hero/SeoModal.jsx` | Mounted once on the homepage route, closed by default. |
| `chrome.footer` | CHROME | 1 | 1 | `Footer.jsx` | Closes the one homepage route, rendered outside main#MAIN. |
| `hero.statement` | HERO | 1 | 1 | `Hero.jsx` | First section of the one homepage route. |
| `story.tagline` | STORY | 1 | 1 | `Tagline.jsx` | Second section of the homepage route. |
| `proof.works` | PROOF | 1 | 1 | `Works.jsx` | Homepage route only. |
| `proof.method` | PROOF | 1 | 1 | `Method.jsx` | Homepage route only. |
| `offer.skills` | OFFER | 1 | 1 | `Skills.jsx` | Homepage route only. |
| `offer.expertises` | OFFER | 1 | 1 | `Expertises.jsx` | Homepage route only. |
| `story.vr` | STORY | 1 | 1 | `Vr.jsx` | Homepage route only. |
| `offer.spotlight` | OFFER | 1 | 1 | `Spotlight.jsx` | Homepage route only. |
| `content.resources` | CONTENT | 1 | 1 | `ResourceCards.jsx` | Homepage route only. |
| `proof.labels` | PROOF | 1 | 1 | `LabelCards.jsx` | Homepage route only. |
| `proof.reviews` | PROOF | 1 | 1 | `ReviewCards.jsx` | Homepage route only. |
| `content.faq` | CONTENT | 1 | 1 | `Faq.jsx` | Homepage route only, last section before the footer. |

**0 shared sections** appear in more than one template and belong in a component library.

**18 single-use sections** appear in exactly one template. Building these
as "reusable" components up front would be speculative — keep them page-local
until a second caller actually appears.

## Templates

### Homepage (FR) — `template.home`

1 route · `/` · chrome: **full**

| # | category | section | |
|---:|---|---|---|
| 1 | BACKDROP | `backdrop.webgl-scene` | page-local |
| 2 | CHROME | `chrome.loader` | page-local |
| 3 | CHROME | `chrome.header` | page-local |
| 4 | CHROME | `chrome.menu-overlay` | page-local |
| 5 | HERO | `hero.statement` | page-local |
| 6 | CHROME | `chrome.seo-modal` | page-local |
| 7 | STORY | `story.tagline` | page-local |
| 8 | PROOF | `proof.works` | page-local |
| 9 | PROOF | `proof.method` | page-local |
| 10 | OFFER | `offer.skills` | page-local |
| 11 | OFFER | `offer.expertises` | page-local |
| 12 | STORY | `story.vr` | page-local |
| 13 | OFFER | `offer.spotlight` | page-local |
| 14 | CONTENT | `content.resources` | page-local |
| 15 | PROOF | `proof.labels` | page-local |
| 16 | PROOF | `proof.reviews` | page-local |
| 17 | CONTENT | `content.faq` | page-local |
| 18 | CHROME | `chrome.footer` | page-local |

## Section reference

### CHROME

_Site-wide fixed or overlay UI that is not part of the scrolling story: header bar, loader, menu overlay, modal, footer._

**`chrome.header`** — Fixed 12rem header bar: logo link, centred 'Menu/Fermer' glass trigger with clip-path text swap, 'Demander un devis' CTA; switches between light and dark designs from the backdrop colour.

· Fixed at the top of the one homepage route for its full length. · appears on 1 routes · implemented by `Header.jsx`

**`chrome.loader`** — Purple three-layer-mask loader panel with a two-triangle spinner; lifts on load (triggers the 3D intro) and closes behind the menu when it opens.

· Shown once on first load of the homepage route and reused as the purple frame behind the menu overlay. · appears on 1 routes · implemented by `header/Loader.jsx`

**`chrome.menu-overlay`** — White rounded panel opened from the header trigger with a 3D swing: navigation links, FR/EN switch, 'Conférences interactives' expertise widget, white-paper and client-case resource widgets.

· Overlay available from the header on the one homepage route. · appears on 1 routes · implemented by `header/Menu.jsx`

**`chrome.seo-modal`** — Hidden dialog holding long-form SEO rich text, opened from a footer link.

· Mounted once on the homepage route, closed by default. · appears on 1 routes · implemented by `hero/SeoModal.jsx`

**`chrome.footer`** — footer#FOOTER: 'PRÊT À TRANSFORMER VOTRE IMPACT?' glass panel with cursor-following glow and label tooltips, FR/EN switch, office cities, navigation and legal links.

· Closes the one homepage route, rendered outside main#MAIN. · appears on 1 routes · implemented by `Footer.jsx`

### BACKDROP

_The fixed full-screen WebGL canvas behind the page that draws backgrounds, glass triangles, 3D titles and the VR scene._

**`backdrop.webgl-scene`** — Fixed canvas#SYNTHRA (z-index -1): gradient background shader with 10 domed colour layers, RGB-shift post pass, 22 glass triangles (intro checkerboard, frame, fence, pinwheel), clipped 3D FKScreamer titles, camera keyframes, VR headset GLB and 80-tile thumbnail sphere. Also computes the header light/dark state.

· Present on the one homepage route, behind every other section; on mobile only a static white-to-grey gradient is drawn. · appears on 1 routes · implemented by `scene/Scene.jsx (engine.js, home.js, background.js, triangles.js, title.js)`

### HERO

_The opening scroll-driven statement of the page._

**`hero.statement`** — 700lvh header: visually-hidden SEO title ('Les meilleures idées font l'avenir / Quand elles sont bien présentées' — visible version is 3D in the backdrop), fixed subtitle 'La boite à slides® : seule agence au monde certifiée ISO 9001…' that fades in mid-scroll, and the bottom-left video widget with Scroll badge. Position at 1440x900: y 0 → 6300.

· First section of the one homepage route. · appears on 1 routes · implemented by `Hero.jsx`

### STORY

_Pinned (sticky) scroll-scrubbed narrative blocks whose content animates with scroll progress._

**`story.tagline`** — 500lvh pinned block: large 'Notre agence PowerPoint amplifie le retentissement…' statement sliding in line by line on the left, small paragraph bottom-right, over the green backdrop and triangle 'fence'. Position at 1440x900: y 6300 → 10800.

· Second section of the homepage route. · appears on 1 routes · implemented by `Tagline.jsx`

**`story.vr`** — 600lvh pinned 'DÉPASSEZ TOUTES LES LIMITES DE POWERPOINT' block: VR headset flies through the camera, near-black backdrop cut, sphere of project thumbnails the camera ends inside, curved white wipe out. Position at 1440x900: y ≈ 21173 → 26573.

· Homepage route only. · appears on 1 routes · implemented by `Vr.jsx`

### PROOF

_Evidence blocks: case studies, credentials, metrics, testimonials._

**`proof.works`** — 'UN SEUL OUTIL, DES POSSIBILITÉS INFINIES' title plus 8 case-study cards (Safran, Adidas, Marriott, Lipton, Kronenbourg, Nissan, Viridien, Upciti) with staggered reveal and cursor-following image hover; the card grid forces the header to light. Position at 1440x900: y 10800 → 13822.

· Homepage route only. · appears on 1 routes · implemented by `Works.jsx`

**`proof.method`** — 30s looping marquee of credentials ('DEPUIS 2002 ● ISO 9001 ● 5/5 NOTE GOOGLE AVIS ● +8 000 PROJETS ● 85% DE RÉACHAT ● MOS…') with character reveal, tagline/paragraph with parallax and a mask-revealed metrics list. Position at 1440x900: y 13918 → 15164.

· Homepage route only. · appears on 1 routes · implemented by `Method.jsx`

**`proof.labels`** — 500lvh pinned 'ENGAGÉS POUR LA QUALITÉ' block: three glass label cards (5 étoiles Google Avis, Certifié ISO 9001:2015 Bureau Veritas, Microsoft Office Specialist) flying right-to-left on a curved path. Position at 1440x900: y ≈ 28290 → 32790.

· Homepage route only. · appears on 1 routes · implemented by `LabelCards.jsx`

**`proof.reviews`** — 'ILS NOUS FONT CONFIANCE' draggable slider of 7 client testimonials with momentum, edge resistance and prev/next buttons. Position at 1440x900: y ≈ 32966.

· Homepage route only. · appears on 1 routes · implemented by `ReviewCards.jsx`

### OFFER

_Blocks describing what the agency sells._

**`offer.skills`** — 540lvh pinned block of 3 stacked skill items each sliding in and fading out, with a 'Voir nos réalisations' split button, over the cyan backdrop and triangle pinwheel. Position at 1440x900: y 15260 → 20120.

· Homepage route only. · appears on 1 routes · implemented by `Skills.jsx`

**`offer.expertises`** — 'NOS EXPERTISES' list of large labels (Présentations, Communication 360, Navigation app like, Séminaire VR, Solutions IA) at low opacity that light up and pop a photo at the right viewport edge on hover. Position at 1440x900: y ≈ 20570.

· Homepage route only. · appears on 1 routes · implemented by `Expertises.jsx`

**`offer.spotlight`** — 'TOUJOURS CARRÉS. JAMAIS FORMATÉS.' statement with a parallaxing image (+300 → −300px). Position at 1440x900: y ≈ 26573.

· Homepage route only. · appears on 1 routes · implemented by `Spotlight.jsx`

### CONTENT

_Editorial and help content: resources, FAQ._

**`content.resources`** — 'NOS DERNIÈRES RESSOURCES' row of article, client-case and white-paper cards (white paper shown as a rotated mockup) that pop in once and reverse on scroll back. Position at 1440x900: y ≈ 27376.

· Homepage route only. · appears on 1 routes · implemented by `ResourceCards.jsx`

**`content.faq`** — 'DES QUESTIONS? ON VOUS RÉPOND' accordion (several questions can be open at once, as on the live site) of 16 questions (6 shown, +6 per 'Voir plus de questions') with cursor-bending string dividers and a scroll mask reveal. Position at 1440x900: y ≈ 33820.

· Homepage route only, last section before the footer. · appears on 1 routes · implemented by `Faq.jsx`
