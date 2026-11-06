# Changelog

## 1.0.0 — 2026-11-06 — initial build (Situation A)

Built against clone commit `f6c2801`. The FR homepage is the only route the clone serves.

### Added

- **Tokens:** 152 tokens across colour, typography, radius, spacing, breakpoint, elevation, icon size, motion, semantic, component and layout. Every one is cited by needle into `src/`, `tailwind.config.js` or `CLONE_SPEC_*.md`. Also added:
  - `motion-patterns.json`, with 23 patterns and their reduced-motion fallbacks;
  - `themes/light.json`;
  - `tokens/llm/token-catalog.json`, derived from the token files;
  - `tokens/llm/token-policy.json`, with node slots, theme combinations and the licensed font.
- **Building blocks and contracts:**
  - 9 primitives and 13 components;
  - 19 section contracts, each with a `source{}`/`semantic{}` split, `retrievalEligible`, a content schema with `maxWords`, closed motion with a locked reduced-motion fallback, structured responsive notes, surface tones and asset roles.
- **Template and rules:**
  - `templates/templates.json`: 1 template and 1 route. Other source links are documented as not built.
  - `compatibility/graph.json`: 9 rules. The same-category and consecutive-stage exceptions were read off the real node order.
- **Assets and policy:**
  - `assets/asset-roles.json`: 27 roles (13 reference-only or blocked, 14 generation-safe). Availability is pinned in code.
  - `policy/source-identity.json`: the R2 registry, built from the real source.
  - `policy/design-policy.json`: `n0-design-constraints-common` 0.1.0, approval pending.
- **Schemas and validation:**
  - Schemas: the PageSpec schema (Draft-07, generated from the contracts) and the section-contract schema.
  - Examples: the reference example (real copy) and the generated example (fictional).
  - Validators: `semantic_validate.py` and `adversarial_test.py`, covering 83 mutations including 9 wrapper-gate cases, plus 4 controls.
- **Verification and evidence:**
  - Checks: `verify_all.py`, `wrapper_gate.py`, `prove_drift.py` and `policy_hash.py`.
  - Builder: `build_repo.py`.
  - Measured heights at 1440x900, 768x1024 and 390x844.
  - Computed-style histogram.
  - Two live-vs-clone parity runs, saved as text-free JSON.

### Recorded, pending human approval

- `hero.statement`: 6300 px is above the 3000 px HERO cap. It is whitelisted with an agent attestation, not a human sign-off.
- `story.vr`: parity is below 0.80 in both runs (0.6898 and 0.7074), caused by the WebGL thumbnail sphere arrangement. The exception's `approvedBy` is null.

### Deviations from the groundwork

- `ia.json`'s single `chrome.footer` is split into `conversion.closing-cta` and `chrome.footer` for R6 category honesty. `ia.json` itself is unchanged, because it is outside this task's write scope.
- `ia.json` meta says "bottom-half sections still in build". In fact all of them are present and measured.
