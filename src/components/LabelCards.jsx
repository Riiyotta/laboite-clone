// CLONE_SPEC_B §5 Label cards sticker — `SECTION._sticker_1b402.@native._labelCards_ya4ut._home__labelCards`.
// DOM layer only: the navy (layer 9) / white (layer 10) background wipes are drawn by the WebGL scene.
import { useEffect, useRef } from 'react'
import Full from './label-cards/Full'
import { store } from '../lib/store'
import { useWhole, useMotion, gsap, SplitText, ScrollTrigger, lvh } from './tagline/sectionMotion'
import { st } from './spotlight/standalone'
import './tagline/sectionMotion.css'
import './label-cards/label-cards.css'

const LABELS = [
  { title: '5 étoiles Google Avis', img: 'Badge_Google_avis_labas_149fc344c9.png', alt: 'illustration du badge 5 étoiles avis google', tag: 'Notation 2026' },
  { title: 'Certifié ISO 9001:2015 Bureau Veritas', img: 'Badge_ISO_9001_labas_49c6d38cef.png', alt: 'illustration du badge certification ISO9001 de la boite à slides', tag: 'Certification 2025' },
  { title: 'Microsoft Office Specialist', img: 'Badge_MOS_labas_83992cf13f.png', alt: 'illustration du badge Microsoft Office Specialist de la boite à slides', tag: 'Depuis 2020' },
]

// Sticker geometry (§5.3): propFragCount 3, propFragHeight 300, propFragGap 100/300 → 500lvh, t = 300/500
const FRAG_H = 300
const FRAG_GAP = 100
const HEIGHT = FRAG_H + FRAG_H * (FRAG_GAP / FRAG_H) * (LABELS.length - 1) // 500 (lvh units)
const T = FRAG_H / HEIGHT // .6
// cubic Bezier control points (x in E units, y in T units)
const P = { a: [0, 0.1], b: [0.5, 0], c: [0.5, 0], d: [1, 0.1] }
const bez = (a, b, c, d, t) => { const u = 1 - t; return u ** 3 * a + 3 * u ** 2 * t * b + 3 * u * t ** 2 * c + t ** 3 * d }
const lerp = (a, b, t) => a + (b - a) * t

