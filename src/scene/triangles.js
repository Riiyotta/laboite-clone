// Glass triangles (spec §3.4 "Glass triangles") — mirrors reference/nuxt/BqBiTg5H.js.
import * as THREE from 'three'

export const TRIANGLE_SIZE = 10
export const TRIANGLE_DEPTH = 1
const SHORTEN = 0.05

function triangleShape() {
  const pts = [new THREE.Vector2(0, 0), new THREE.Vector2(TRIANGLE_SIZE, 0), new THREE.Vector2(0, TRIANGLE_SIZE)]
  const shorten = (a, b) => {
    const ang = Math.atan2(b.y - a.y, b.x - a.x), c = Math.cos(ang), s = Math.sin(ang)
    return [new THREE.Vector2(a.x + SHORTEN * c, a.y + SHORTEN * s), new THREE.Vector2(b.x - SHORTEN * c, b.y - SHORTEN * s)]
  }
  const edges = [shorten(pts[0], pts[1]), shorten(pts[1], pts[2]), shorten(pts[2], pts[0])]
  const shape = new THREE.Shape()
  shape.moveTo(edges[2][1].x, edges[2][1].y)
  for (let i = 0; i < 3; i++) {
    const v = pts[i], [a, b] = edges[i]
    shape.quadraticCurveTo(v.x, v.y, a.x, a.y)
    shape.lineTo(b.x, b.y)
  }
  return shape
}

export function createTriangleGeometry() {
  return new THREE.ExtrudeGeometry(triangleShape(), {
    depth: TRIANGLE_DEPTH, bevelEnabled: true, bevelThickness: 0.045, bevelSize: 0.3, bevelSegments: 5, curveSegments: 20,
  })
}

export function createGlassMaterial() {
  return new THREE.MeshPhysicalMaterial({
    color: 0xffffff, metalness: 0, roughness: 0.2, transparent: true, transmission: 1, ior: 1.7, thickness: 6,
    specularIntensity: 1, envMapIntensity: 0.6, clearcoat: 1, clearcoatRoughness: 0.1, dispersion: 0,
    attenuationColor: new THREE.Color(0xffffff), attenuationDistance: 3.5, iridescence: 0, iridescenceIOR: 1.3, depthWrite: true,
  })
}

// 22 meshes sharing one geometry + one material (mesh.clone() shares both, as in the original)
export function createTriangleMeshes(count) {
  const proto = new THREE.Mesh(createTriangleGeometry(), createGlassMaterial())
  proto.castShadow = true
  const meshes = []
  for (let i = 0; i < count; i++) {
    const m = proto.clone()
    m.name = `TRIANGLE_3D[${i}]`
    m.renderOrder = 1
    meshes.push(m)
  }
  return { meshes, material: proto.material, geometry: proto.geometry }
}
