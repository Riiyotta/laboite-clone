// Local motion helpers shared by Tagline / Works / Method / Skills.
// These re-implement the original Nuxt helpers (reference/nuxt/B6fTRVdz.js) where src/lib/motion.js
// deviates from them:
//  - sectionTimeline: positions are recomputed on every ScrollTrigger refresh (original #J/#X), so
//    layout/font/lvh changes after creation don't leave stale tween positions; T comes from the
//    trigger's real start/end, and s/c are scaled by r = min(T/(ovS+ovE), 1) like the original.
//  - linesSlide: `superPreAccents` goes on the split element (parent of the lines), not on each line.
//  - wordsRise: color tween targets only `.line>.word` (words inside <strong> keep their own color).
//  - charsIn: splits "words,chars" (mask chars), tags char masks with the @noFix pre-accents variant,
//    and accepts non-text targets (the marquee icon svg).
import { useEffect, useLayoutEffect, useState } from 'react'
import { gsap, ScrollTrigger, SplitText, lvh } from '../../lib/motion'

const MOBILE_MQ = '(max-width: 767.9px), (max-height: 434.9px)'

export function useWhole() {
  const [whole, setWhole] = useState(() => !window.matchMedia(MOBILE_MQ).matches)
  useEffect(() => {
    const m = window.matchMedia(MOBILE_MQ)
    const f = () => setWhole(!m.matches)
    m.addEventListener('change', f)
    return () => m.removeEventListener('change', f)
  }, [])
  return whole
}

let refreshTimer = 0
export function requestRefresh() {
  clearTimeout(refreshTimer)
  refreshTimer = setTimeout(() => ScrollTrigger.refresh(), 60)
}

// Runs `build(ctx)` inside a gsap.context once fonts are ready (line splits depend on metrics);
// rebuilds on width change (re-split), reverts everything on unmount / when disabled.
export function useMotion(build, enabled = true) {
  useLayoutEffect(() => {
    if (!enabled) return
    let ctx = null
    let dead = false
    let w = window.innerWidth
    let timer = 0
    const run = () => {
      ctx = gsap.context(() => {})
      ctx.add(() => build(ctx))
      requestRefresh()
    }
    document.fonts.ready.then(() => { if (!dead) run() })
    const onResize = () => {
      clearTimeout(timer)
      timer = setTimeout(() => {
        if (dead || window.innerWidth === w) return
        w = window.innerWidth
        ctx?.revert()
        run()
      }, 150)
    }
    window.addEventListener('resize', onResize)
    return () => {
      dead = true
      clearTimeout(timer)
      window.removeEventListener('resize', onResize)
      ctx?.revert()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled])
}

const toList = (t) => {
  if (!t) return []
  if (t instanceof NodeList || Array.isArray(t)) return [...t].filter(Boolean)
  return [t]
}

// Section Timeline (spec §0.4, original class `f` in B6fTRVdz.js).
export function sectionTimeline(trigger, { overflowStart = 0, overflowEnd = 0 } = {}, ctx) {
  const fS = typeof overflowStart === 'function' ? overflowStart : () => overflowStart
  const fE = typeof overflowEnd === 'function' ? overflowEnd : () => overflowEnd
  const items = []
  let s = 0
  let c = 0
  let o = 1
  const make = (fn) => (ctx ? ctx.add(fn) : fn())

  const place = (item) => {
    const tS = o * item.start + s * (1 - item.overflowStart)
    const tE = s + o * item.end + c * item.overflowEnd
    const t = Math.max(tE - tS, 0)
    const n = item.targets.length
    const B = 1 - s * (1 - item.overflowStart) - c * (1 - item.overflowEnd)
    let stagger
    if (n > 1) {
      if (item.itemDuration) stagger = Math.max(t - B * item.itemDuration, 0) / (n - 1)
      else if (item.stagger) stagger = B * item.stagger
    }
    const duration = stagger ? Math.max(t - stagger * (n - 1), 0) : t
    if (item.tween) {
      tl.remove(item.tween)
      if (item.tween.vars.duration === duration && item.tween.vars.stagger === stagger) item.tween.invalidate()
      else { item.tween.kill(); item.tween = null }
    }
    if (!item.tween) {
      make(() => { item.tween = gsap.fromTo(item.targets, item.from, { ...item.to, duration, stagger }) })
    }
    tl.add(item.tween, tS)
  }

  const layout = (self) => {
    const T = self.end - self.start
    if (T) {
      const e = Math.max(fS(), 0)
      const n = Math.max(fE(), 0)
      const r = Math.min(T / Math.max(e + n, 1), 1)
      o = Math.max(T - e - n, 0) / T
      s = (e / T) * r
      c = (n / T) * r
    } else { s = c = o = 0 }
    for (const it of items) place(it)
    const p = T ? gsap.utils.clamp(0, 1, (self.scroll() - self.start) / T) : 0
    tl.progress(0, true).progress(p)
  }

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger,
      scrub: true,
      start: () => { const v = fS(); return v ? `0%-=${v} 0` : '0% 0' },
      end: () => { const v = fE(); return v ? `100%+=${v} ${lvh()}` : `100% ${lvh()}` },
      onRefresh: (self) => layout(self),
    },
  })
  tl.to({}, { duration: 1 }, 0)

  const api = {
    tl,
    // add(targets, fromVars, toVars(+ease…), {start,end,overflowStart,overflowEnd,itemDuration,stagger})
    add(targets, from, to, { start = 0, end = 1, overflowStart: os = 0, overflowEnd: oe = 0, itemDuration, stagger } = {}) {
      const list = toList(targets)
      if (!list.length) return api
      items.push({ targets: list, from, to, start, end, overflowStart: os, overflowEnd: oe, itemDuration, stagger, tween: null })
      return api
    },
    sync() { if (tl.scrollTrigger) layout(tl.scrollTrigger); return api },
  }
  return api
}

