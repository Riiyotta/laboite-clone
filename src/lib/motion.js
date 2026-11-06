// Shared motion primitives — mirrors CLONE_SPEC_A.md §0.4 exactly.
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { CustomEase } from 'gsap/CustomEase'
import { SplitText } from 'gsap/SplitText'
import Lenis from 'lenis'

gsap.registerPlugin(ScrollTrigger, CustomEase, SplitText)
gsap.ticker.lagSmoothing(0)
ScrollTrigger.config({ autoRefreshEvents: '' })

CustomEase.create('custom::out', 'M0,0 C.084,.61 .088,.874 .184,.944 .283,1.016 .374,1 1,1')
CustomEase.create('custom::out::back', 'M0,0 C.08,.7 .1,1.05 .2,1.12 .35,1.08 .5,1 1,1')
CustomEase.create('home::custom::out', 'M0,0 C0,1 0,0.903 1,1')

export { gsap, ScrollTrigger, CustomEase, SplitText }

// ---- Format detection (spec §0.1) ----
export const isMobile = () =>
  window.matchMedia('(max-width: 767.9px), (max-height: 434.9px)').matches
export const isWhole = () => !isMobile()
export const lvh = () => window.innerHeight

// ---- Lenis driven from the GSAP ticker ----
let lenis = null
export function initLenis() {
  if (lenis) return lenis
  lenis = new Lenis({ autoRaf: false })
  lenis.on('scroll', ScrollTrigger.update)
  gsap.ticker.add((t) => lenis.raf(t * 1000))
  window.lenis = lenis
  return lenis
}
export const getLenis = () => lenis

// ---- Section Timeline (spec §0.4) ----
// Usage:
//   const st = sectionTimeline(el, { overflowStart: lvh(), overflowEnd: lvh() })
//   st.add(target, fromVars, toVars, { start, end, overflowStart, overflowEnd, itemDuration, stagger })
//   st.track({ start, end, ... }, (p) => {...})   // progress 0..1 callback
export function sectionTimeline(trigger, { overflowStart = 0, overflowEnd = 0 } = {}) {
  const H = lvh()
  const tl = gsap.timeline({
    defaults: { ease: 'power1.out' },
    scrollTrigger: {
      trigger,
      scrub: true,
      start: overflowStart ? `0%-=${overflowStart} 0` : '0% 0',
      end: overflowEnd ? `100%+=${overflowEnd} ${H}` : `100% ${H}`,
      invalidateOnRefresh: true,
    },
  })
  // force total duration 1
  tl.set({}, {}, 1)
  const T = Math.max(1, overflowStart + trigger.offsetHeight + overflowEnd - H)
  const s = overflowStart / T
  const c = overflowEnd / T
  const o = 1 - s - c
  const map = ({ start = 0, end = 1, overflowStart: os = 0, overflowEnd: oe = 0 } = {}) => {
    const tStart = o * start + s * (1 - os)
    const tEnd = s + o * end + c * oe
    const B = 1 - s * (1 - os) - c * (1 - oe)
    return { tStart, tEnd, B }
  }
  const api = {
    tl, s, c, o, T, map,
    add(targets, fromVars, toVars, item = {}) {
      const { tStart, tEnd, B } = map(item)
      const list = gsap.utils.toArray(targets)
      const n = list.length
      let dur = tEnd - tStart
      let stagger = 0
      if (n > 1 && item.itemDuration != null) {
        dur = B * item.itemDuration
        stagger = (tEnd - tStart - dur) / (n - 1)
      } else if (n > 1 && item.stagger != null) {
        stagger = B * item.stagger
        dur = tEnd - tStart - stagger * (n - 1)
      }
      tl.fromTo(list.length ? list : targets, fromVars, { ...toVars, duration: dur, stagger, immediateRender: true }, tStart)
      return api
    },
    track(item, cb) {
      const { tStart, tEnd } = map(item)
      const proxy = { p: 0 }
      tl.fromTo(proxy, { p: 0 }, { p: 1, ease: 'none', duration: tEnd - tStart, onUpdate: () => cb(proxy.p) }, tStart)
      return api
    },
  }
  return api
}

// ---- Text helpers (spec §0.4) ----
export function splitLines(el, mask = false) {
  return new SplitText(el, { type: 'lines', linesClass: 'line superPreAccents', mask: mask ? 'lines' : undefined })
}
export const linesSlideVars = (axis = 'y') => {
  const key = axis.replace('-', '')
  const v = axis === '-x' ? -20 : 20
  return [{ [key]: v, autoAlpha: 0 }, { [key]: 0, autoAlpha: 1 }]
}
export const fadeVars = (dir = 'in') => (dir === 'in' ? [{ autoAlpha: 0 }, { autoAlpha: 1 }] : [{ autoAlpha: 1 }, { autoAlpha: 0 }])
export const parallaxVars = (n) => [{ y: n }, { y: -n }]

export function charsIn(trigger, els) {
  const splits = gsap.utils.toArray(els).map((e) => new SplitText(e, { type: 'chars', charsClass: 'char', mask: 'chars' }))
  const chars = splits.flatMap((s) => s.chars)
  return gsap.fromTo(chars, { x: '100%', opacity: 0 }, {
    x: '0%', opacity: 1, stagger: 0.05, duration: 1.7, ease: 'custom::out',
    scrollTrigger: { trigger, start: '0% 100%', scrub: false, toggleActions: 'play none none reverse' },
  })
}

export function wordsRise(el) {
  const color = getComputedStyle(el).color
  const split = new SplitText(el, { type: 'lines,words', linesClass: 'line', wordsClass: 'word', mask: 'lines' })
  return { split, from: { y: '130%', scale: 1.05, color: '#6630FF' }, to: { y: '0%', scale: 1, color }, targets: split.words }
}

export function maskReveal(el, size = 200, at = 90) {
  gsap.set(el, {
    maskImage: `linear-gradient(0deg, transparent calc(50% - ${size / 2}px), red calc(50% + ${size / 2}px))`,
    maskSize: `100% calc(200% + ${size}px)`, maskRepeat: 'no-repeat', maskPosition: '0% 100%',
    webkitMaskImage: `linear-gradient(0deg, transparent calc(50% - ${size / 2}px), red calc(50% + ${size / 2}px))`,
    webkitMaskSize: `100% calc(200% + ${size}px)`, webkitMaskRepeat: 'no-repeat',
  })
  return gsap.fromTo(el, { maskPosition: '0% 100%', webkitMaskPosition: '0% 100%' }, {
    maskPosition: '0% 0%', webkitMaskPosition: '0% 0%', ease: 'none',
    scrollTrigger: { trigger: el, start: `0% ${at}%`, end: `100%+=${size} ${at}%`, scrub: true },
  })
}

// ---- Button hover (spec §1.2) ----
export function bindButtonHover(btn) {
  const enter = () => {
    btn.classList.add('@hovered')
    gsap.fromTo(btn, { '--button-hover-y': '0%' }, { '--button-hover-y': '50%', duration: 2.5, ease: 'custom::out', overwrite: true })
  }
  const leave = () => {
    btn.classList.remove('@hovered')
    gsap.to(btn, { '--button-hover-y': '100%', duration: 0.4, overwrite: true, onComplete: () => gsap.set(btn, { '--button-hover-y': '0%' }) })
  }
  btn.addEventListener('mouseenter', enter)
  btn.addEventListener('mouseleave', leave)
  return () => { btn.removeEventListener('mouseenter', enter); btn.removeEventListener('mouseleave', leave) }
}
