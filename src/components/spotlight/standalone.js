// Standalone (non-Timeline) variants of the shared text helpers (reference/nuxt/B6fTRVdz.js):
// each helper call becomes a plain gsap.fromTo with its own ScrollTrigger. The helper `m(r)` defaults
// are applied: start "0% 90%", end "0% 30%", scrub true. Default ease = GSAP power1.out.
import { gsap } from '../tagline/sectionMotion'

export const st = (vars) => ({ start: '0% 90%', end: '0% 30%', scrub: true, ...vars })

// adapter with the same `add(targets, from, to, opts)` signature the sectionMotion helpers call
export const standalone = {
  add(targets, from, to, opts) {
    const { scrollTrigger, ...rest } = opts
    gsap.fromTo(targets, from, { ...to, ...rest, ...(scrollTrigger ? { scrollTrigger: { ...scrollTrigger } } : null) })
    return standalone
  },
}

// stagger defaults per helper (standalone branch of the original)
export const S_WORDS = 0.07
export const S_LINES = 0.07
export const S_FADE = 0.1
