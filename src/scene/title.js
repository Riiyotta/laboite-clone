// 3D clipped title lines (spec §3.4 "3D title") — mirrors the TITLE plugin in reference/nuxt/Co2d9rFw.js.
import * as THREE from 'three'
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js'
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js'

const SIZE = 9.5
export const TITLE = { HEIGHT: 0, BASE: 0, LINE_HEIGHT: 0, font: null }

export async function loadTitleFont() {
  if (TITLE.font) return TITLE.font
  const font = await new FontLoader().loadAsync('/assets/fonts/FK Screamer Legacy Upright_Regular.json')
  const d = font.data
  const desc = (d.descender / d.resolution) * SIZE
  TITLE.HEIGHT = (d.ascender / d.resolution) * SIZE - desc
  TITLE.BASE = TITLE.HEIGHT / 2 + desc
  TITLE.LINE_HEIGHT = TITLE.HEIGHT * 0.71
  TITLE.font = font
  return font
}

export const maskStep = (i) => TITLE.LINE_HEIGHT * (0.5 + i) + (TITLE.HEIGHT - TITLE.LINE_HEIGHT) / 2
export const maskStep2 = (i, n = 1) => maskStep(i) - TITLE.HEIGHT * n

const baseMaterial = () => new THREE.MeshBasicMaterial({ side: THREE.FrontSide, transparent: false, depthWrite: true, depthTest: true, clipShadows: true })

// hex '#RRGGBB' → raw /255 components fed to Color(r,g,b) (no sRGB→linear conversion, as in the original)
export const rawColor = (hex) => {
  const h = hex.replace('#', '')
  return new THREE.Color(parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255)
}

// linesData: [{ text, color: '#hex', position:[x,y,z], rotation:[x,y,z], mask: i }]
export function buildTitle(group, linesData) {
  const lines = [], masks = []
  const mat = baseMaterial()
  for (const L of linesData) {
    const geo = new TextGeometry(L.text, { font: TITLE.font, size: SIZE, depth: 0.1, curveSegments: 8, bevelEnabled: false })
    geo.computeBoundingBox()
    geo.translate(-(geo.boundingBox.max.x + geo.boundingBox.min.x) / 2, -TITLE.BASE, 0)
    const m = mat.clone()
    m.color.copy(rawColor(L.color))
    const mesh = new THREE.Mesh(geo, m)
    mesh.renderOrder = 2
    mesh.position.set(...L.position)
    if (L.rotation) mesh.rotation.set(...L.rotation)
    const plane = new THREE.Plane(new THREE.Vector3(0, 0, -1), maskStep(L.mask))
    m.clippingPlanes = [plane]
    m.needsUpdate = true
    masks.push(plane)
    group.add(mesh)
    lines.push(mesh)
  }
  return { lines, masks }
}
