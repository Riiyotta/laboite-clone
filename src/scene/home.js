// Home-page scene phases (spec §3.3, §3.5, §3.6, §4.2, §5.2, §7.2) — mirrors the HOME page setup in
// reference/nuxt/DqzInzYb.js (functions At/jt/Mt/Nt/Ot/qt/zt/$).
import * as THREE from 'three'
import { gsap, CustomEase, lvh } from '../lib/motion'
import { lerp } from './x3d'
import { TITLE, maskStep, maskStep2 } from './title'
import { TRIANGLE_SIZE, TRIANGLE_DEPTH } from './triangles'

const TAU = Math.PI * 2
const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v)
const nearest = (v, a, b) => (Math.abs(v - a) < Math.abs(v - b) ? a : b)
const STEP = 0.08
const FRAG = 0.92 / 3

// lerp helper for keyframe pairs
const L3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)]

export function setupHome(ctx) {
  const { sections, camera, tri, titleA, titleB, bg, data } = ctx
  const H = data.DATA_CAMERA_3D, U = data.DATA_TRIANGLES_3D, W = data.DATA_TRIANGLES_3D_CHILDREN
  const { group: q, children: z, material } = tri
  const lvhPx = () => lvh()

  // ---- $(k[, fade]) : children p(k-1)→pk, r(k-1)→rk ----
  const $ = (k, fade = 1) => {
    const pa = `p${k - 1}`, pb = `p${k}`, ra = `r${k - 1}`, rb = `r${k}`
    const op = fade === 'in' ? (p) => { material.opacity = p } : fade === 'out' ? (p) => { material.opacity = 1 - p } : () => { if (material.opacity !== fade) material.opacity = fade }
    return (p, imm) => {
      op(p)
      for (let i = 0; i < z.length; i++) {
        const d = W[i]
        const P = L3(d[pa], d[pb], p), R = L3(d[ra], d[rb], p)
        z[i].addPosition(P[0], P[1], P[2], p, imm)
        z[i].addRotation(R[0], R[1], R[2], p, imm)
      }
    }
  }
  const camTrack = (a, b) => (p, imm) => { const P = L3(H[a], H[b], p); camera.addPosition(P[0], P[1], P[2], p, imm) }
  const groupPos = (a, b, ease = (t) => t) => (p, imm) => { const e = ease(p); const P = L3(U[a], U[b], e); q.addPosition(P[0], P[1], P[2], e, imm) }
  const groupRot = (a, b, ease = (t) => t) => (p, imm) => { const e = ease(p); const R = L3(U[a], U[b], e); q.addRotation(R[0], R[1], R[2], e, imm) }
  const layer = (sec, k, item) => {
    const Lk = bg.layers[k - 1]
    sec.tween({ ...item, ease: 'none' }, (v) => { Lk.uTransition.value = v; Lk.uCurveAmount.value = 0.3 - 0.3 * v })
  }

  // ---------------- background (At) ----------------
  bg.layers[0].uTransition.value = 1
  bg.layers[0].uCurveAmount.value = 0
  bg.layers[6].uCurveAmount.value = 0

  // ---------------- HEADER (hero) ----------------
  const HERO = sections.add({ name: 'HEADER', selector: '[data-section="hero"]', overflowEnd: lvhPx })
  layer(HERO, 2, { start: 0, end: 0.4 })
  // camera (jt)
  camera.setPosition(...H.p0)
  HERO.track({ start: 0, end: 0.4 }, camTrack('p0', 'p1'))
    .track({ start: 0.4, end: 0.6 }, camTrack('p1', 'p2'))
    .track({ start: 0.6, end: 0.9 }, camTrack('p2', 'p3'))
    .track({ start: 1, overflowEnd: 1 }, camTrack('p3', 'p4'))
  // triangles (Mt)
  q.setRotation(...U.r0)
  HERO.track({ start: 0, end: 0.6 }, $(1))
    .track({ start: 0.6, end: 0.9 }, $(2))
    .track({ start: 0.6, end: 0.9 }, groupRot('r0', 'r1', (t) => t ** 3))
  // titles (Nt)
  const setTitlesVisible = (v) => { titleA.x3d.root.visible = titleB.x3d.root.visible = v }
  HERO.track({ start: 0, end: 0.75 }, undefined, { onLeave: () => setTitlesVisible(false), onEnterBack: () => setTitlesVisible(true) })
  const LH = TITLE.LINE_HEIGHT, HT = TITLE.HEIGHT
  HERO.fromTo(titleA.masks[2], 'constant', maskStep(1), maskStep2(1), { start: 0.08, end: 0.16 })
    .fromTo(titleA.masks[1], 'constant', maskStep(0), maskStep2(0), { start: 0.1, end: 0.18 })
    .fromTo(titleA.masks[0], 'constant', maskStep(-1), maskStep2(-1), { start: 0.12, end: 0.2 })
    .fromTo(titleB.lines[0].position, 'z', -LH + HT, -LH, { start: 0.26, end: 0.33 })
    .fromTo(titleB.lines[1].position, 'z', HT, 0, { start: 0.28, end: 0.35 })
    .fromTo(titleB.lines[2].position, 'z', LH + HT, LH, { start: 0.3, end: 0.37 })
    .fromTo(titleB.masks[2], 'constant', maskStep(1), maskStep2(1), { start: 0.48, end: 0.55 })
    .fromTo(titleB.masks[1], 'constant', maskStep(0), maskStep2(0), { start: 0.5, end: 0.57 })
    .fromTo(titleB.masks[0], 'constant', maskStep(-1), maskStep2(-1), { start: 0.52, end: 0.59 })

  // ---------------- TAGLINE ----------------
  const TAG = sections.add({ name: 'TAGLINE', selector: '[data-section="tagline"]', overflowStart: lvhPx, overflowEnd: lvhPx })
  layer(TAG, 3, { end: 0.15, overflowStart: 0.7 })
  layer(TAG, 4, { start: 1, overflowEnd: 1 })
  TAG.track({ start: 0, overflowEnd: 0.7 }, camTrack('p4', 'p5'))
  TAG.track({ end: 0, overflowStart: 0.7 }, groupPos('p0', 'p1'))
    .track({ start: 0, overflowEnd: 0.7 }, (p, imm) => { groupPos('p1', 'p2')(p, imm); groupRot('r1', 'r2')(p, imm) })
    .track({ end: 0, overflowStart: 0.7 }, $(3))
    .track({ start: 0, end: 0.25 }, $(4))
    .track({ start: 0.25, end: 0.75 }, $(5))

  // ---------------- WORKS ----------------
  const WORKS = sections.add({ name: 'WORKS', selector: '[data-section="works"]', overflowStart: lvhPx, overflowEnd: lvhPx })
  WORKS.track({ start: 0.6, end: 0.9 }, camTrack('p5', 'p6'))
  const outCubic = (t) => 1 - (1 - t) ** 3
  WORKS.track({ end: 0.5, overflowStart: 1 }, (p, imm) => { groupPos('p2', 'p3', outCubic)(p, imm); groupRot('r2', 'r3', outCubic)(p, imm) })
    .track({ end: 0.5, overflowStart: 1 }, $(6, 'out'))

  // ---------------- SKILLS ----------------
  const SKILLS = sections.add({ name: 'SKILLS', selector: '[data-section="skills"]', overflowStart: lvhPx, overflowEnd: lvhPx })
  layer(SKILLS, 5, { end: 0.1, overflowStart: 0.7 })
  layer(SKILLS, 6, { start: 1, overflowEnd: 1 })
  SKILLS.track({ end: STEP, overflowStart: 0.5 }, camTrack('p6', 'p7'))
  SKILLS.track({ end: 0.2, overflowStart: 0.7 }, groupPos('p3', 'p4'))
    .track({ end: STEP, overflowStart: 0.5 }, groupRot('r3', 'r4'))
    .track({ end: STEP, overflowStart: 0.5 }, $(7, 'in'))
    .track({ start: 1, overflowEnd: 0.7 }, $(11), { onEnterBack: () => { q.root.visible = true }, onLeave: () => { q.root.visible = false } })
  for (let k = 0; k < 3; k++) {
    const s = FRAG * k + STEP
    SKILLS.track({ start: s, end: s + 0.07 }, $(8 + k))
  }

  // ---------------- frame layout (qt) — recomputed on resize ----------------
  function layoutFrame() {
    const g = 1.4
    const dist = Math.sqrt(H.p3[1] ** 2 + H.p3[2] ** 2)
    const h = Math.tan(THREE.MathUtils.degToRad(camera.root.fov / 2)) * (dist - TRIANGLE_DEPTH) * 2
    const w = h * camera.root.aspect
    const ax = Math.max(w / 2, TRIANGLE_SIZE * 2 + g * 3), ay = Math.max(h / 2, TRIANGLE_SIZE * 2 + g * 2)
    const S = [-1, 1, -1, -1, 1, -1, 1, 1]
    const C = [18, 11, 16, 10, 1, -1, 3, 20, 12, 13, 14, 9, 19, 8, 21, 2, 4, -1, 7, 17, 15, 5, 0, 6]
    for (let k = 0; k < 4; k++) {
      const sx = S[k * 2], sy = S[k * 2 + 1], r = k * 6
      const c0 = W[C[r]].p2, c1 = W[C[r + 1]].p2, c2 = W[C[r + 2]].p2, c3 = W[C[r + 3]].p2, c4 = W[C[r + 4]].p2
      const X = ax * sx, Y = ay * sy, x1 = X - TRIANGLE_SIZE * sx, y1 = Y - TRIANGLE_SIZE * sy
      c0[0] = X; c0[1] = Y
      c1[0] = x1 - g * sx; c1[1] = y1 - g * sy
      c2[0] = x1 - g * 2 * sx; c2[1] = Y
      c3[0] = X; c3[1] = y1 - g * 2 * sy
      if (k % 2) {
        const c5 = W[C[r + 5]].p2
        c4[0] = -0.7; c5[0] = 0.7; c4[1] = c5[1] = y1 - g * sy
      } else { c4[0] = X - g * sx; c4[1] = 0 }
    }
  }
  layoutFrame()

  // ---------------- idle bob (Ge2) ----------------
  const phases = z.map(() => Math.random() * TAU)
  let bobT = 0
  let bobOn = false
  const bob = (dt) => {
    if (!bobOn) return
    bobT += dt
    for (let i = 0; i < z.length; i++) z[i].addNoisyPosition(0, Math.sin(phases[i] + bobT) * 0.5, 0, 0)
  }

  // ---------------- load intro (Ot / zt) ----------------
  let introPrepared = null
  function prepareIntro() {
    // b = bounding size of child 0 with the group's world matrix still identity (as at the original call site)
    const m0 = z[0].root
    m0.updateMatrix()
    const box = new THREE.Box3().setFromBufferAttribute(m0.geometry.attributes.position).applyMatrix4(m0.matrix)
    const b = box.getSize(new THREE.Vector3())
    const n3 = 1.7, r2 = 1.2
    const cw = b.x + n3, ch = b.y + n3, px = cw + r2, py = ch + r2
    const x0 = (-px * 5 + r2) / 2, y0 = (-py * 3 + r2) / 2
    const maxD = Math.sqrt((x0 + px * 4) ** 2 + (y0 + py * 2) ** 2) || 1
    const P = [-1, -1, 3, 13, 12, 9, 21, 19, -1, -1, 10, 1, 11, 18, 14, 17, 4, 8, 2, 5, -1, -1, 20, 16, 6, 0, 15, 7, -1, -1]
    const out = []
    for (let t = 0; t < 15; t++) {
      const A = P[t * 2]
      if (A === -1) continue
      const B = P[t * 2 + 1]
      const dz = t & 1 ? -13 : 13
      const gx = x0 + (t % 5) * px, gy = y0 + py * ((t / 5) | 0)
      const dA = (Math.sqrt(gx ** 2 + gy ** 2) / maxD) * 0.07 + (((A * 17 + 7) % 97) / 97) * 0.055
      const bx = gx + cw, by = gy + ch
      const dB = (Math.sqrt(bx ** 2 + by ** 2) / maxD) * 0.07 + (((B * 17 + 16) % 97) / 97) * 0.055 + 0.007
      const a = z[A], bb = z[B]
      const TA = {
        x: a,
        p0: [gx - a.pX + (gx < 0 ? -6 : 6), gy - a.pY + (gy < 0 ? -2 : 2), -55 - a.pZ + dz],
        p1: [gx - a.pX, gy - a.pY, -55 - a.pZ],
        r0: [nearest(a.rX, 0, TAU) - a.rX, nearest(a.rY, 0, TAU) - a.rY, nearest(a.rZ, 0, TAU) - a.rZ],
        delay: dA, duration: 1 - dA,
      }
      const TB = {
        x: bb,
        p0: [bx - bb.pX + 0, by - bb.pY + (by < 0 ? -2 : 2), -55 - bb.pZ + dz],
        p1: [bx - bb.pX, by - bb.pY, -55 - bb.pZ],
        r0: [nearest(bb.rX, 0, TAU) - bb.rX, nearest(bb.rY, 0, TAU) - bb.rY, nearest(bb.rZ, Math.PI, Math.PI * 3) - bb.rZ],
        delay: dB, duration: 1 - dB,
      }
      for (const T of [TA, TB]) { T.x.set('shaken', 'position', ...T.p0); T.x.set('shaken', 'rotation', ...T.r0) }
      out.push(TA, TB)
    }
    return out
  }
  const introTweens = []
  let introPlayed = false
  function setIntroStart() {
    // initial pose before LOAD: checkerboard + title A lines below their masks
    introPrepared = prepareIntro()
    const l = titleA.lines
    l[0].position.z = -LH + HT; l[1].position.z = HT; l[2].position.z = LH + HT
  }
  function clearIntro() {
    for (const T of introPrepared || []) { T.x.set('shaken', 'position', 0, 0, 0); T.x.set('shaken', 'rotation', 0, 0, 0) }
    const l = titleA.lines
    l[0].position.z = -LH; l[1].position.z = 0; l[2].position.z = LH
    introPrepared = null
  }
  function playIntro() {
    if (introPlayed) return
    introPlayed = true
    if (HERO.enabled && HERO.progress >= 1) { clearIntro(); return }
    if (!introPrepared) setIntroStart()
    const items = introPrepared
    const ease = CustomEase.get('home::custom::out') || CustomEase.create('home::custom::out', 'M0,0 C0,1 0,0.903 1,1')
    const p1 = { progress: 0 }, p2 = { progress: 0 }, p3 = { progress: 0 }, p4 = { progress: 0 }
    introTweens.push(
      gsap.fromTo(p1, { progress: 0 }, { progress: 1, duration: 7.7, delay: 0, onUpdate: () => {
        const e = (1 - p1.progress) ** 3
        q.addShakenPosition(0, -10 * e, 3 * e, e)
      } }),
      gsap.fromTo(p2, { progress: 0 }, { progress: 1, duration: 1.5, delay: 0, onUpdate: () => {
        const n = 1 - (1 - p2.progress) ** 3
        for (const T of items) T.x.addShakenPosition(lerp(T.p0[0], T.p1[0], n), lerp(T.p0[1], T.p1[1], n), lerp(T.p0[2], T.p1[2], n), n)
      } }),
      gsap.fromTo(p3, { progress: 0 }, { progress: 1, duration: 7, delay: 1.1, onUpdate: () => {
        const e = p3.progress
        for (const T of items) {
          const i = clamp((e - T.delay) / T.duration)
          if (!i) continue
          const a = 1 - ease(i)
          T.x.addShakenPosition(T.p1[0] * a, T.p1[1] * a, T.p1[2] * a, a)
          T.x.addShakenRotation(T.r0[0] * a, T.r0[1] * a, T.r0[2] * a, a)
        }
      } }),
      gsap.fromTo(p4, { progress: 0 }, { progress: 1, duration: 4.7, delay: 0.9, onUpdate: () => {
        const e = (1 - p4.progress) ** 4
        titleA.x3d.addShakenPosition(0, 50 * e, 15 * e, e)
        titleA.x3d.addShakenRotation(-1.3 * e, 0, 0, e)
      } }),
      gsap.fromTo(titleA.lines[0].position, { z: -LH + HT }, { z: -LH, duration: 4.3, delay: 0.9, ease: 'custom::out' }),
      gsap.fromTo(titleA.lines[1].position, { z: HT }, { z: 0, duration: 4.3, delay: 1.1, ease: 'custom::out' }),
      gsap.fromTo(titleA.lines[2].position, { z: LH + HT }, { z: LH, duration: 4.3, delay: 1.3, ease: 'custom::out' }),
    )
  }

  return {
    sections: { HERO, TAG, WORKS, SKILLS },
    layoutFrame,
    tick: bob,
    startBob() { bobOn = true },
    setIntroStart,
    playIntro,
    get introPlayed() { return introPlayed },
    introTweens,
  }
}
