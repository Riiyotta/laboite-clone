// Tiny pub/sub store shared between DOM sections and the WebGL scene.
const state = {
  loaded: false,        // loader finished
  menuOpen: false,
  headerLight: true,    // spec §1.3
  lightRegions: [],     // DOM elements that force a light header (e.g. works cards grid)
}
const subs = new Set()
export const store = {
  get: () => state,
  set(patch) { Object.assign(state, patch); subs.forEach((f) => f(state)) },
  subscribe(f) { subs.add(f); return () => subs.delete(f) },
}
// The WebGL scene exposes its controllable objects here once ready (see src/scene/).
export const sceneBus = { ready: false, api: null, listeners: new Set(),
  onReady(f) { if (this.ready) f(this.api); else this.listeners.add(f) },
  resolve(api) { this.api = api; this.ready = true; this.listeners.forEach((f) => f(api)); this.listeners.clear() } }
