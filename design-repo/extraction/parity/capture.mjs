#!/usr/bin/env node
// Live-vs-clone parity capture (R12). Captures the SAME scroll offsets on one side and writes
// viewport screenshots + a text-free geometry dump to OUT_DIR (outside the repo: live screenshots
// are never committed). Run once per side, then compare with compare.py.
//
//   SIDE=clone URL=http://127.0.0.1:5181/ OUT_DIR=<scratch>/run1/clone node extraction/parity/capture.mjs
//   SIDE=live  URL=https://laboiteaslides.fr/ OUT_DIR=<scratch>/run1/live OFFSETS=<scratch>/run1/clone/geometry.json node extraction/parity/capture.mjs
//
// Determinism measures applied identically on both sides:
//   - viewport 1440x900, deviceScaleFactor 1, same Chromium build, reduced nothing (motion is the product)
//   - Math.random seeded (mulberry32, seed 20261106) before any page script runs
//   - every <video> paused and seeked to 0 before each shot (waits for `seeked`)
//   - consent/cookie overlays are NOT clicked: any fixed element whose id/class matches the consent
//     pattern is hidden with visibility:hidden (no layout change) and the count is recorded
//   - each shot is taken after scrolling to the offset and waiting SETTLE_MS (scrubbed timelines + the
//     WebGL scene's ~0.1 s transform smoothing settle)
//   - capture offsets come from OFFSETS (the clone's geometry) when given, so both sides are compared
//     at identical scrollY values; the side's own section tops are recorded for the layout check
// Env: SIDE, URL, OUT_DIR, OFFSETS (optional), SETTLE_MS (default 2200), GL (gpu|swiftshader, default gpu),
//      PLAYWRIGHT_MODULE, CHROME_PATH
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const selectors = JSON.parse(readFileSync(join(here, '..', 'section-selectors.json'), 'utf8')).sections
const SIDE = process.env.SIDE
const URL_ = process.env.URL
const OUT = process.env.OUT_DIR
if (!SIDE || !URL_ || !OUT) { console.error('SIDE, URL and OUT_DIR are required'); process.exit(2) }
const SETTLE = Number(process.env.SETTLE_MS || 2200)
const VW = 1440, VH = 900
const SAMPLES_TALL = [0.25, 0.5, 0.75]
// GL=gpu uses the machine's GPU through ANGLE (closest to a real visitor; the live site's layout was
// confirmed identical to the clone's 35 940 px this way); GL=swiftshader is the portable software path.
const GL = process.env.GL || 'gpu'
const GL_ARGS = {
  gpu: ['--enable-gpu', '--ignore-gpu-blocklist', ...(process.platform === 'darwin' ? ['--use-angle=metal'] : [])],
  swiftshader: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
}
const CONSENT = /cookie|consent|axeptio|didomi|tarteaucitron|cookiebot|onetrust|cookieyes|\bcmp\b|gdpr|rgpd/i
mkdirSync(OUT, { recursive: true })

const mod = await import(process.env.PLAYWRIGHT_MODULE || 'playwright-core')
const chromium = mod.chromium || mod.default?.chromium
const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}),
  args: [...GL_ARGS[GL], '--autoplay-policy=no-user-gesture-required'],
})
const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1, locale: 'fr-FR' })
await ctx.addInitScript(() => {
  let a = 20261106
  Math.random = () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296 }
})
const page = await ctx.newPage()
await page.goto(URL_, { waitUntil: 'load', timeout: 90000 })
await page.evaluate(() => document.fonts.ready)
await page.waitForTimeout(6000) // loader lift + 7 s custom::out intros are mostly settled; identical on both sides