// ---- Original text helpers ----
function preAccents(els, noFix = false) {
  for (const e of els) e.parentElement?.classList.add('superPreAccents', ...(noFix ? ['noFix'] : []))
}

// linesSlide (I): lines {[axis]:±20, autoAlpha:0} → {0, 1}
export function linesSlide(tl, el, dir, axis, item) {
  if (!el) return
  const neg = axis.startsWith('-')
  const key = neg ? axis[1] : axis
  const off = neg ? -20 : 20
  const [a, b, c, d] = dir === 'in' ? [off, 0, 0, 1] : [0, off, 1, 0]
  const split = SplitText.create(el, { type: 'lines', linesClass: 'line' })
  preAccents(split.lines)
  const { ease, ...rest } = item
  tl.add(split.lines, { [key]: a, autoAlpha: c }, { [key]: b, autoAlpha: d, ...(ease ? { ease } : null) }, rest)
}

// fade (R)
export function fade(tl, targets, dir, item) {
  const [a, b] = dir === 'in' ? [0, 1] : [1, 0]
  const { ease, ...rest } = item
  tl.add(targets, { autoAlpha: a }, { autoAlpha: b, ...(ease ? { ease } : null) }, rest)
}

// parallax (z): y n → -n
export function parallax(tl, el, n, item) {
  tl.add(el, { y: n }, { y: -n }, item)
}

// wordsRise (De)
export function wordsRise(tl, el, item) {
  if (!el) return
  const color = getComputedStyle(el).color
  const split = SplitText.create(el, { type: 'lines,words', mask: 'lines', linesClass: 'line', wordsClass: 'word' })
  preAccents(split.lines)
  tl.add(split.words, { y: '130%', scale: 1.05 }, { y: '0%', scale: 1 }, item)
  tl.add(el.querySelectorAll('.line>.word'), { color: '#6630FF' }, { color }, item)
}

// charsIn (L)
export function charsIn(trigger, els) {
  const targets = []
  for (const e of els) {
    if (!e) continue
    if (e.textContent) {
      const sp = SplitText.create(e, { type: 'words,chars', mask: 'chars', wordsClass: 'word', charsClass: 'char' })
      targets.push(...sp.chars)
      preAccents(sp.chars, true)
    } else targets.push(e)
  }
  if (!targets.length) return null
  return gsap.fromTo(targets, { x: '100%', opacity: 0 }, {
    x: '0%', opacity: 1, stagger: 0.05, duration: 1.7, ease: 'custom::out',
    scrollTrigger: { trigger, start: '0% 100%', scrub: false, toggleActions: 'play none none reverse' },
  })
}

// maskReveal (F) — same as original T(): `mask` shorthand then maskPosition tween.
export function maskReveal(el, size = 200, at = 90) {
  if (!el) return null
  const h = size / 2
  gsap.set(el, { mask: `linear-gradient(0deg, transparent calc(50% - ${h}px), red calc(50% + ${h}px)) 0% 0% / 100% calc(200% + ${size}px) no-repeat` })
  return gsap.fromTo(el, { maskPosition: '0% 100%' }, {
    maskPosition: '0% 0%', ease: 'none',
    scrollTrigger: { trigger: el, start: `0% ${at}%`, end: `100%+=${size} ${at}%`, scrub: true },
  })
}

export { gsap, ScrollTrigger, SplitText, lvh }
