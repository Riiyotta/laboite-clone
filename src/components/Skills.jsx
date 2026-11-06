// §7 Skills sticker. DOM layer only — cyan/white background layers and the triangle pinwheel on the
// left half are drawn by the WebGL scene (it uses data-section="skills" as its trigger).
import { useEffect, useRef } from 'react'
import { Arrow } from './method/icons'
import { useWhole, useMotion, sectionTimeline, linesSlide, fade, gsap, lvh } from './tagline/sectionMotion'
import './tagline/sectionMotion.css'
import './skills/skills.css'

const LABELS = [
  { src: '/sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg', alt: 'Certification ISO9001 LABAS' },
  { src: '/sk/uploads/Badge_simple_MOS_LABAS_d0815bc7cf.svg', alt: 'Badge-simple-MOS-LABAS.svg' },
  { src: '/sk/uploads/Logo_simple_Avis_Google_LABAS_d3f7b5bccc.svg', alt: 'Avis Google' },
]
const SKILLS = [
  { title: "0 retard sur +8 000 projets. Nous utilisons la rigueur de l'ISO 9001 pour sécuriser vos calendriers.", labels: LABELS },
  { title: "96% de stabilité de l'enveloppe budgétaire. Notre méthode vise la justesse dès le départ pour respecter votre budget.", labels: LABELS },
  { title: "La preuve ultime d'un rendu maîtrisé ? Un taux de réachat de 85% auprès des directions marketing, qui nous renouvellent leur confiance au cours de l'année.", labels: [], cta: { href: '/realisations', title: 'Voir nos réalisations' } },
]
const STEP = 0.08
const FRAG = 0.92 / SKILLS.length

// UIActionCTA (darkGlass): round arrow button (@hover @left) + pill (@hover @bottom); hovering either
// sets both to hovered.
function Cta({ href, title, className }) {
  const root = useRef(null)
  useEffect(() => {
    const el = root.current
    const btns = el.querySelectorAll('.btn')
    let tweens = []
    let hovered = false
    const kill = () => { tweens.forEach((t) => t.kill()); tweens = [] }
    const set = (on) => {
      if (on === hovered) return
      hovered = on
      kill()
      btns.forEach((b) => {
        b.classList.toggle('@hovered', on)
        tweens.push(on
          ? gsap.fromTo(b, { '--button-hover-y': '0%' }, { '--button-hover-y': '50%', duration: 2.5, ease: 'custom::out' })
          : gsap.to(b, { '--button-hover-y': '100%', duration: 0.4, onComplete: () => gsap.set(b, { '--button-hover-y': '0%' }) }))
      })
    }
    // enter/leave across the two adjacent buttons fire in the same task: evaluate once (Vue watcher batching)
    let count = 0
    const flush = () => queueMicrotask(() => set(count > 0))
    const on = () => { count++; flush() }
    const off = () => { count = Math.max(count - 1, 0); flush() }
    btns.forEach((b) => { b.addEventListener('mouseenter', on); b.addEventListener('mouseleave', off) })
    return () => { kill(); btns.forEach((b) => { b.removeEventListener('mouseenter', on); b.removeEventListener('mouseleave', off) }) }
  }, [])
  return (
    <a ref={root} href={href} className={`ui-cta ${className}`}>
      <span className="btn round hover-left d-darkGlass cta__icon" tabIndex={0}>
        <span className="ui-icon s1" role="presentation" aria-hidden="true"><Arrow /></span>
      </span>
      <span className="btn hover-bottom d-darkGlass ui-cta__button" tabIndex={0}>
        <span className="ui-cta__button-content"><span>{title}</span></span>
      </span>
    </a>
  )
}

export default function Skills() {
  const whole = useWhole()
  const root = useRef(null)

  // §7.2 — timeline SKILLS (overflowStart = overflowEnd = lvh), step .08, frag .92/3.
  useMotion((ctx) => {
    const tl = sectionTimeline(root.current, { overflowStart: lvh, overflowEnd: lvh }, ctx)
    root.current.querySelectorAll('.skills__track-skill').forEach((li, k) => {
      const i = STEP + FRAG * k
      const o = i + 0.2
      const s = i + FRAG - 0.02
      linesSlide(tl, li.querySelector('.skill__title'), 'in', 'x', { start: i, end: o, itemDuration: 0.14, ease: 'power2.out' })
      fade(tl, [...li.querySelectorAll('.skill__labels-label'), li.querySelector('.skills__track-skill__cta')], 'in', { start: i + 0.03, end: o, itemDuration: 0.14, ease: 'power2.in' })
      fade(tl, li, 'out', { start: s - 0.14, end: s, ease: 'power2.in' })
    })
    tl.sync()
  }, whole)

  return (
    <div
      ref={root}
      data-section="skills"
      className={`skills ui-sticker ${whole ? 'is-whole' : 'is-fit superDevice'}`}
      style={{ height: whole ? '540lvh' : 'fit-content' }}
    >
      <div
        className="skills__track ui-sticker__track superGrid"
        style={{ '--gridColumns': 2, '--gridGapBlock': '10.3rem', '--gridGapInline': '1.6rem' }}
      >
        <div className="skills__A1" />
        <ul style={{ display: 'contents' }}>
          {SKILLS.map((sk) => (
            <li key={sk.title} className="skills__track-skill">
              <h3 className="skill__title ff-inter">{sk.title}</h3>
              {sk.labels.length > 0 && (
                <ul className="skill__labels">
                  {sk.labels.map((l) => (
                    <li key={l.src} className="skill__labels-label superGlass glass-lgh" style={{ '--glassBlur': '24px' }}>
                      <span className="ui-icon s6 label__icon" role="presentation" aria-hidden="true">
                        <img src={l.src} alt={l.alt} loading="lazy" />
                      </span>
                    </li>
                  ))}
                </ul>
              )}
              {sk.cta && <Cta href={sk.cta.href} title={sk.cta.title} className="skills__track-skill__cta" />}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
