// Smoothed transform wrapper — reproduces the original "X3D/spider" model (reference Co2d9rFw.js):
//   final = canonical + noisy + shaken   (per position / rotation / scale, component-wise; rotation is Euler XYZ)
//   Each channel keeps a target = weighted average of all contributions received during the current tick,
//   weight = max(sin(progress·π), 1e-4); every frame value += (target − value)·(1 − e^(−10·dt)),
//   snapping when |target − value|² < 1e-8. Contributions flagged `immediate` (track jumped over in a single
//   scroll update) set the value directly, as in the original.

const EPS2 = 1e-8
const W_MIN = 1e-4
let TICK = 0
export const nextTick = () => ++TICK
export const currentTick = () => TICK

const KINDS = ['canon', 'noisy', 'shaken']
const PROPS = ['position', 'rotation', 'scale']

function channel(x = 0, y = 0, z = 0) {
  return { v: [x, y, z], t: [x, y, z], acc: [0, 0, 0, 0], tick: -1, active: false }
}

export class X3D {
  constructor(root, { speed = 10, name } = {}) {
    this.root = root
    if (name) root.name = name
    this.speed = speed
    this.ch = {}
    for (const k of KINDS) {
      this.ch[k] = {}
      for (const p of PROPS) {
        const base = k === 'canon' ? root[p] : null
        this.ch[k][p] = base ? channel(base.x, base.y, base.z) : channel()
      }
    }
    this.onPosition = null // attachment fired after position recomposes (camera lookAt)
  }
  get pX() { return this.ch.canon.position.v[0] }
  get pY() { return this.ch.canon.position.v[1] }
  get pZ() { return this.ch.canon.position.v[2] }
  get rX() { return this.ch.canon.rotation.v[0] }
  get rY() { return this.ch.canon.rotation.v[1] }
  get rZ() { return this.ch.canon.rotation.v[2] }

  // immediate set (setPosition / setShakenPosition …)
  set(kind, prop, x, y, z) {
    const c = this.ch[kind][prop]
    c.v[0] = x; c.v[1] = y; c.v[2] = z
    if (!c.active) { c.t[0] = x; c.t[1] = y; c.t[2] = z }
    this.compose(prop)
  }
  // smoothed contribution (addPosition / addNoisyPosition / addShakenPosition …)
  add(kind, prop, x, y, z, progress = 0, immediate = false) {
    const c = this.ch[kind][prop]
    if (immediate) {
      c.v[0] = x; c.v[1] = y; c.v[2] = z
      if (c.tick !== TICK) { c.active = false; c.t[0] = x; c.t[1] = y; c.t[2] = z }
      this.compose(prop)
      return
    }
    const w = Math.max(Math.sin(progress * Math.PI), W_MIN)
    const a = c.acc
    if (c.active && c.tick === TICK) { a[0] += x * w; a[1] += y * w; a[2] += z * w; a[3] += w }
    else { a[0] = x * w; a[1] = y * w; a[2] = z * w; a[3] = w; c.tick = TICK }
    c.t[0] = a[0] / a[3]; c.t[1] = a[1] / a[3]; c.t[2] = a[2] / a[3]
    c.active = true
  }
  setPosition(x, y, z) { this.set('canon', 'position', x, y, z) }
  setRotation(x, y, z) { this.set('canon', 'rotation', x, y, z) }
  setScale(x, y, z) { this.set('canon', 'scale', x, y, z) }
  addPosition(x, y, z, p, imm) { this.add('canon', 'position', x, y, z, p, imm) }
  addRotation(x, y, z, p, imm) { this.add('canon', 'rotation', x, y, z, p, imm) }
  addScale(x, y, z, p, imm) { this.add('canon', 'scale', x, y, z, p, imm) }
  addNoisyPosition(x, y, z, p) { this.add('noisy', 'position', x, y, z, p) }
  addNoisyRotation(x, y, z, p) { this.add('noisy', 'rotation', x, y, z, p) }
  addShakenPosition(x, y, z, p) { this.add('shaken', 'position', x, y, z, p) }
  addShakenRotation(x, y, z, p) { this.add('shaken', 'rotation', x, y, z, p) }

  update(dt) {
    const f = 1 - Math.exp(-this.speed * dt)
    for (const p of PROPS) {
      let dirty = false
      for (const k of KINDS) {
        const c = this.ch[k][p]
        if (!c.active) continue
        dirty = true
        const dx = c.t[0] - c.v[0], dy = c.t[1] - c.v[1], dz = c.t[2] - c.v[2]
        if (dx * dx + dy * dy + dz * dz < EPS2) { c.v[0] = c.t[0]; c.v[1] = c.t[1]; c.v[2] = c.t[2]; c.active = false }
        else { c.v[0] += dx * f; c.v[1] += dy * f; c.v[2] += dz * f }
      }
      if (dirty) this.compose(p)
    }
  }
  compose(p) {
    const a = this.ch.canon[p].v, b = this.ch.noisy[p].v, c = this.ch.shaken[p].v
    this.root[p].set(a[0] + b[0] + c[0], a[1] + b[1] + c[1], a[2] + b[2] + c[2])
    if (p === 'position' && this.onPosition) this.onPosition(this)
  }
}

export const lerp = (a, b, t) => a - (a - b) * t
