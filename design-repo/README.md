# Design-repo: La boîte à slides, FR homepage

This folder is a machine-validated description of how the cloned homepage looks and behaves. It covers tokens, primitives, components, section contracts, the page template, compatibility rules, the PageSpec schema and validators. An LLM can use it to produce new on-brand page compositions without inventing colours, copy or structure. It also cannot reuse the source company's identity.

The source is the React clone in the parent folder: the French homepage of `https://laboiteaslides.fr/`, a real presentation-design agency. The stack is recorded only as provenance, in `registry.manifest.json` → `sourceStack`. No contract depends on it.

> **Real company, real content.** The logos, client photos, people, testimonials, certifications, copy and display typeface belong to La boîte à slides and its clients. They are allowed as evidence in `mode: "reference"` only. A `mode: "generated"` PageSpec is rejected if it contains any of them (`schema/semantic_validate.py`, `GENERATED_MODE_*`). Keep this repo private.

## Status

- `status: design-review-pending`, `productionApproved: false`. Production approval is a separate human sign-off and has not been given.
- **Approved by the owner on 2026-11-06** (Riya Ghosh, verbatim decision: "approve"; recorded in `extraction/human-decisions.json`):
  1. The wrapper-gate whitelist for `hero.statement` (6300 px at 1440x900, a 700lvh scroll-scrubbed opener). See `extraction/measured-values.json` → `wrapperGate.whitelist`.
  2. The parity exception for `story.vr`, which scored 0.69 and 0.71 in two runs against a 0.80 gate. The live and clone WebGL thumbnail spheres place different thumbnails; the DOM layer is identical. See `extraction/measured-values.json` → `parity.exceptions`.
  3. The design-policy classification: `n0-design-constraints-common` 0.1.0, category `agency-marketing-site` (`policy/design-policy.json` → `approval`).
- `verify_all.py` accepts an approved item only when a record in `extraction/human-decisions.json` covers it and names the same human approver. An agent never adds those records on its own.

## Counts (recomputed by the builder; `verify_all.py` checks them)

<!-- counts:start -->
| Field | Count |
| --- | --- |
| tokens | 152 |
| sections | 19 |
| primitives | 9 |
| components | 13 |
| templates | 1 |
| routes | 1 |
| assetRoles | 27 |
| generationSafeAssetRoles | 14 |
| retrievalIneligibleSections | 4 |
| motionPatterns | 23 |
| graphRules | 9 |
| examplePageSpecs | 2 |
<!-- counts:end -->

## Scope

- **One route, one template.** The clone serves only `/`, and it maps to `template.home`, which has 19 ordered nodes. Every other link in the source (expertises, réalisations, ressources, contact, legal…) points at the original site's routes. Those pages are **not built**, so no template was invented for them.
- **Sections are semantic units.** `footer#FOOTER` is split into two sections:
  - `conversion.closing-cta`: the closing question and the contact CTA.
  - `chrome.footer`: the navigation panel.

  The SEO modal's long prose is broken up at its own headings. `ia.json` in the parent folder still lists 18 sections. That difference is recorded in `extraction/measured-values.json` → `iaReconciliation`.
- **Runtime UI is not retrievable.** These sections are `retrievalEligible: false`, and the setting is pinned in code:
  - `chrome.loader` (the load curtain)
  - `chrome.menu-overlay` (the navigation overlay)
  - `chrome.seo-modal` (a hidden dialog)
  - `backdrop.webgl-scene` (a fixed canvas with no content of its own; sections pick its look through `tokens.surfaceTone`)

## Layout

```text
registry.manifest.json   status, counts, versions, category + design policy, entry points (all inside this folder)
tokens/                  00-foundation (colour, typography, radius, spacing, breakpoint, elevation, icon-size, motion,
                         motion-patterns), 10-semantic, 20-component, 30-layout, themes/light.json,
                         llm/ (component-allowlist, token-catalog, token-policy)
primitives/ components/  building blocks with props, tokens and evidence
sections/                19 section contracts: source{} provenance + semantic{} taxonomy, content schema with maxWords,
                         motion + reduced-motion fallback, responsive, surface tones, asset roles, retrievalEligible
templates/templates.json template.home (structured nodes: required / repeatable) + route table
compatibility/graph.json rhythm / position rules (error | warn), enforced under the same ids by the validator
assets/asset-roles.json  closed asset-role vocabulary, availability reference-only | generation-safe | blocked-for-generation
policy/                  source-identity.json (brand, domains, CTAs, copy shingles, claims, people, clients), design-policy.json
schema/                  pagespec.schema.json (Draft-07), section-contract.schema.json, example.pagespec.json (reference),
                         examples/generated.home.pagespec.json (fictional), semantic_validate.py, tests/adversarial_test.py
extraction/              build_repo.py (builder), verify_all.py, wrapper_gate.py, prove_drift.py, policy_hash.py,
                         measured-values.json (citation + measurement ledger), raw measurement dumps,
                         measure_sections.mjs, style_histogram.mjs, parity/ (capture.mjs, compare.py, results-run*.json)
```

## Run the checks

You need Python 3.9 or later and `jsonschema`. The parity harness additionally needs Pillow and numpy.

