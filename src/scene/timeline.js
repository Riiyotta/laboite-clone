// Scroll "Section Timeline" for the WebGL scene (spec §0.4), re-implemented on top of ScrollTrigger so it can be
// recomputed on every refresh (sections may still be zero-height stubs when the scene boots).
//
//   const sec = new SceneSection({ name, selector, overflowStart: () => lvh, overflowEnd: () => lvh })
//   sec.track({ start, end, overflowStart, overflowEnd }, (p, immediate) => …, { onEnter, onLeave, onEnterBack, onLeaveBack })
//     callbacks receive (immediate, syncing): immediate = the track was jumped over in one update, syncing = replayed by sync()
//   sec.tween({ start, end, … , ease }, (v) => …)     // stateless scrubbed tween: v = ease(local progress)
//
// Track semantics follow reference/nuxt/B6fTRVdz.js: on each progress change, tracks containing the new progress get
// eUpdate(p); tracks crossed entirely get eUpdate(1) (forward, by ascending end) / eUpdate(0) (backward, by descending
// start), flagged `immediate` when they were never active (→ X3D snaps instead of smoothing).
import { gsap, ScrollTrigger } from '../lib/motion'

const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v)
const noop = () => {}

export class SceneSection {
  constructor({ name, selector, trigger = null, overflowStart = null, overflowEnd = null, order = 0 }) {
    this.name = name
    this.selector = selector
    this.fixedTrigger = trigger
    this.getOS = overflowStart
    this.getOE = overflowEnd
    this.order = order
    this.tracks = []
    this.tweens = []
    this.el = null
    this.st = null
    this.startPx = 0
    this.T = 0
    this.s = this.c = 0
    this.o = 1
    this.progress = 0
    this.synced = false
    this.active = new Set()
    this.enabled = false
    this.syncing = false
  }

  // ---- mapping (§0.4) ----
  map({ start = 0, end = 1, overflowStart = 0, overflowEnd = 0 } = {}) {
    const tStart = this.o * clamp(start) + this.s * (1 - clamp(overflowStart))
    const tEnd = this.s + this.o * clamp(end) + this.c * clamp(overflowEnd)
    return [tStart, tEnd]
  }
  B({ overflowStart = 0, overflowEnd = 0 } = {}) { return 1 - this.s * (1 - overflowStart) - this.c * (1 - overflowEnd) }
  scrollAt(t) { return this.startPx + this.T * t }
  // scroll position of a timeline item (useful for other agents / debugging)
  range(item) { const [a, b] = this.map(item); return [this.scrollAt(a), this.scrollAt(b)] }
  // original Timeline.getTop(e): scroll position of pinned-range progress e (no overflow)
  getTop(e) { return this.startPx + this.T * (this.s + this.o * e) }

  track(item, update = noop, cbs = {}) {
    this.tracks.push({ item, update, onEnter: cbs.onEnter || noop, onLeave: cbs.onLeave || noop, onEnterBack: cbs.onEnterBack || noop, onLeaveBack: cbs.onLeaveBack || noop, a: 0, b: 1, p: -1 })
    this.remap()
    return this
  }
  tween(item, apply) {
    const ease = typeof item.ease === 'function' ? item.ease : gsap.parseEase(item.ease || 'power1.out')
    this.tweens.push({ item, apply, ease, a: 0, b: 1, last: NaN })
    this.remap()
    return this
  }
  // convenience: numeric fromTo on a plain object/uniform
  fromTo(target, key, from, to, item) {
    return this.tween(item, (v) => { target[key] = from + (to - from) * v })
  }

  remap() {
    for (const tr of this.tracks) [tr.a, tr.b] = this.map(tr.item)
    for (const tw of this.tweens) [tw.a, tw.b] = this.map(tw.item)
  }

