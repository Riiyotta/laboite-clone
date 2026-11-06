// Bottom-half scene phases after the VR sticker (spec B §0.2, §5, §8.4):
//   · layers 9 (DRK) / 10 (LGH) — scrubbed by the label-cards sticker (DqzInzYb.js At(): Ve.tweens_add on
//     `.home__labelCards`, "0% 100%" → "0% 0%" and "100% 100%" → "100% 0%", ease none)
//   · final layer (PRM) — footer, "0% 100%" → "0% 0%", default ease power1.out, uCurveAmountFinal −.05 → 0
//   · footer glass-triangle conveyor (BJwg4-9U.js Footer: TRIANGLES plugin + timeline H + BASIC tick)
// The DOM sections are owned by other components and may be stubs / re-rendered: every range is re-resolved
// from its selector on each ScrollTrigger refresh.
import * as THREE from 'three'
import { gsap, ScrollTrigger, lvh } from '../lib/motion'
import { lerp } from './x3d'
import { createTriangleMeshes, TRIANGLE_SIZE } from './triangles'

// BGRTs5Rh.js export `t` — footer triangle ring (positions / rotations)
export const FOOTER_TRIANGLES = [
  { position: [30, 0, 0], rotation: [-1.571, 1.571, 0] }, { position: [28.532, 0, 9.271], rotation: [-1.571, 1.885, 0] },
  { position: [24.271, 0, 17.634], rotation: [-1.571, 2.199, 0] }, { position: [17.634, 0, 24.271], rotation: [-1.571, 2.513, 0] },
  { position: [9.271, 0, 28.532], rotation: [-1.571, 2.827, 0] }, { position: [0, 0, 30], rotation: [-1.571, 3.142, 0] },
  { position: [-9.271, 0, 28.532], rotation: [-1.571, 3.456, 0] }, { position: [-17.634, 0, 24.271], rotation: [-1.571, 3.77, 0] },
  { position: [-24.271, 0, 17.634], rotation: [-1.571, 4.084, 0] }, { position: [-28.532, 0, 9.271], rotation: [-1.571, 4.398, 0] },
  { position: [-30, 0, 0], rotation: [-1.571, 4.712, 0] }, { position: [-28.532, 0, -9.271], rotation: [-1.571, 5.027, 0] },
  { position: [-24.271, 0, -17.634], rotation: [-1.571, 5.341, 0] }, { position: [-17.634, 0, -24.271], rotation: [-1.571, 5.655, 0] },
  { position: [-9.271, 0, -28.532], rotation: [-1.571, 5.969, 0] }, { position: [0, 0, -30], rotation: [-1.571, 6.283, 0] },
  { position: [9.271, 0, -28.532], rotation: [-1.571, 6.597, 0] }, { position: [17.634, 0, -24.271], rotation: [-1.571, 6.912, 0] },
  { position: [24.271, 0, -17.634], rotation: [-1.571, 7.226, 0] }, { position: [28.532, 0, -9.271], rotation: [-1.571, 7.54, 0] },
]

const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v)

// Scrubbed range on a DOM element: start/end = f(top, bottom, lvh) in document px (ScrollTrigger "A% B%" notation).
class DomRange {
  constructor(selector, start, end, apply, ease = (t) => t) {
    Object.assign(this, { selector, startFn: start, endFn: end, apply, ease })
    this.a = this.b = 0
    this.ok = false
    this.last = NaN
  }
  measure() {
    const el = document.querySelector(this.selector)
    this.ok = !!el && el.offsetHeight > 0
    if (!this.ok) return
    const r = el.getBoundingClientRect()
    const top = r.top + window.scrollY
    const vh = lvh()
    this.a = this.startFn(top, top + r.height, vh)
    this.b = this.endFn(top, top + r.height, vh)
    this.last = NaN
  }
  update(y, force = false) {
    if (!this.ok) return
    const d = this.b - this.a
    const p = d > 0 ? clamp01((y - this.a) / d) : y >= this.b ? 1 : 0
    if (!force && p === this.last) return
    this.last = p
    this.apply(this.ease(p), p)
  }
}