```bash
python3 extraction/verify_all.py               # schema, sync, allowlist, counts, catalog, pins, gate, citations, copy
python3 schema/semantic_validate.py --schema schema/example.pagespec.json schema/examples/generated.home.pagespec.json
python3 schema/tests/adversarial_test.py        # every mutation rejected, every control passes
python3 extraction/prove_drift.py               # every injected drift caught by verify_all
python3 extraction/wrapper_gate.py              # R9 gate alone
```

The design-repo also works on its own (zipped or copied without the clone). In that case, the citation, copy-fidelity and source-pin checks become warnings and everything else still runs. With the parent clone present, they are hard checks.

To rebuild after the clone changes (R16), run `python3 extraction/build_repo.py`. It needs the parent clone. Citations are found by needle, so line numbers re-point automatically. Then re-run every check above, re-measure heights and parity, and bump the version in `CHANGELOG.md`.

### Measuring and parity (optional; needs a headless Chromium through `playwright-core`)

```bash
# the clone: npm ci && npm run dev  (serves http://127.0.0.1:5181/)
BASE_URL=http://127.0.0.1:5181/ node extraction/measure_sections.mjs > <scratch>/heights.json
SIDE=clone URL=http://127.0.0.1:5181/ OUT_DIR=<scratch>/run/clone node extraction/parity/capture.mjs
SIDE=live  URL=https://laboiteaslides.fr/ OUT_DIR=<scratch>/run/live OFFSETS=<scratch>/run/clone/geometry.json node extraction/parity/capture.mjs
python3 extraction/parity/compare.py --live <scratch>/run/live --clone <scratch>/run/clone --label runN --out extraction/parity/results-runN.json
```

Optional environment variables:

- `PLAYWRIGHT_MODULE`: the module to import. Defaults to `playwright-core`, resolved by Node from the current directory upwards.
- `CHROME_PATH`: a specific browser binary.
- `GL=gpu|swiftshader`: the WebGL backend.

The live site renders its "fit" (non-3D) layout when it falls back to software WebGL, so parity was captured with `GL=gpu`. In that mode the live and clone layouts were identical: 35 940 px tall, with every section top equal.

How parity is captured:

- **Metric:** both screenshots are downsampled 4x. A pixel matches when its largest channel difference is ≤ 24/255. A section's score is the mean over 1 shot, or 3 shots at 25/50/75 % of a tall section's scroll range. The gate is every section ≥ 0.80 and the average ≥ 0.80.
- **Consent banners:** the live site's consent banner is never clicked. Fixed consent overlays would be hidden identically on both sides; none were found.
- **Screenshots:** live screenshots are not committed. Only the text-free result JSON is.

Parity results, from `extraction/parity/results-run1.json` and `results-run2.json`:

<!-- parity:start -->
| Section | run1 | run2 | Δ |
| --- | --- | --- | --- |
| chrome.footer | 0.8795 | 0.9172 | 0.0377 |
| content.faq | 0.99 | 0.9905 | 0.0005 |
| content.resources | 0.9727 | 1.0 | 0.0273 |
| conversion.closing-cta | 0.9245 | 0.9416 | 0.0171 |
| hero.statement | 0.9912 | 0.9944 | 0.0032 |
| offer.expertises | 1.0 | 1.0 | 0.0 |
| offer.skills | 0.9153 | 0.9396 | 0.0243 |
| offer.spotlight | 0.9977 | 1.0 | 0.0023 |
| proof.labels | 0.8587 | 0.8643 | 0.0056 |
| proof.method | 0.8629 | 0.8824 | 0.0195 |
| proof.reviews | 0.9973 | 0.9977 | 0.0004 |
| proof.works | 0.994 | 0.9997 | 0.0057 |
| story.tagline | 0.9225 | 0.9337 | 0.0112 |
| story.vr | 0.6898 | 0.7074 | 0.0176 |
| **average** | 0.9283 | 0.9406 |  |
<!-- parity:end -->

## Generated mode in one paragraph

A generated PageSpec has these properties:

- **Brand and people:** a fictional or user-supplied brand (`brand.isFictional: true`), and fictional people.
- **Assets:** only generation-safe asset roles, for example `brand.placeholder-mark`, `media.generated-image`, `person.fictional-avatar` or `credential.placeholder-badge`. Placeholder credentials and ratings must be marked `isPlaceholder: true`.
- **Links:** relative links, or links on reserved `.example` / `.invalid` / `.test` hosts.
- **Copy:** original copy.
- **Fonts:** `fonts.display` must be `font.family.text`, because the display typeface is licensed.

The validator rejects any of the following:

- the source brand, its domains or its social profiles;
- its CTA strings;
- any 6-word run of its copy, or any of its distinctive headings;
- its statistics, certifications or ratings;
- the names of its reviewers or clients;
- any reference-only or blocked asset;
- store marks or store links.

`schema/examples/generated.home.pagespec.json` is the passing control ("Northlight Decks", a fictional studio).

## What this repo does not contain

- No IR or IR schema; none was requested.
- No `prefers-reduced-motion` handling exists in the source. The `reducedMotionFallback` values are requirements set by this repo. They are grounded in the source's own mobile "fit" layouts.
- No `node_modules`, build output, live screenshots or saved copy of the original site. `design-repo.zip` sits next to this folder, is regenerated last, and is gitignored.
