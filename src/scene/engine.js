// SYNTHRA — full-screen WebGL scene (spec §3.4). Owns: renderer/composer/camera, background layers, env,
// glass triangles, 3D titles, scroll section phases, X3D smoothing and the header light/dark computation (§1.3).
import * as THREE from 'three'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import { RGBShiftShader } from 'three/examples/jsm/shaders/RGBShiftShader.js'
import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { gsap, ScrollTrigger, isWhole, lvh } from '../lib/motion'
import { store } from '../lib/store'
import { X3D, nextTick, lerp } from './x3d'
import { createBackground } from './background'
import { createTriangleMeshes } from './triangles'
import { loadTitleFont, buildTitle, TITLE } from './title'
import { SceneSection } from './timeline'
import { setupHome } from './home'
import { setupVr } from './vr'
import { setupBottom } from './bottom'
import * as DATA from './data'

export const RGB_SHIFT_DEFAULT_AMOUNT = 0.00128

const pixelRatio = () => {
  const ua = navigator.userAgent || ''
  const winLinux = /Windows|Win64|Win32/i.test(ua) || (/Linux/i.test(ua) && !/Android/i.test(ua))
  return Math.min(window.devicePixelRatio || 1, winLinux ? 2 : 1.5)
}
// mouse parallax curve (reference B-0jv5Ee.js `J`)
const J = (e) => (e < 0.5 ? (e * 2) ** 2 - 1 : 1 - (1 - (e - 0.5) * 2) ** 2) * 1e-3

// deep clone of keyframes so the frame layout can mutate p2 per instance
const cloneData = () => JSON.parse(JSON.stringify({
  DATA_CAMERA_3D: DATA.DATA_CAMERA_3D, DATA_TRIANGLES_3D: DATA.DATA_TRIANGLES_3D,
  DATA_TRIANGLES_3D_CHILDREN: DATA.DATA_TRIANGLES_3D_CHILDREN, DATA_VR_MASK_3D: DATA.DATA_VR_MASK_3D, DATA_SPHERE_3D: DATA.DATA_SPHERE_3D,
}))

