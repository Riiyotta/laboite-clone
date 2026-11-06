// VR sticker scene (spec B §2.3–§2.5) — mirrors functions Pt / Ft / It and the VR parts of At / jt in
// reference/nuxt/DqzInzYb.js, plus the SPHERE / MASK plugins of reference/nuxt/Co2d9rFw.js.
//   timeline "VR": trigger [data-section="vr"], overflowStart = overflowEnd = lvh
//   headset GLB fly-through · RGB-shift pulse · hard cut to BLK (layer 7) · 80-image Fibonacci sphere ·
//   darkening plane in front of the camera · white wipe (layer 8) · camera p7 → p8
import * as THREE from 'three'
import { gsap, lvh } from '../lib/motion'
import { lerp } from './x3d'

// Spec B §9.2 — the 61 `small_*` thumbnails (CMS order); plane i uses texture i % 61.
export const SPHERE_TEXTURES = [
  'small_Adobe_Stock_206118370_5ab61dcb89', 'small_Brasseries_kronenbourg_2_ef3160d1cb', 'small_Brico_Depot_9265283144',
  'small_Econocom_1_bbf2deda06', 'small_Candriam_d7ec4211ac', 'small_Brasseries_kronenbourg_3_2c511aaf16',
  'small_Brasseries_kronenbourg_c4aa37d707', 'small_Live_cam_powerpoint_66ba77a3d6', 'small_Live_cam_Realite_Augmentee_powerpoint_1_326712230e',
  'small_Econocom_2_b5451e30d7', 'small_Econocom_3_09b37caa26', 'small_Econocom_4_d6a171dce4', 'small_Limatech_0200a6e1da',
  'small_Live_cam_Realite_Augmentee_powerpoint_2_0da8adf478', 'small_qui_veut_gagner_des_millions_7ec0f870fa', 'small_Trivial_Pursuit_8a4b25c1ca',
  'small_Maison_Perrier_Award_219180308a', 'small_Maison_Perrier_6c1d185c63', 'small_Maison_Perrier_Chic_2e80303fbc',
  'small_Trivial_Pursuit_5_Trivial_Pursuit_6_34207ab249', 'small_Trivial_Pursuit_5_e5e59ced1f', 'small_Trivial_Pursuit_3_7f9cf56cb4',
  'small_Trivial_Pursuit_2_6fafb6e677', 'small_Trivial_Pursuit_4_07eee46f2f', 'small_twix_snickers_a4c29b83f1', 'small_Araymond_4eb84ffff0',
  'small_Vaudoise_0b797b5987', 'small_Adidas_20ec508fa3', 'small_Audiens_b499a54b85', 'small_Axa_aide_a_la_vente_a02a510b23',
  'small_Axa_ed688ebfaa', 'small_Babymoov_cb337e2d48', 'small_Caterpillar_2278246ff0', 'small_Chanel_f654a93dae', 'small_CBRE_00fce42506',
  'small_Coface_144ab51cdd', 'small_Essity_9872bcbd26', 'small_JDM_PRES_PPT_04_1_e2c5eec858', 'small_Flextone_1839960e8e',
  'small_General_Motors_0fde66cf2b', 'small_M_and_Ms_mini_e4ae435636', 'small_Liebig_2b76ec3546', 'small_Marie_9cca944ff8',
  'small_Nissan_aa945746e2', 'small_Nuxe_72b8bd830c', 'small_Mars_wrigley_ac9f9d1412', 'small_Pukka_9c6a08bda9',
  'small_Renault_electric_dcecf4d28c', 'small_Renault_dd9391e8d8', 'small_Saur_cbcd180b87', 'small_Safran_bc185c343c',
  'small_The_edge_1_5cf73378d2', 'small_The_edge_1_2_bef5289ffc', 'small_Renault_ev_forum_f11bc1287b', 'small_Ship_up_73ecf0f94b',
  'small_Total_energies_8ec1dc0287', 'small_Upcoop_f8ef861fe9', 'small_wolf_oil_e2c4402e3a', 'small_Viridien_bbd464d417',
  'small_Vittel_980cb8f103', 'small_Tishman_speyer_10c8fc2359',
].map((n) => `/sk/uploads/${n}.jpg`)