export default function LabelCards() {
  const whole = useWhole()
  const root = useRef(null)
  const title = useRef(null)

  // Header light region (CLONE_SPEC_A §1.3): the sticker element forces a light header on desktop.
  useEffect(() => {
    if (!whole) return
    const el = root.current
    const regions = store.get().lightRegions
    regions.push(el)
    return () => { const i = regions.indexOf(el); if (i !== -1) regions.splice(i, 1) }
  }, [whole])

  // §5.3 Title: PARALLAX_Y 50 (ease "ease" → power1.out) + LINES_REVEAL in
  useMotion(() => {
    const trigger = root.current
    const el = title.current
    gsap.fromTo(el, { y: 50 }, { y: -50, ease: 'power1.out', scrollTrigger: st({ trigger, start: '0% 100%', end: '100% 0%' }) })
    const split = SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'line' })
    split.lines.forEach((l) => l.parentElement?.classList.add('superPreAccents'))
    gsap.fromTo(split.lines, { y: '130%', scale: 0.97 }, { y: '0%', scale: 1, stagger: 0.07, scrollTrigger: st({ trigger, start: '0% 0%', end: '0% -100%' }) })
  }, whole)

  // §5.3 Cards: Sticker scroll value → LabelCards.ae(e, .6)
  useEffect(() => {
    const section = root.current
    const cards = [...section.querySelectorAll('.lc')]
    if (!whole) { cards.forEach((c) => { c.style.transform = '' }); return }
    // per-card fixed randoms: rnd (px), cos/sin of i and -i
    const R = cards.map(() => {
      const i = Math.random() * -0.1 - 0.05
      return { rnd: Math.random() * 100 - 50, c0: Math.cos(i), s0: Math.sin(i), c1: Math.cos(-i), s1: Math.sin(-i) }
    })
    const C = { a: [0, 0], b: [0, 0], c: [0, 0], d: [0, 0] }
    const O = [0, 0, 0, 0, 0] // top, end, range, clampMin, clampMax
    const measure = () => {
      const r = section.getBoundingClientRect()
      const top = r.top + window.scrollY
      const L = lvh()
      O[0] = top
      O[2] = Math.max(r.height - L, 0)
      O[1] = top + O[2]
      O[3] = top - L
      O[4] = O[1] + L
    }
    const updateCurve = () => { // eUpdate (Q): E measured with the first card's current transform
      const W = window.innerWidth
      const E = W + (cards[0]?.getBoundingClientRect().width ?? 0)
      const Tt = E * (lvh() / W)
      for (const k of ['a', 'b', 'c', 'd']) { C[k][0] = P[k][0] * E; C[k][1] = P[k][1] * Tt }
    }
    const value = () => O[2] && (gsap.utils.clamp(O[3], O[4], window.scrollY) - O[0]) / O[2]
    const apply = (v) => {
      const e = (v - 0.17) / 0.83
      for (let r = 0; r < cards.length; r++) {
        const a = (e - (FRAG_GAP * r) / HEIGHT) / T
        const x = -bez(C.a[0], C.b[0], C.c[0], C.d[0], a)
        const y = bez(C.a[1], C.b[1], C.c[1], C.d[1], a) + R[r].rnd
        const c = lerp(R[r].c0, R[r].c1, a)
        const s = lerp(R[r].s0, R[r].s1, a)
        cards[r].style.transform = `matrix3d(${c}, ${-s}, 0, 0, ${s}, ${c}, 0, 0, 0, 0, 1, 0, ${x}, ${y}, 0, 1)`
      }
    }
    const onScroll = () => apply(value())
    const onLoad = () => { measure(); updateCurve(); onScroll() } // LOAD / EARTHQUAKE
    onLoad()
    const onRefresh = () => { measure(); onScroll() }
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('load', onLoad)
    window.addEventListener('resize', onLoad)
    ScrollTrigger.addEventListener('refresh', onRefresh)
    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('load', onLoad)
      window.removeEventListener('resize', onLoad)
      ScrollTrigger.removeEventListener('refresh', onRefresh)
      cards.forEach((c) => { c.style.transform = '' })
    }
  }, [whole])

  return (
    <section
      ref={root}
      data-section="label-cards"
      className={`lcs ui-sticker ${whole ? 'is-whole' : 'is-fit'}`}
      style={{ height: whole ? `${HEIGHT}lvh` : 'fit-content' }}
    >
      <Full className="lcs__track ui-sticker__track">
        <h2 ref={title} className="lcs__title ff-screamer">
          Engagés pour <strong className="text-prm1">la qualité</strong>
        </h2>
        <ul
          className={whole ? 'lcs__list' : 'lcs__list superGrid'}
          style={whole ? { display: 'contents' } : { '--gridColumns': 2, '--gridMargin': '2rem', '--gridGapBlock': '1.6rem', '--gridGapInline': '1.6rem' }}
        >
          {LABELS.map((l) => (
            <li key={l.img} style={{ display: 'contents' }}>
              <section className="lc superGlass glass-lgh" style={{ '--glassBlur': '90px' }}>
                <h3 className="lc__title ff-screamer">{l.title}</h3>
                <img className="lc__image" src={`/sk/uploads/${l.img}`} srcSet={`/sk/uploads/thumbnail_${l.img} 1w`} sizes="0px" alt={l.alt} loading="lazy" />
                <div className="lc__A1">
                  <span className="lbsTag @lgh1">{l.tag}</span>
                </div>
              </section>
            </li>
          ))}
        </ul>
      </Full>
    </section>
  )
}