// ---------------------------------------------------------------------------------------------------------------
export async function createScene(canvas) {
  let disposed = false
  let whole = isWhole()
  const W = () => window.innerWidth, Hh = () => lvh()

  // ---- renderer / scene / camera ----
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', canvas })
  renderer.outputColorSpace = THREE.LinearSRGBColorSpace
  renderer.toneMapping = THREE.NoToneMapping
  renderer.localClippingEnabled = true
  const scene = new THREE.Scene()
  const cam = new THREE.PerspectiveCamera(45, W() / Hh(), 0.1, 500)
  scene.add(cam)
  const camera = new X3D(cam, { name: 'CAMERA_3D' })
  const _m4 = new THREE.Matrix4(), _eye = new THREE.Vector3(), _target = new THREE.Vector3(0, 0, 0), _up = new THREE.Vector3(0, 1, 0)
  const _eul = new THREE.Euler(0, 0, 0, 'XZY')
  const lookAtOrigin = () => {
    _eye.copy(cam.position)
    _eul.setFromRotationMatrix(_m4.lookAt(_eye, _target, _up))
    camera.setRotation(_eul.x, _eul.y, _eul.z) // applied with the camera's default 'XYZ' order — same as the original
  }
  camera.onPosition = lookAtOrigin
  camera.setPosition(0, 0, 1)

  const rt = new THREE.WebGLRenderTarget(W(), Hh(), { samples: Math.min(2, renderer.capabilities.maxSamples) })
  const composer = new EffectComposer(renderer, rt)
  composer.addPass(new RenderPass(scene, cam))
  const rgbShift = new ShaderPass(RGBShiftShader)
  rgbShift.uniforms.angle.value = 2
  rgbShift.uniforms.amount.value = RGB_SHIFT_DEFAULT_AMOUNT
  composer.addPass(rgbShift)

  function resizeRenderer() {
    const pr = pixelRatio()
    renderer.setSize(W(), Hh(), false)
    renderer.setPixelRatio(pr)
    composer.setSize(W(), Hh())
    composer.setPixelRatio(pr)
    cam.aspect = W() / Hh()
    cam.updateProjectionMatrix()
  }
  resizeRenderer()

  // ---- background ----
  const bg = createBackground()
  scene.add(bg.mesh)

  // ---- environment ----
  let envResolve
  const envReady = new Promise((r) => { envResolve = r })
  new HDRLoader().load('/assets/hdr/studio_small_08_1k.hdr', (tex) => {
    if (disposed) return tex.dispose()
    tex.mapping = THREE.EquirectangularReflectionMapping
    scene.environment = tex
    envResolve(tex)
  }, undefined, (err) => console.error('[SYNTHRA] HDR load failed', err))

  // ---- data / triangles ----
  const data = cloneData()
  const childrenData = data.DATA_TRIANGLES_3D_CHILDREN
  const trianglesRoot = new THREE.Group()
  const group = new X3D(trianglesRoot, { name: 'TRIANGLES_3D' })
  const { meshes, material } = createTriangleMeshes(childrenData.length)
  const children = meshes.map((m, i) => {
    trianglesRoot.add(m)
    const x = new X3D(m)
    x.setPosition(...childrenData[i].p0)
    x.setRotation(...childrenData[i].r0)
    return x
  })
  scene.add(trianglesRoot)

  // ---- titles ----
  await loadTitleFont()
  if (disposed) return null
  const LH = TITLE.LINE_HEIGHT
  const rot = [-Math.PI / 2, 0, 0]
  const mkTitle = (texts, colors) => {
    const root = new THREE.Group()
    const x = new X3D(root, { name: 'TITLE_3D' })
    const { lines, masks } = buildTitle(root, [
      { text: texts[0].toUpperCase(), color: colors[0], position: [0, 0.99, -LH], rotation: rot, mask: -1 },
      { text: texts[1].toUpperCase(), color: colors[1], position: [0, 1, 0], rotation: rot, mask: 0 },
      { text: texts[2].toUpperCase(), color: colors[2], position: [0, 1.01, LH], rotation: rot, mask: 1 },
    ])
    scene.add(root)
    return { x3d: x, root, lines, masks }
  }
  const titleA = mkTitle(['Les meilleures', 'idées font', "l'avenir"], ['#FFFFFF', '#FFFFFF', '#120042'])
  const titleB = mkTitle(['Quand elles', 'sont bien', 'présentées'], ['#120042', '#120042', '#6630FF'])

  // ---- sections registry (extension point for the bottom-half sections) ----
  const list = []
  const sections = {
    list,
    add(opts) { const s = new SceneSection(opts); list.push(s); if (ready) { s.measure(); s.sync(window.scrollY) } return s },
    get(name) { return list.find((s) => s.name === name) },
    measure() { for (const s of list) s.measure(); list.sort((a, b) => a.startPx - b.startPx) },
    sync() { const y = window.scrollY; for (const s of list) s.sync(y) },
    update() { const y = window.scrollY; for (const s of list) s.update(y) },
    reset() { for (const s of list) { s.synced = false; s.active.clear(); s.progress = 0 } },
  }
  let ready = false

  const x3ds = new Set([camera, group, ...children, titleA.x3d, titleB.x3d])
  const home = setupHome({ sections, camera, tri: { group, children, material, root: trianglesRoot }, titleA, titleB, bg, data })
  home.setIntroStart()

  // ---- VR headset (loaded at init like the original; driven later by the VR section) ----
  const vrRoot = new THREE.Group()
  const vr = new X3D(vrRoot, { name: 'VR_MASK_3D' })
  const VRD = data.DATA_VR_MASK_3D
  vr.setPosition(...VRD.p0); vr.setRotation(...VRD.r0); vr.setScale(...VRD.s0)
  vrRoot.visible = false
  scene.add(vrRoot)
  x3ds.add(vr)
  const vrFade = [] // meshes Object_183/181/157 (made transparent)
  let vrGlass = null // Object_195
  const vrReady = new GLTFLoader().loadAsync('/assets/models/DECIMATE v2_compressed-compressed.glb').then(async (gltf) => {
    if (disposed) return null
    vrRoot.add(...gltf.scene.children)
    const env = await envReady
    vrRoot.traverse((o) => {
      if (!o.isMesh) return
      if (['Object_183', 'Object_181', 'Object_157'].includes(o.name)) {
        ;(Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => { m.transparent ||= true })
        vrFade.push(o)
      } else if (o.name === 'Object_195') {
        if (o.material?.isMeshPhysicalMaterial) { o.material.envMap = env; o.material.envMapIntensity = 1; o.material.needsUpdate = true }
        else {
          ;(Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose())
          o.material = new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: 0.1, transparent: true, transmission: 1, ior: 2, thickness: 0.5, specularIntensity: 1, envMap: env, envMapIntensity: 1, clearcoat: 1, clearcoatRoughness: 0.1, depthWrite: false, side: THREE.DoubleSide })
        }
        vrGlass = o
      }
    })
    return vrRoot
  }).catch((e) => { console.error('[SYNTHRA] VR mask load failed', e); return null })

  // ---- bottom half: VR sticker scene (spec B §2) + label-cards / footer layers and footer triangles (§0.2, §8.4) ----
  const addX3D = (obj3d, opts) => { const x = obj3d instanceof X3D ? obj3d : new X3D(obj3d, opts); x3ds.add(x); return x }
  const tickers = new Set() // extension: (dt, api) => void, run after the X3D update like Synthra BASIC plugins
  const addTicker = (f) => { tickers.add(f); return () => tickers.delete(f) }
  const vrScene = setupVr({
    sections, camera, bg, rgbShift, RGB_SHIFT_DEFAULT_AMOUNT, data, addX3D, addTicker, scene, renderer,
    vr: { x3d: vr, root: vrRoot, ready: vrReady, fadeMeshes: vrFade, get glass() { return vrGlass } },
  })
  const bottom = setupBottom({ sections, bg, addX3D, addTicker, scene })

  // ---- header light/dark (§1.3) ----
  let remPx = parseFloat(getComputedStyle(document.documentElement).fontSize) || 8.78
  let headerLight = store.get().headerLight
  function computeHeaderLight() {
    const hH = 12 * remPx
    const y = window.scrollY
    const probe = y + hH / 2
    const regions = [...(store.get().lightRegions || [])]
    if (!whole) {
      // mobile: hero, VR, label cards and footer broadcast a light region (VR / LabelCards / Footer `header` reactors)
      for (const sel of ['[data-section="hero"]', '[data-section="vr"]', '[data-section="label-cards"]', '[data-section="footer"]']) {
        const el = document.querySelector(sel); if (el) regions.push(el)
      }
    }
    for (const el of regions) {
      if (!el || !el.isConnected) continue
      const r = el.getBoundingClientRect()
      if (probe >= r.top + y && probe <= r.bottom + y) return true
    }
    const G = 1 - hH / Hh() / 2
    const states = bg.states()
    let lum = 1
    for (let i = states.length - 1; i > -1; i--) {
      const s = states[i]
      if (s.transition < G || !s.top) continue
      lum = 0.299 * s.top.r + 0.587 * s.top.g + 0.114 * s.top.b
      break
    }
    return lum < 0.5
  }
  function updateHeader() {
    const v = computeHeaderLight()
    if (v !== headerLight || store.get().headerLight !== v) { headerLight = v; store.set({ headerLight: v }) }
  }

  // ---- whole / mobile gating (§9) ----
  function applyWhole(w) {
    titleA.root.visible = titleB.root.visible = w
    rgbShift.enabled = w
    vrScene.setWhole(w)
    bottom.setWhole(w)
    if (!w) { for (const L of bg.layers) { L.uTransition.value = 0; L.uCurveAmount.value = 0.3 } trianglesRoot.visible = false; vrRoot.visible = false }
    else {
      trianglesRoot.visible = true
      bg.layers[0].uTransition.value = 1; bg.layers[0].uCurveAmount.value = 0; bg.layers[6].uCurveAmount.value = 0
      sections.reset()
      sections.measure()
      sections.sync()
    }
  }

  // ---- input / resize ----
  const onMouse = (e) => { if (whole) camera.addNoisyRotation(J(e.clientY / Hh()), J(e.clientX / W()), 0, 0) }
  window.addEventListener('mousemove', onMouse, { passive: true })
  const onResize = () => {
    remPx = parseFloat(getComputedStyle(document.documentElement).fontSize) || remPx
    resizeRenderer()
    home.layoutFrame()
    vrScene.resize()
    const w = isWhole()
    if (w !== whole) { whole = w; applyWhole(w); tryIntro(store.get()) }
    else if (whole) { sections.measure(); sections.sync() }
  }
  window.addEventListener('resize', onResize)
  const onRefresh = () => { if (!whole) return; sections.measure(); sections.sync() }
  ScrollTrigger.addEventListener('refresh', onRefresh)
  // sections may still be stubs / grow later: refresh ScrollTrigger when the document height changes
  let roT = 0
  const ro = new ResizeObserver(() => { clearTimeout(roT); roT = setTimeout(() => ScrollTrigger.refresh(), 150) })
  ro.observe(document.body)

  // ---- frame loop (gsap ticker → runs after Lenis) ----
  const frame = (time, deltaMs) => {
    const dt = Math.min(deltaMs / 1000, 0.25)
    if (whole && ready) sections.update()
    for (const x of x3ds) x.update(dt)
    if (whole) home.tick(dt)
    for (const f of tickers) f(dt, api)
    bg.tick(dt)
    updateHeader()
    composer.render(dt)
    nextTick()
  }

  // ---- intro on LOAD ----
  const tryIntro = (s) => { if (s.loaded && whole && !home.introPlayed) home.playIntro() }
  const unsub = store.subscribe(tryIntro)

  // ---- boot ----
  if (!whole) applyWhole(false)
  else { sections.measure(); sections.sync() }
  ready = true
  home.startBob()
  // first render compiles shaders before the loader lifts
  renderer.compile(scene, cam)
  gsap.ticker.add(frame)
  ScrollTrigger.refresh()
  tryIntro(store.get())

  const api = {
    THREE, renderer, scene, composer, rgbShift, RGB_SHIFT_DEFAULT_AMOUNT,
    camera, // X3D (camera.root = PerspectiveCamera)
    background: bg, // { layers[0..9] (k = index+1): { uTransition, uCurveAmount, top, bottom }, final (PRM), uniforms, states() }
    triangles: { group, children, material, root: trianglesRoot, data: childrenData, groupData: data.DATA_TRIANGLES_3D },
    titles: { A: titleA, B: titleB, metrics: TITLE },
    vr: { x3d: vr, root: vrRoot, ready: vrReady, fadeMeshes: vrFade, get glass() { return vrGlass }, data: VRD },
    data, envReady,
    sections, // registerSection: sections.add({ name, selector, overflowStart: () => px, overflowEnd: () => px }) → SceneSection
    home,
    X3D, lerp,
    vrScene, // { section (timeline "VR"), sphere { x3d, root, planes, textures, ready }, mask }
    bottom, // { ranges (layers 9/10/final), footer { x3d, root, children, material, section } }
    addX3D,
    removeX3D(x) { x3ds.delete(x) },
    addTicker,
    playIntro: () => home.playIntro(),
    refresh: () => ScrollTrigger.refresh(),
    get whole() { return whole },
    get headerLight() { return headerLight },
    dispose() {
      disposed = true
      gsap.ticker.remove(frame)
      unsub()
      ro.disconnect()
      ScrollTrigger.removeEventListener('refresh', onRefresh)
      window.removeEventListener('mousemove', onMouse)
      window.removeEventListener('resize', onResize)
      for (const t of home.introTweens) t.kill()
      for (const s of list) s.kill()
      vrScene.dispose(); bottom.dispose()
      composer.dispose(); rt.dispose(); renderer.dispose()
    },
  }
  return api
}
