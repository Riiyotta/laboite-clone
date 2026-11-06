# La boîte à slides — homepage clone

React + Vite + Tailwind v3 clone of the French homepage of https://laboiteaslides.fr/ (three r181, GSAP + ScrollTrigger, Lenis), for local study. Only `/` is cloned; every other link points at the original site's routes.

```bash
npm install
npm run dev        # http://127.0.0.1:5181/
```

## Information architecture

`ia.json` is the only IA file to hand-edit. `IA.md` and `matrix.csv` are **generated**; don't edit them.

```bash
node validate.mjs && node build.mjs
```

What the data shows:

- **One template, one route, 18 sections.** None of them is shared, because there is only one page. Reuse questions only arise once a second page is cloned. The obvious candidates are `chrome.header`, `chrome.footer`, `chrome.menu-overlay` and `chrome.loader`.
- **About 25 600 of the roughly 36 000 px of scroll (about 70%) belong to five scroll-scrubbed sections:**
  - `hero.statement`
  - `story.tagline`
  - `offer.skills`
  - `story.vr`
  - `proof.labels`

  Their visible content is mostly drawn by `backdrop.webgl-scene` and driven by scroll progress, not laid out in the DOM. Fidelity work on those sections is therefore mostly scene work.
- The `CHROME` category (6 sections) is the site-wide shell. The other 12 sections are the homepage's scroll story.

## Other files

- `CLONE_SPEC_A.md` / `CLONE_SPEC_B.md`: measured spec for the top and bottom halves, including typography, layout and motion values.
- `CLONE_SPEC_A_ASSETS.md`: inline SVGs and triangle keyframes.
- `public/`: assets downloaded from the original, at their original URL paths.
- `reference/`: the original's SSR HTML and JS bundles, kept as evidence.

Assets, copy, logos and client case studies belong to La boîte à slides and its clients. Keep this clone local; don't deploy it publicly.
