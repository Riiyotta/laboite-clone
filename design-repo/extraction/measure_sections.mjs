#!/usr/bin/env node
// Re-measure section heights of the served clone with a headless Chromium (optional tool; the
// recorded numbers in measured-values.json are what verify_all.py / wrapper_gate.py check).
//
//   BASE_URL=http://127.0.0.1:5181/ node extraction/measure_sections.mjs > /some/scratch/heights.json
//
// Environment (no machine paths are stored in this repo):
//   BASE_URL           page to measure (default http://127.0.0.1:5181/)
//   PLAYWRIGHT_MODULE  module specifier to import (default "playwright-core"; resolved by Node from the cwd upwards)
//   CHROME_PATH        optional Chromium/Chrome executable; otherwise the module's own bundled browser is used
//   VIEWPORTS          optional comma list WxH (default 1440x900,768x1024,390x844)
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const selectors = JSON.parse(readFileSync(join(here, 'section-selectors.json'), 'utf8')).sections
const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5181/'
const mod = await import(process.env.PLAYWRIGHT_MODULE || 'playwright-core')
const chromium = mod.chromium || mod.default?.chromium
const viewports = (process.env.VIEWPORTS || '1440x900,768x1024,390x844').split(',').map((v) => v.split('x').map(Number))

const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}),
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
})
const out = { measuredAt: new Date().toISOString(), baseUrl: BASE_URL, tool: 'extraction/measure_sections.mjs (headless Chromium)', viewports: {} }
for (const [width, height] of viewports) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 })
  await page.goto(BASE_URL, { waitUntil: 'load', timeout: 60000 })
  await page.evaluate(() => document.fonts.ready)
  await page.waitForTimeout(2500)
  const data = await page.evaluate((sel) => {
    const docTop = (el) => el.getBoundingClientRect().top + window.scrollY
    const res = {}
    for (const [id, s] of Object.entries(sel)) {
      const el = document.querySelector(s.selector)
      if (!el) { res[id] = { found: false }; continue }
      let top = docTop(el)
      let h = el.getBoundingClientRect().height
      if (s.range) {
        const from = document.querySelector(s.range.from)
        top = docTop(from)
        if (s.range.to) h = docTop(document.querySelector(s.range.to)) - top
        else if (s.range.toBottomOf) { const b = document.querySelector(s.range.toBottomOf); h = docTop(b) + b.getBoundingClientRect().height - top }
      }
      res[id] = { found: true, positionKind: s.positionKind, cssPosition: getComputedStyle(el).position, topPx: Math.round(top * 10) / 10, heightPx: Math.round(h * 10) / 10 }
    }
    return { documentHeightPx: document.documentElement.scrollHeight, htmlFontSizePx: parseFloat(getComputedStyle(document.documentElement).fontSize), sections: res }
  }, selectors)
  out.viewports[`${width}x${height}`] = data
  await page.close()
}
await browser.close()
process.stdout.write(JSON.stringify(out, null, 2) + '\n')