// SPHERE plugin constants (Co2d9rFw.js class Yr)
const SPHERE_RADIUS = 10
const GOLDEN = Math.PI * (3 - Math.sqrt(5))
const SPHERE_LENGTH = 80
const IMG_W = 3
const IMG_H = (IMG_W * 9) / 16
const MASK_COLOR = 0x080808 // B1RHjsqj.js `t` = 526344

const L3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)]
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v)

function sphereGeometry() {
  const g = new THREE.PlaneGeometry(IMG_W, IMG_H, 5, 3)
  const p = g.attributes.position
  for (let i = 0; i < p.count; i++) p.setZ(i, Math.sqrt(p.getX(i) ** 2 + p.getY(i) ** 2) * 0.1)
  p.needsUpdate = true
  return g
}

// $Scroll.__scroll_toMotion(top, n) (Co2d9rFw.js): every tick move the Lenis target n px toward `top`;
// stops once reached or as soon as the user scrolls the other way.
let stopMotion = null
function scrollToMotion(top, n) {
  const lenis = window.lenis
  if (!lenis) return
  stopMotion?.()
  let r = lenis.scroll
  const d = top - r
  const [a, o] = d < 0 ? [top, r] : [r, top]
  if (n <= 0) n = 10
  let c = d < 0 ? -1 : 1
  const onScroll = () => { c = lenis.scroll < r ? -1 : 1; r = lenis.scroll }
  const tick = () => {
    const l = clamp(r + n * c, a, o)
    if (c > 0 ? l === o : l === a) stop()
    lenis.scrollTo(l)
  }
  const off = lenis.on('scroll', onScroll)
  const stop = () => { off(); gsap.ticker.remove(tick); if (stopMotion === stop) stopMotion = null }
  stopMotion = stop
  gsap.ticker.add(tick)
}

