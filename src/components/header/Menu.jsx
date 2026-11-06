// section._menu (spec §1.5). Content/links copied from reference/original.html.
import { useLayoutEffect, useRef } from 'react'
import { gsap, lvh } from '../../lib/motion'
import ActionCTA from './ActionCTA'
import { Icon, LinkedIn, Vimeo } from './icons'

const EXPLORE = [
  ['Réalisations', '/realisations'],
  ['Nous connaître', '/nous-connaitre'],
  ['Notre méthode', '/la-methode-labas'],
  ['Ressources', '/ressources'],
  ['Contact', '/contact'],
  ["Offres d'emploi", '/nos-offres-d-emploi'],
]
const EXPERTISES = [
  ['Présentations', '/expertises/presentations-powerpoint'],
  ['Communication 360', '/expertises/communication-360'],
  ['Navigation App Like', '/expertises/navigation-interactive-powerpoint'],
  ['Animatiques', '/expertises/Animatiques-powerpoint'],
  ['Conférences Interactives', '/expertises/conferences-interactives'],
  ['Séminaire VR', '/expertises/seminaire-realite-virtuelle'],
  ['Solutions IA', '/expertises/solutions-ia-powerpoint'],
  ['Formations & Coaching', '/expertises/formations-powerpoint-coaching-labas-agence-powerpoint'],
]

// 3D swing data (normals interleaved [y0,z0,y1,z1,...]; y × lvh, z × 1000) — verbatim from the shipped Menu.
const PANEL = { cos: Math.cos(-0.15), sin: Math.sin(-0.15), normals: [-1.5, 0, -1.7, -1, 0.1, 0.1, 0, 0], points: new Float32Array(8) }
const WIDGET = { cos: Math.cos(0.1), sin: Math.sin(0.1), normals: [1, 0, 0, 0, 0, 0.1, 0, 0], points: new Float32Array(8) }
const computePoints = ({ normals, points }) => {
  for (let n = 0; n < 8; n += 2) { points[n] = normals[n] * lvh(); points[n + 1] = normals[n + 1] * 1e3 }
}
const lerp = (a, b, t) => a + (b - a) * t
const bez = (a, b, c, d, t) => { const u = 1 - t; return u ** 3 * a + 3 * u ** 2 * t * b + 3 * u * t ** 2 * c + t ** 3 * d }
const swing = (el, { cos, sin, points: r }, { progress: i }) => {
  const a = lerp(cos, 1, i)
  const o = lerp(sin, 0, i)
  el.style.transform = `matrix3d(1, 0, 0, 0, 0, ${a}, ${-o}, 0, 0, ${o}, ${a}, 0, 0, ${bez(r[0], r[2], r[4], r[6], i)}, ${bez(r[1], r[3], r[5], r[7], i)}, 1)`
}