  // ---- layout ----
  bind() {
    const el = this.fixedTrigger || (this.selector ? document.querySelector(this.selector) : null)
    if (el !== this.el) {
      this.st?.kill()
      this.st = null
      this.el = el
      if (el) {
        this.st = ScrollTrigger.create({
          trigger: el,
          start: () => (this.os() ? `0%-=${this.os()} 0` : '0% 0'),
          end: () => (this.oe() ? `100%+=${this.oe()} ${innerHeight}` : `100% ${innerHeight}`),
        })
        this.st.refresh()
      }
    }
  }
  os() { return this.getOS ? Math.max(this.getOS(), 0) : 0 }
  oe() { return this.getOE ? Math.max(this.getOE(), 0) : 0 }
  measure() {
    this.bind()
    if (!this.el || !this.st) { this.enabled = false; return }
    const start = this.st.start, end = this.st.end
    const total = end - start
    this.enabled = this.el.offsetHeight > 0 && total > 0
    this.startPx = start
    this.T = Math.max(total, 0)
    if (total > 0) {
      const os = this.os(), oe = this.oe()
      const r = Math.min(total / Math.max(os + oe, 1), 1)
      this.o = Math.max(total - os - oe, 0) / total
      this.s = (os / total) * r
      this.c = (oe / total) * r
    } else { this.o = 1; this.s = this.c = 0 }
    this.remap()
  }
  progressAt(scrollY) {
    if (!this.enabled) return 0
    return clamp((scrollY - this.startPx) / this.T)
  }

  // ---- runtime ----
  // called after every (re)measure — like Timeline.sync(): if the section has started, replay 0 → p
  sync(scrollY) {
    if (!this.enabled) return
    const p = this.progressAt(scrollY)
    this.renderTweens(p, true)
    this.synced = true
    this.syncing = true
    if (this.startPx <= scrollY) this.process(0, p)
    this.syncing = false
    this.progress = p
  }
  update(scrollY) {
    if (!this.enabled) return
    const p = this.progressAt(scrollY)
    if (p === this.progress) return
    this.renderTweens(p)
    this.process(this.progress, p)
    this.progress = p
  }
  renderTweens(p, force = false) {
    for (const tw of this.tweens) {
      const d = tw.b - tw.a
      const lp = d > 0 ? clamp((p - tw.a) / d) : p >= tw.b ? 1 : 0
      if (!force && lp === tw.last) continue
      tw.last = lp
      tw.apply(tw.ease(lp), lp)
    }
  }
  process(prev, cur) {
    const fwd = cur > prev
    const lo = Math.min(prev, cur), hi = Math.max(prev, cur)
    const mid = cur > 0 && cur < 1
    const nextActive = new Set()
    const passed = []
    for (const tr of this.tracks) {
      if (tr.b < lo || tr.a > hi) continue
      if (tr.a > cur || tr.b < cur) { passed.push(tr); continue }
      const was = this.active.delete(tr)
      if (!was) {
        if (!mid) { passed.push(tr); continue }
        fwd ? tr.onEnter(false, this.syncing) : tr.onEnterBack(false, this.syncing)
      }
      if (mid) nextActive.add(tr)
      const d = tr.b - tr.a
      tr.p = clamp(d ? (cur - tr.a) / d : 0)
      tr.update(tr.p, false)
    }
    if (passed.length) {
      if (fwd) {
        passed.sort((x, y) => x.b - y.b)
        for (const tr of passed) {
          const imm = !this.active.delete(tr)
          if (imm) tr.onEnter(true, this.syncing)
          tr.p = 1; tr.update(1, imm); tr.onLeave(imm, this.syncing)
        }
      } else {
        passed.sort((x, y) => y.a - x.a)
        for (const tr of passed) {
          const imm = !this.active.delete(tr)
          if (imm) tr.onEnterBack(true, this.syncing)
          tr.p = 0; tr.update(0, imm); tr.onLeaveBack(imm, this.syncing)
        }
      }
    }
    for (const tr of this.active) {
      const t = fwd ? 1 : 0
      if (tr.p !== t) { tr.p = t; tr.update(t, false) }
      fwd ? tr.onLeave(false, this.syncing) : tr.onLeaveBack(false, this.syncing)
    }
    this.active = nextActive
  }
  kill() { this.st?.kill(); this.st = null; this.el = null }
}