export function setupBottom(ctx) {
  const { sections, bg, addX3D, addTicker, scene } = ctx
  const L9 = bg.layers[8], L10 = bg.layers[9], F = bg.final
  const LABEL = '[data-section="label-cards"]'
  const FOOTER = '[data-section="footer"]'
  const power1Out = gsap.parseEase('power1.out')

  const ranges = [
    new DomRange(LABEL, (t, b, vh) => t - vh, (t) => t, (v) => { L9.uTransition.value = v; L9.uCurveAmount.value = 0.3 - 0.3 * v }),
    new DomRange(LABEL, (t, b, vh) => b - vh, (t, b) => b, (v) => { L10.uTransition.value = v; L10.uCurveAmount.value = 0.3 - 0.3 * v }),
    new DomRange(FOOTER, (t, b, vh) => t - vh, (t) => t, (v) => { F.uTransition.value = v; F.uCurveAmount.value = -0.05 + 0.05 * v }, power1Out),
  ]
  F.uCurveAmount.value = -0.05

  // ---------------- footer triangles ----------------
  const R = FOOTER_TRIANGLES.length
  const root = new THREE.Group()
  const X = addX3D(root, { name: 'TRIANGLES_3D' })
  root.visible = false
  X.setPosition(TRIANGLE_SIZE / 2, -100, -47)
  X.setRotation(Math.PI, 0.5, 0.3)
  const Z = [TRIANGLE_SIZE / 2, -100, -47]
  const { meshes, material, geometry } = createTriangleMeshes(R)
  const z = meshes.map((m, t) => {
    m.renderOrder = 0
    m.name = `TRIANGLE_3D[${t}]`
    root.add(m)
    const x = addX3D(m)
    const { position: n, rotation: r } = FOOTER_TRIANGLES[t]
    x.setPosition(n[0] + 5, n[1], n[2])
    x.setRotation(...r)
    return x
  })
  scene.add(root)

  let K = 0, q = 1, J = 0, Yi = 0, on = false
  const Ve = () => {
    material.opacity = K
    let n = FOOTER_TRIANGLES[Yi ? Yi - 1 : R - 1].position
    for (let t = 0; t < R; t++) {
      const i = FOOTER_TRIANGLES[(t + Yi) % R].position
      const a = FOOTER_TRIANGLES[t].rotation
      z[t].addPosition(lerp(n[0], i[0], J) * q, lerp(n[1], i[1], J), lerp(n[2], i[2], J) * q, J)
      z[t].addRotation(a[0] * q, a[1] * q, a[2] * q, 0.5)
      n = i
    }
  }
  const Q = (v) => { on = v; root.visible = v }

  const FOOT = sections.add({ name: 'FOOTER', selector: FOOTER, overflowStart: lvh })
  FOOT.track({ end: 1, overflowStart: 1 }, (t, imm) => {
    const i = 1 - (1 - t) ** 2
    K = t ** 2
    q = 1 + (1 - i) * 2
    X.addPosition(Z[0], lerp(Z[1], 3, i), Z[2], i, imm)
  }, { onEnter: () => Q(true), onLeaveBack: () => Q(false) })

  let whole = true
  const removeTick = addTicker((dt) => {
    if (!whole) return
    const y = window.scrollY
    for (const r of ranges) r.update(y)
    if (on) {
      J = Math.min(J + dt * 0.3, 1)
      Ve()
      if (J === 1) { J = 0; Yi = (Yi + 1) % R }
    }
  })
  const measure = () => {
    if (!whole) return
    const y = window.scrollY
    for (const r of ranges) { r.measure(); r.update(y, true) }
  }
  ScrollTrigger.addEventListener('refresh', measure)
  measure()

  return {
    ranges, measure,
    footer: { x3d: X, root, children: z, material, section: FOOT },
    setWhole(w) {
      whole = w
      if (!w) {
        Q(false)
        for (const L of [L9, L10]) { L.uTransition.value = 0; L.uCurveAmount.value = 0.3 }
        F.uTransition.value = 0; F.uCurveAmount.value = -0.05
      } else measure()
    },
    dispose() {
      removeTick()
      ScrollTrigger.removeEventListener('refresh', measure)
      scene.remove(root); geometry.dispose(); material.dispose()
    },
  }
}
