#!/usr/bin/env node
// Computed-style histogram of the served clone at 1440x900 (optional evidence tool; its recorded
// output lives in measured-values.json -> styleHistogram1440). Text-free: counts values only.
//   BASE_URL=http://127.0.0.1:5181/ node extraction/style_histogram.mjs
// Env: BASE_URL, PLAYWRIGHT_MODULE (default "playwright-core"), CHROME_PATH (optional).
const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:5181/'
const mod = await import(process.env.PLAYWRIGHT_MODULE || 'playwright-core')
const chromium = mod.chromium || mod.default?.chromium
const browser = await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 })
await page.goto(BASE_URL, { waitUntil: 'load', timeout: 60000 })
await page.evaluate(() => document.fonts.ready)
await page.waitForTimeout(2000)
const hist = await page.evaluate(() => {
  const H = {}
  const add = (k, v) => { if (!v || v === 'none' || v === 'normal' && k !== 'lineHeight') return; (H[k] ||= {})[v] = (H[k][v] || 0) + 1 }
  for (const el of document.querySelectorAll('body *')) {
    if (el.closest('svg') && el.tagName !== 'svg') continue
    const cs = getComputedStyle(el)
    const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())
    if (hasText) {
      add('color', cs.color)
      add('fontFamily', cs.fontFamily.split(',')[0].replace(/"/g, '').trim())
      add('fontSize', cs.fontSize)
      add('fontWeight', cs.fontWeight)
      add('lineHeight', cs.lineHeight)
      add('letterSpacing', cs.letterSpacing)
      add('textTransform', cs.textTransform)
    }
    if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') add('backgroundColor', cs.backgroundColor)
    if (cs.borderTopLeftRadius !== '0px') add('borderRadius', cs.borderTopLeftRadius)
    if (cs.backdropFilter && cs.backdropFilter !== 'none') add('backdropFilter', cs.backdropFilter)
  }
  const sort = (o) => Object.fromEntries(Object.entries(o).sort((a, b) => b[1] - a[1]))
  return Object.fromEntries(Object.entries(H).map(([k, v]) => [k, sort(v)]))
})
await browser.close()
process.stdout.write(JSON.stringify({ measuredAt: new Date().toISOString(), viewport: '1440x900', baseUrl: BASE_URL, histogram: hist }, null, 2) + '\n')