const hideConsent = () => page.evaluate((src) => {
  const re = new RegExp(src, 'i')
  let n = 0
  for (const el of document.querySelectorAll('body *')) {
    const tag = `${el.id} ${typeof el.className === 'string' ? el.className : ''}`
    if (!re.test(tag)) continue
    const pos = getComputedStyle(el).position
    if (pos === 'fixed' || pos === 'sticky') { el.style.setProperty('visibility', 'hidden', 'important'); n++ }
  }
  return n
}, CONSENT.source)
const pauseVideos = () => page.evaluate(async () => {
  const vids = [...document.querySelectorAll('video')]
  await Promise.all(vids.map((v) => new Promise((res) => {
    try { v.pause() } catch {}
    if (v.readyState < 1 || v.currentTime === 0) return res()
    const t = setTimeout(res, 1500)
    v.addEventListener('seeked', () => { clearTimeout(t); res() }, { once: true })
    v.currentTime = 0
  })))
  return vids.length
})

const geometry = await page.evaluate((sel) => {
  const res = {}
  for (const [id, s] of Object.entries(sel)) {
    const q = s.liveSelector && !document.querySelector(s.selector) ? s.liveSelector : s.selector
    const el = document.querySelector(q)
    if (!el) { res[id] = { found: false }; continue }
    const docTop = (e) => e.getBoundingClientRect().top + window.scrollY
    let top = docTop(el)
    let h = el.getBoundingClientRect().height
    const from = s.range && document.querySelector(s.range.from)
    if (from) {
      top = docTop(from)
      const to = s.range.to && document.querySelector(s.range.to)
      const tb = s.range.toBottomOf && document.querySelector(s.range.toBottomOf)
      if (to) h = docTop(to) - top
      else if (tb) h = docTop(tb) + tb.getBoundingClientRect().height - top
    }
    res[id] = { found: true, via: q === s.selector ? 'selector' : 'liveSelector', ranged: !!from, topPx: Math.round(top * 10) / 10, heightPx: Math.round(h * 10) / 10, positionKind: s.positionKind }
  }
  return { documentHeightPx: document.documentElement.scrollHeight, htmlFontSizePx: parseFloat(getComputedStyle(document.documentElement).fontSize), sections: res }
}, selectors)

// capture offsets: from OFFSETS (clone geometry) if given, else from this side's own geometry
const base = process.env.OFFSETS ? JSON.parse(readFileSync(process.env.OFFSETS, 'utf8')).sections : geometry.sections
const maxY = geometry.documentHeightPx - VH
const shots = []
for (const [id, s] of Object.entries(selectors)) {
  if (s.positionKind !== 'in-flow') continue
  const g = base[id]
  if (!g || !g.found) { shots.push({ section: id, skipped: 'section not found' }); continue }
  const tall = g.heightPx > 1.5 * VH
  const ys = tall
    ? SAMPLES_TALL.map((f) => g.topPx + f * (g.heightPx - VH))
    : [g.topPx + g.heightPx / 2 - VH / 2]
  ys.forEach((y, i) => shots.push({ section: id, sample: i, scrollY: Math.round(Math.min(Math.max(y, 0), maxY)) }))
}
let consentHidden = 0
for (const sh of shots) {
  if (sh.skipped) continue
  await page.evaluate((y) => window.scrollTo(0, y), sh.scrollY)
  await page.waitForTimeout(SETTLE)
  consentHidden = Math.max(consentHidden, await hideConsent())
  sh.videos = await pauseVideos()
  await page.waitForTimeout(150)
  sh.actualScrollY = await page.evaluate(() => Math.round(window.scrollY))
  sh.file = `${sh.section}__${sh.sample}.png`
  await page.screenshot({ path: join(OUT, sh.file) })
}
writeFileSync(join(OUT, 'geometry.json'), JSON.stringify({ side: SIDE, url: URL_, capturedAt: new Date().toISOString(), viewport: `${VW}x${VH}`, settleMs: SETTLE, gl: GL, consentOverlaysHidden: consentHidden, ...geometry, shots }, null, 2))
await browser.close()
console.log(`${SIDE}: ${shots.filter((s) => s.file).length} shots, consent overlays hidden: ${consentHidden}, doc height ${geometry.documentHeightPx}`)