export default function Menu({ show, loaded, mobile, crushed, onClose }) {
  const ref = useRef(null)
  const api = useRef({})
  const whole = !mobile

  // Build timelines (desktop: W/G/K, mobile: U). Rebuilt when the format changes.
  useLayoutEffect(() => {
    const menu = ref.current
    if (!menu) return
    const A = api.current
    let cleanupInline = () => {}
    const ctx = gsap.context(() => {
      if (!whole) {
        A.U = gsap.fromTo(menu, { y: '-100%', scale: 0.95 }, { paused: true, y: '0%', scale: 1, duration: 0.5, ease: 'power2.out' })
        if (A.show) A.U.progress(1)
        return
      }
      computePoints(PANEL); computePoints(WIDGET)
      const q = (s) => menu.querySelector(s)
      const qa = (s) => menu.querySelectorAll(s)
      const panel = q('.menu__background-panel')
      const lang = q('.menu__langSwitcher')
      const widgets = qa('.menu__widgets-widget')
      const titles = qa('.menu__explore-title, .menu__expertises-title')
      const explore = qa('.menu__explore-route')
      const expertise = qa('.menu__expertises-route')
      const address = q('.menu__address')
      const sep = q('.menu__separator')
      const socials = qa('.menu__socials-social')
      const d = { progress: 0 }
      const f = widgets.length
      const p = Array.from({ length: f }, () => ({ progress: 0 }))
      const m = p.map((pp, i) => () => swing(widgets[i], WIDGET, pp))
      const h = () => swing(panel, PANEL, d)
      const reset = () => {
        d.progress = 0; h()
        gsap.set(menu, { y: '0%', scale: 1 })
        gsap.set(lang, { scale: 1.07, autoAlpha: 0 })
        gsap.set(titles, { autoAlpha: 0 })
        gsap.set(explore, { y: '130%', scale: 1.05 })
        gsap.set(expertise, { x: 15, scale: 1.05, autoAlpha: 0 })
        gsap.set(address, { x: -10, y: -10, scale: 0.95, autoAlpha: 0 })
        gsap.set(sep, { x: -20, scaleX: 0, autoAlpha: 0 })
        gsap.set(socials, { x: -10, y: -10, scale: 0.95, autoAlpha: 0 })
        A.G?.pause()
        for (let e = 0; e < f; e++) { p[e].progress = 0; m[e]() }
      }
      reset()
      A.W = gsap.timeline({ paused: true })
        .to(d, { progress: 1, duration: 2, ease: 'custom::out', onUpdate: h }, 0)
        .to(lang, { scale: 1, autoAlpha: 1, duration: 1.7, ease: 'custom::out' }, 0.35)
        .to(titles, { autoAlpha: 0.5, duration: 2, ease: 'custom::out' }, 0.15)
        .to(explore, { y: '0%', scale: 1, duration: 2.7, stagger: 0.09, ease: 'custom::out' }, '<+=.07')
        .to(expertise, { x: 0, scale: 1, autoAlpha: 1, duration: 2.7, stagger: 0.09, ease: 'custom::out' }, '<')
        .to(address, { x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 2.3, ease: 'custom::out' }, 0.3)
        .to(sep, { x: 0, scaleX: 1, autoAlpha: 1, duration: 2.3, ease: 'custom::out' }, 0.35)
        .to(socials, { x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 2, stagger: 0.05, ease: 'custom::out' }, 0.4)
      A.G = gsap.timeline({ paused: true, delay: 0.1 })
      for (let e = 0; e < f; e++) A.G.to(p[e], { progress: 1, duration: 2.9, ease: 'custom::out', onUpdate: m[e] }, 0.2 * e)
      A.K = gsap.fromTo(menu, { y: '0%', scale: 1 }, { paused: true, y: '-100%', scale: 0.95, duration: 0.5, ease: 'power2.out', onComplete: reset })
      A.reset = reset
      A.resize = () => { computePoints(PANEL); computePoints(WIDGET); if (!A.show) reset() }
      cleanupInline = () => { panel.style.transform = ''; widgets.forEach((w) => { w.style.transform = '' }) }
      if (A.show) { A.W.progress(1); A.G.progress(1) }
    }, menu)
    const onResize = () => A.resize?.()
    window.addEventListener('resize', onResize)
    return () => {
      window.removeEventListener('resize', onResize)
      ctx.revert(); cleanupInline()
      A.U = A.W = A.G = A.K = A.reset = A.resize = null
    }
  }, [whole])

  // show / hide
  const firstShow = useRef(true)
  useLayoutEffect(() => {
    const A = api.current
    const prev = A.show
    A.show = show
    if (firstShow.current) { firstShow.current = false; if (!show) return }
    if (prev === show) return
    if (whole) {
      if (!A.W) return
      if (show) {
        if (A.K.progress() !== 1) { A.K.pause(); A.K.reverse() }
        A.W.invalidate(); A.W.restart()
        A.G.invalidate(); A.G.restart()
      } else {
        A.W.pause(); A.K.restart()
      }
    } else if (A.U) {
      if (show) A.U.restart()
      else { A.U.pause(); A.U.reverse() }
    }
  }, [show, whole])

  const cls = ['menu', loaded ? '@loaded' : '', show ? '@show' : '', crushed ? '@crushed' : '', mobile ? '@mobile' : ''].filter(Boolean).join(' ')
  return (
    <section className={cls} ref={ref}>
      <div className="menu__background" role="presentation" aria-hidden="true">
        <div className="menu__background-panel" />
      </div>
      <div className="menu__A1 superGrid">
        <ul className="langSwitcher @dark menu__langSwitcher">
          <li className="lbsContents"><button className="langSwitcher__option @current superFont" type="button">fr</button></li>
          <li className="lbsContents"><button className="langSwitcher__option superFont" type="button">en</button></li>
        </ul>
        <ul className="menu__widgets superGrid">
          <li className="lbsContents">
            <a href="/expertises/conferences-interactives" className="menu__widgets-widget @expertise" onClick={onClose}>
              <section className="expertiseWidget">
                <div className="expertiseWidget__title">Conférences Interactives</div>
                <ActionCTA design="lightGlass" onClick={onClose}>Découvrir</ActionCTA>
                <img className="expertiseWidget__image" src="/sk/uploads/large_Presentation_augmentee_1d02882a38.jpg" alt="Presentation-augmentee.jpg" loading="lazy" />
              </section>
            </a>
          </li>
          <li className="lbsContents">
            <a href="/ressources/4-conseils-pour-capter-lattention-en-1-minute" className="menu__widgets-widget @resource" onClick={onClose}>
              <section className="resourceWidget @whitePaper">
                <div className="lbsTag @drk1">Livre blanc</div>
                <div className="whitePaper resourceWidget__whitePaper">
                  <div className="whitePaper__A1">
                    <div className="whitePaper__B1">
                      <span className="whitePaper__title">4 conseils pour capter l’attention en 1 minute</span>
                    </div>
                  </div>
                </div>
              </section>
            </a>
          </li>
          <li className="lbsContents">
            <a href="/ressources/arcitek-presentation-corporate" className="menu__widgets-widget @resource" onClick={onClose}>
              <section className="resourceWidget @client">
                <div className="lbsTag @lgh1">Cas client</div>
                <span className="resourceWidget__title">Arcitek - Présentation corporate</span>
                <img className="resourceWidget__image" src="/sk/uploads/large_Adobe_Stock_206118370_5ab61dcb89.jpg" alt="AdobeStock_206118370.jpg" loading="lazy" />
              </section>
            </a>
          </li>
        </ul>
        <div className="menu__B1">
          <nav className="lbsNav menu__explore">
            <div className="lbsNav__title menu__explore-title">Explorer</div>
            {EXPLORE.map(([t, href]) => (
              <div className="menu__explore-item" key={href}>
                <a href={href} className="lbsNav__route menu__explore-route" onClick={onClose}>
                  <span className="lbsNav__route-title">{t}</span>
                </a>
              </div>
            ))}
          </nav>
          <div className="menu__C1">
            <address className="menu__address">Paris, Bordeaux, Verdun, Aix-en-Provence, Rennes, Strasbourg</address>
            <hr className="menu__separator" />
            <nav className="menu__socials">
              <a className="menu__socials-social" target="_blank" rel="noreferrer" href="https://www.linkedin.com/company/laboiteaslides/">
                <Icon size={2} role="img" aria-hidden={undefined} aria-label="linkedin"><LinkedIn /></Icon>
              </a>
              <a className="menu__socials-social" target="_blank" rel="noreferrer" href="https://vimeo.com/laboiteaslides?fl=pp&fe=sh">
                <Icon size={2} role="img" aria-hidden={undefined} aria-label="vimeo"><Vimeo /></Icon>
              </a>
            </nav>
          </div>
        </div>
        <nav className="lbsNav menu__expertises">
          <div className="lbsNav__title menu__expertises-title">Expertises</div>
          {EXPERTISES.map(([t, href]) => (
            <a key={href} href={href} className="lbsNav__route menu__expertises-route" onClick={onClose}>
              <span className="lbsNav__route-title">{t}</span>
            </a>
          ))}
        </nav>
      </div>
    </section>
  )
}