export function setupVr(ctx) {
  const { sections, camera, bg, vr, rgbShift, RGB_SHIFT_DEFAULT_AMOUNT, data, addX3D, addTicker, scene } = ctx
  const H = data.DATA_CAMERA_3D, G = data.DATA_VR_MASK_3D, K = data.DATA_SPHERE_3D
  const Y = vr.x3d

  const V = sections.add({ name: 'VR', selector: '[data-section="vr"]', overflowStart: lvh, overflowEnd: lvh })

  // ---------------- background (At) : layer 7 hard cut is in the headset tracks; layer 8 wipe ----------------
  const L7 = bg.layers[6], L8 = bg.layers[7]
  V.tween({ start: 0.97, overflowEnd: 0.7, ease: 'none' }, (v) => { L8.uTransition.value = v; L8.uCurveAmount.value = 0.3 - 0.3 * v })

  // ---------------- camera (jt) : P7 -> P8 ----------------
  V.track({ start: 0.99, end: 1 }, (p, imm) => { const P = L3(H.p7, H.p8, p); camera.addPosition(P[0], P[1], P[2], p, imm) })

  // ---------------- VR headset (Pt) ----------------
  const n = 0.25, r = 0.6
  const show = (v) => { Y.root.visible = v }
  // Original: `t = spider.RGBShaderPass?.uniforms.amount ?? {value:0}` captured at setup. Live frames (22 973, 23 423)
  // show NO colour fringing in this range, i.e. the pass is not yet created there and the pulse writes into the dummy.
  // Matched to the observed output: the formula runs but does not drive the real pass.
  const amount = { value: RGB_SHIFT_DEFAULT_AMOUNT }
  void rgbShift
  const pos = (a, b) => (p, imm) => { const P = L3(G[a], G[b], p); Y.addPosition(P[0], P[1], P[2], p, imm) }
  const rotT = (a, b) => (p, imm) => { const R = L3(G[a], G[b], p); Y.addRotation(R[0], R[1], R[2], p, imm) }
  V.track({ start: 0, end: 0.15 }, (p, imm) => { pos('p0', 'p1')(p, imm); rotT('r0', 'r1')(p, imm) },
    { onEnter: () => show(true), onLeaveBack: () => show(false) })
    .track({ start: 0.13, end: n }, (p, imm) => { pos('p1', 'p2')(p, imm); rotT('r1', 'r2')(p, imm) })
    .track({ start: n, end: r }, (p) => { amount.value = RGB_SHIFT_DEFAULT_AMOUNT + Math.sin(Math.PI * (1 - (1 - p) ** 1.7)) / 30 }, {
      onEnter: (imm, syncing) => { if (!imm && !syncing) scrollToMotion(V.getTop(0.65), 150) },
      onEnterBack: (imm, syncing) => { show(true); if (!imm && !syncing) scrollToMotion(V.getTop(0.2), 200) },
      onLeave: () => show(false),
    })
    .track({ start: n, end: 0.35 }, pos('p2', 'p3'))
    .track({ start: 0.35, end: 0.45 }, (p, imm) => {
      pos('p3', 'p4')(p, imm)
      const o = 1 - p ** 2
      for (const m of vr.fadeMeshes) {
        if (Array.isArray(m.material)) m.material.forEach((x) => { x.opacity = o })
        else m.material.opacity = o
      }
      const g = vr.glass
      if (g) g.material.opacity = (1 - p) ** 5
    }, { onEnter: () => { L7.uTransition.value = 1 }, onLeaveBack: () => { L7.uTransition.value = 0 } })
    .track({ start: 0.45, end: r }, pos('p4', 'p5'))

  // ---------------- image sphere (SPHERE plugin + Ft) ----------------
  const sphereRoot = new THREE.Group()
  const X = addX3D(sphereRoot, { name: 'SPHERE_3D' })
  const geo = sphereGeometry()
  const baseMat = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, depthWrite: true })
  const planes = []
  const points = []
  const _m4 = new THREE.Matrix4(), _eul = new THREE.Euler(), _up = new THREE.Vector3(0, 1, 0)
  for (let l = 0, u = SPHERE_LENGTH - 1; l < SPHERE_LENGTH; l++) {
    const a = 1 - (l / u) * 2
    const d = Math.sqrt(1 - a ** 2)
    const f = GOLDEN * l
    const P = [Math.cos(f) * d * SPHERE_RADIUS, a * SPHERE_RADIUS, Math.sin(f) * d * SPHERE_RADIUS]
    const mesh = new THREE.Mesh(geo, baseMat.clone())
    const h = addX3D(mesh, { name: `IMAGE_3D[${l}]` })
    h.setPosition(...P)
    const eye = mesh.position.clone()
    _eul.setFromRotationMatrix(_m4.lookAt(eye, eye.clone().add(new THREE.Vector3(...P).normalize()), _up))
    h.setRotation(_eul.x, _eul.y, _eul.z)
    sphereRoot.add(mesh)
    planes.push(h)
    points.push([P, [P[0] * 1.7, P[1] * 1.7, P[2] * 1.7]])
  }
  X.setPosition(...K.p0); X.setRotation(...K.r0); X.setScale(...K.s0)
  sphereRoot.visible = false
  scene.add(sphereRoot)

  // textures (TextureLoader, sRGB, repeat wrapping) — plane i ← texture i % 61
  const textures = []
  const loader = new THREE.TextureLoader()
  const texturesReady = Promise.all(SPHERE_TEXTURES.map((url, i) => new Promise((res) => {
    loader.load(url, (t) => {
      t.colorSpace = THREE.SRGBColorSpace
      t.wrapS = t.wrapT = THREE.RepeatWrapping
      textures[i] = t
      for (let k = i; k < planes.length; k += SPHERE_TEXTURES.length) { const m = planes[k].root.material; m.map = t; m.needsUpdate = true }
      res(t)
    }, undefined, () => { console.error('[SYNTHRA] sphere texture failed', url); res(null) })
  })))

  // spin (BASIC plugin Ke): while shown, rotationY_extra -= delta * .1
  let spinOff = true
  let spin = 0
  const removeSpin = addTicker((dt) => { if (!spinOff) X.addNoisyRotation(0, (spin -= dt * 0.1), 0, 0) })
  const setHidden = (hidden) => { spinOff = hidden; sphereRoot.visible = !hidden } // Yt(e)

  V.track({ start: 0.4, end: 0.6 }, (p, imm) => {
    const i = 1 - (1 - p) ** 2
    const S = L3(K.s0, K.s1, i)
    X.addScale(S[0], S[1], S[2], p, imm)
  }, { onEnter: () => setHidden(false), onLeaveBack: () => setHidden(true) })
    .track({ start: 0.4, end: 0.71 }, (p, imm) => {
      const i = 1 - (1 - p) ** 2
      const P = L3(K.p0, K.p1, i), R = L3(K.r0, K.r1, i)
      X.addPosition(P[0], P[1], P[2], i, imm)
      X.addRotation(R[0], R[1], R[2], i, imm)
    })
    .track({ start: 0.5, end: 0.9 }, (p, imm) => {
      const o = p ** 2
      for (let k = 0; k < planes.length; k++) {
        const [a, b] = points[k]
        planes[k].addPosition(lerp(a[0], b[0], o), lerp(a[1], b[1], o), lerp(a[2], b[2], o), o, imm)
      }
    }, { onEnterBack: () => setHidden(false), onLeave: () => setHidden(true) })

  // ---------------- darkening plane (MASK plugin + It) ----------------
  const mask = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({
    color: new THREE.Color(MASK_COLOR), opacity: 0, transparent: true, depthWrite: false, depthTest: false, side: THREE.FrontSide,
  }))
  mask.name = 'MASK'
  mask.position.z = -1
  mask.renderOrder = 2
  mask.frustumCulled = false
  mask.visible = false
  camera.root.add(mask)
  function resize() {
    // world.getRect(|z|): visible width/height at distance 1 from the camera
    const h = Math.tan(THREE.MathUtils.degToRad(camera.root.fov / 2)) * Math.abs(mask.position.z) * 2
    mask.scale.set(h * camera.root.aspect, h, 1)
  }
  resize()
  V.track({ start: 0.65, end: 0.7 }, (p) => { mask.material.opacity = p * 0.5 }, { onEnter: () => { mask.visible = true }, onLeaveBack: () => { mask.visible = false } })
    .track({ start: 0.8, end: 0.9 }, (p) => { mask.material.opacity = 0.5 + p * 0.5 })
    .track({ start: 0.9, end: 1 }, (p) => { mask.material.opacity = 1 - p }, { onEnterBack: () => { mask.visible = true }, onLeave: () => { mask.visible = false } })

  // pre-compile headset + sphere programs so the first visible frame doesn't hitch (original: spider.compile())
  const compileHidden = (root) => {
    const was = root.visible
    root.visible = true
    try { ctx.renderer.compile(scene, camera.root) } catch { /* ignore */ }
    root.visible = was
  }
  vr.ready.then((root) => { if (root) compileHidden(root) })
  texturesReady.then(() => compileHidden(sphereRoot))

  return {
    section: V,
    sphere: { x3d: X, root: sphereRoot, planes, textures, ready: texturesReady },
    mask,
    resize,
    setWhole(w) {
      if (!w) { setHidden(true); mask.visible = false; Y.root.visible = false; stopMotion?.() }
    },
    dispose() {
      removeSpin(); stopMotion?.()
      camera.root.remove(mask); mask.geometry.dispose(); mask.material.dispose()
      geo.dispose(); baseMat.dispose(); for (const p of planes) p.root.material.dispose()
      for (const t of textures) t?.dispose()
      scene.remove(sphereRoot)
    },
  }
}
