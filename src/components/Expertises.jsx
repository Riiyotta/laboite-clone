// CLONE_SPEC_B §1 Expertises — `section._expertises_jvwcv.@whole`.
// DOM layer only (white background comes from the WebGL shader).
import { useEffect, useRef } from 'react'
import Full from './label-cards/Full'
import { useAutoSizes, srcSet } from './resource-cards/useAutoSizes'
import { useWhole, useMotion, gsap, lvh } from './tagline/sectionMotion'
import './expertises/expertises.css'

const ROUTES = [
  { label: 'Présentations', href: '/expertises/presentations-powerpoint', img: 'Presentation_e945d6b799.png', alt: 'Presentation.png' },
  { label: 'Communication 360', href: '/expertises/communication-360', img: 'Communication_360_7a5ef30bda.png', alt: 'Communication-360.png' },
  { label: 'Navigation App Like', href: '/expertises/navigation-interactive-powerpoint', img: 'FDH_URW_navigation_interactive_87d42a0822.jpg', alt: 'Un homme cliquant sur la présentation interaction du Forum des halles sur un ipad' },
  { label: 'Séminaire VR', href: '/expertises/seminaire-realite-virtuelle', img: 'Immersion_VR_e950803a61.png', alt: 'Immersion-VR.png' },
  { label: 'Solutions IA', href: '/expertises/solutions-ia-powerpoint', img: 'Assistance_IA_LABAS_bot_1963bf7998.jpg', alt: 'Bot Assistance IA La boite à slides' },
]

export default function Expertises() {
  const whole = useWhole()
  const root = useRef(null)
  const nav = useRef(null)
  useAutoSizes(root)

  // §1.3 — per-image random hover values, set once on mount
  useEffect(() => {
    root.current.querySelectorAll('.exp__image').forEach((n) => {
      n.style.setProperty('--vx', `${(Math.random() - 0.5) * 50}px`)
      n.style.setProperty('--vy', `${(Math.random() - 0.5) * 30}px`)
      n.style.setProperty('--r', `${(Math.random() - 0.5) * Math.PI * 0.07}rad`)
    })
  }, [])

  // §1.4 — labels rise 17lvh → 0, stagger .3, scrub .5, trigger router "0% 83%" → "100% 83%"
  useMotion(() => {
    const labels = nav.current.querySelectorAll('.exp__label')
    gsap.fromTo(labels, { y: () => lvh() * 0.17 }, {
      y: 0, stagger: 0.3,
      scrollTrigger: { trigger: nav.current, start: '0% 83%', end: '100% 83%', scrub: 0.5 },
    })
  }, whole)

  return (
    <section ref={root} data-section="expertises" className={`exp ${whole ? 'is-whole' : ''}`}>
      <h2 className="exp__title ff-inter">Nos expertises</h2>
      <Full>
        <nav ref={nav} className="exp__router">
          <ul style={{ display: 'contents' }}>
            {ROUTES.map((r) => (
              <li key={r.href} style={{ display: 'contents' }}>
                <a href={r.href} className="exp__route">
                  <span className="exp__label ff-screamer">{r.label}</span>
                  <img className="exp__image" src={`/sk/uploads/large_${r.img}`} srcSet={srcSet(r.img)} sizes="0px" alt={r.alt} loading="lazy" />
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </Full>
    </section>
  )
}
