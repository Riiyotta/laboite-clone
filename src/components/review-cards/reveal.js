// Standalone (non-Timeline) scroll helpers from reference/nuxt/B6fTRVdz.js, used by ReviewCards / FAQ / Footer.
// Every scrubbed helper goes through `withDefaults` (original `m()`): start ??= "0% 90%", end ??= "0% 30%", scrub = true.
// Call them inside useMotion (gsap.context) so they are reverted on unmount / re-split on resize.
import { gsap, SplitText } from '../tagline/sectionMotion'

const withDefaults = (st) => ({ start: '0% 90%', end: '0% 30%', ...st, scrub: true })

// original `y()`: SplitText wrappers get `superPreAccents @step[.1em]`
function preAccents(els) {
  for (const e of els) e.parentElement?.classList.add('superPreAccents')
}

// WORDS_REVEAL (export `d`, fn A): words {y:130%, scale:1.05} → {0%, 1} and `.line>.word` color #6630ff → computed color
export function wordsReveal(el, st) {
  if (!el) return
  const color = getComputedStyle(el).color
  const split = SplitText.create(el, { type: 'lines,words', mask: 'lines', linesClass: 'line', wordsClass: 'word' })
  preAccents(split.lines)
  gsap.fromTo(split.words, { y: '130%', scale: 1.05 }, { y: '0%', scale: 1, stagger: 0.07, scrollTrigger: withDefaults(st) })
  gsap.fromTo(el.querySelectorAll('.line>.word'), { color: '#6630ff' }, { color, stagger: 0.07, scrollTrigger: withDefaults(st) })
}

// FADE (export `s`, fn S)
export function fadeIn(targets, st) {
  if (!targets) return
  gsap.fromTo(targets, { autoAlpha: 0 }, { autoAlpha: 1, stagger: 0.1, scrollTrigger: withDefaults(st) })
}

// BLUR (export `a`, fn w) "in"
export function blurIn(el, st) {
  if (!el) return
  gsap.fromTo(el, { filter: 'blur(100px)' }, { filter: 'blur(0px)', scrollTrigger: withDefaults(st) })
}

// CARDS_POP (export `o`, fn M): time-based, play on enter / reverse on leave-back
export function cardsPop(targets, st) {
  if (!targets || !targets.length) return
  gsap.fromTo(targets, { y: '25%', scale: 0.95 }, {
    y: '0%', scale: 1, stagger: 0.1, duration: 0.7,
    scrollTrigger: { ...st, toggleActions: 'play none none reverse' },
  })
}
