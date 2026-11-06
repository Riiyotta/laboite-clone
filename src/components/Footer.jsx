// CLONE_SPEC_B §8 — footer#FOOTER (layouts Footer in reference/nuxt/BJwg4-9U.js). DOM layer only:
// the purple "final" background layer and the glass-triangle conveyor are WebGL (scene agent); this
// component keeps id="FOOTER" / data-section="footer" for their triggers.
import { useEffect, useRef, useState } from 'react'
import ActionCTA from './header/ActionCTA'
import { Logo, LinkedIn, Vimeo, Icon } from './header/icons'
import { store } from '../lib/store'
import { useWhole, useMotion } from './tagline/sectionMotion'
import { wordsReveal, fadeIn } from './review-cards/reveal'
import { useGlower } from './footer/useGlower'
import './review-cards/reviewCards.css'
import './footer/footer.css'

const EXPLORE = [
  ['Réalisations', '/realisations'],
  ['Nous connaître', '/nous-connaitre'],
  ['Notre méthode', '/la-methode-labas'],
  ['Ressources', '/ressources'],
  ['Contact', '/contact'],
  ["Offres d'emploi", '/nos-offres-d-emploi'],
]
const EXPERTISES = [
  ['Communication 360', '/expertises/communication-360'],
  ['Navigation App Like', '/expertises/navigation-interactive-powerpoint'],
  ['Animatiques', '/expertises/Animatiques-powerpoint'],
  ['Conférences Interactives', '/expertises/conferences-interactives'],
  ['Séminaire VR', '/expertises/seminaire-realite-virtuelle'],
  ['Solutions IA', '/expertises/solutions-ia-powerpoint'],
  ['Formations & Coaching', '/expertises/formations-powerpoint-coaching-labas-agence-powerpoint'],
]
const P = '/expertises/presentations-powerpoint/'
const PRESENTATIONS = [
  ['Présentation', 'commerciale', `${P}presentation-commerciale`],
  ['Présentation', 'corporate', `${P}presentation-corporate`],
  ['Présentation', 'événementielle', `${P}presentation-evenementielle-labas-agence-powerpoint`],
  ['Présentation', 'appel d’offre', `${P}presentation-appel-offre`],
  ['Présentation', 'ressources humaines', `${P}presentation-ressources-humaines`],
  ['Masque', 'PPT', `${P}masque-ppt-labas-agence-powerpoint`],
  ['Présentation', 'marketing', `${P}presentation-marketing`],
  ['Présentation', 'financière', `${P}presentation-financiere`],
]
const LABELS = [
  { src: '/sk/uploads/Logo_simple_certification_ISO_LABAS_1a3bc958ae.svg', alt: 'Certification ISO9001 LABAS', title: 'Certifié ISO 9001:2015 Bureau Veritas' },
  { src: '/sk/uploads/Badge_simple_MOS_LABAS_d0815bc7cf.svg', alt: 'Badge-simple-MOS-LABAS.svg', title: 'Microsoft Office Specialist' },
  { src: '/sk/uploads/Logo_simple_Avis_Google_LABAS_f10bfef852.svg', alt: 'Avis Google LABAS', title: '5 étoiles Google Avis' },
]
const LEGALS = [
  ['Mentions légales', '/mentions-legales'],
  ['Politique de confidentialité', '/politique-de-confidentialite'],
  ['Cookies', '#'],
]
const BUBBLE_ARROW = 'M7.27611 7.04478C6.87592 7.53733 6.12408 7.53733 5.72389 7.04478L-2.54292e-07 -1.82822e-07L13 9.53674e-07L7.27611 7.04478Z'
const INFO = 'M8.33477 1.01079C4.37774 0.922906 1.0983 4.05981 1.01042 8.01688C0.922533 11.9739 4.05947 15.2534 8.01651 15.3412C11.9736 15.4291 15.253 12.2922 15.3409 8.33515C15.4287 4.37808 12.2918 1.09867 8.33477 1.01079ZM8.53816 6.85073C8.90615 6.8589 9.19819 7.16344 9.1902 7.53139C9.18203 7.89948 8.87665 8.19157 8.50857 8.18341L8.44196 11.1827C8.43378 11.5507 8.12925 11.8427 7.76129 11.8347C7.3932 11.8265 7.1011 11.5212 7.10928 11.1531L7.175 8.19384C7.17825 8.0448 7.18232 7.87816 7.20272 7.73731C7.22629 7.57491 7.28388 7.34775 7.46968 7.15227C7.66407 6.94793 7.89746 6.88319 8.07493 6.86095C8.21616 6.84327 8.37883 6.84708 8.51083 6.85012C8.51994 6.85033 8.52937 6.85053 8.53816 6.85073ZM8.24965 4.84383C8.61764 4.852 8.90968 5.15654 8.90169 5.52449C8.89351 5.89259 8.58815 6.18468 8.22005 6.17651C7.85195 6.16833 7.55986 5.86297 7.56803 5.49487C7.57638 5.12692 7.88166 4.83565 8.24965 4.84383Z'

function Nav({ className, title, children }) {
  return (
    <nav className={`router footerNav ${className}`}>
      <div className="footerNav__title">{title}</div>
      {children}
    </nav>
  )
}

function Route({ href, className, children }) {
  return (
    <li className="contents">
      <a href={href} className={`footerNav__route ${className}`}>
        <span className="footerNav__route-title">{children}</span>
      </a>
    </li>
  )
}

export default function Footer() {
  const whole = useWhole()
  const root = useRef(null)
  const title = useRef(null)
  const panel = useRef(null)
  const [target, setTarget] = useState(-1)

  // Header light region — the original only broadcasts it on mobile (react: e => isMobile); on desktop the
  // header reads the purple "final" background layer instead.
  useEffect(() => {
    if (whole) return
    const el = root.current
    const regions = store.get().lightRegions
    regions.push(el)
    return () => { const i = regions.indexOf(el); if (i !== -1) regions.splice(i, 1) }
  }, [whole])

  // §8.4 (desktop only): title WORDS_REVEAL (0% 70% → 0% 10%), CTA FADE (0% 40% → 0% 0%)
  useMotion(() => {
    wordsReveal(title.current, { trigger: root.current, start: '0% 70%', end: '0% 10%' })
    fadeIn(root.current.querySelector('.footer__cta'), { trigger: root.current, start: '0% 40%', end: '0% 0%' })
  }, whole)
  // §8.2 @glow (desktop only, set up with the "whole" reactor)
  useGlower(panel, whole)

  const enterLabel = (i) => setTarget(i)
  const leaveLabel = (i) => setTarget((t) => (t === i ? -1 : t))

  return (
    <footer ref={root} id="FOOTER" data-section="footer" className="superDevice">
      <div ref={title} className="footer__title ff-screamer">
        Prêt à transformer votre <strong>impact?</strong>
      </div>
      <ActionCTA design="light" href="/contact" className="footer__cta">Contactez-nous</ActionCTA>

      <div
        ref={panel}
        className="footer__A1 superGrid"
        style={{ '--gridColumns': 12, '--gridMargin': '4.8rem', '--gridGapInline': '1.6rem' }}
      >
        <div className="footer__B1">
          <div className="footer__C1">
            <a className="footer__logo" href="/"><Logo className="footer__logo-svg" /></a>
            <ul className="langSwitcher">
              <li className="contents"><button type="button" className="langSwitcher__option @current">fr</button></li>
              <li className="contents"><button type="button" className="langSwitcher__option">en</button></li>
            </ul>
            <address className="footer__address">Paris, Bordeaux, Verdun, Aix-en-Provence, Rennes, Strasbourg</address>
          </div>
          <Nav className="footer__explore" title="Explorer">
            <ul className="contents">
              {EXPLORE.map(([t, h]) => <Route key={h} href={h} className="footerNav__route--explore">{t}</Route>)}
            </ul>
          </Nav>
          <div className="footer__C2">
            <Nav className="footer__expertises" title="Expertises">
              <ul className="footer__expertises-list">
                {EXPERTISES.map(([t, h]) => <Route key={h} href={h} className="footerNav__route--expertise">{t}</Route>)}
              </ul>
            </Nav>
            <Nav className="footer__expertises" title="Présentations">
              <ul className="footer__expertises-list">
                {PRESENTATIONS.map(([s, t, h]) => (
                  <Route key={h} href={h} className="footerNav__route--expertise"><strong>{s}</strong> {t}</Route>
                ))}
              </ul>
            </Nav>
          </div>
        </div>

        <ul className={`footer__labels ${target !== -1 ? '@highlight' : ''}`}>
          {LABELS.map((l, i) => (
            <li key={l.src} className="contents">
              <div
                className={`tooltip footer__labels-label ${target === i ? '@target' : ''}`}
                onMouseEnter={() => enterLabel(i)}
                onMouseLeave={() => leaveLabel(i)}
              >
                <div
                  className="tooltip__slot label__slot"
                  tabIndex={0}
                  aria-describedby={`BUBBLE_FOOTER_${i}`}
                  onFocus={() => enterLabel(i)}
                  onBlur={() => leaveLabel(i)}
                >
                  <img className="label__icon" src={l.src} alt={l.alt} loading="lazy" />
                </div>
                <div id={`BUBBLE_FOOTER_${i}`} className="tooltip__bubble" role="tooltip">
                  <div className="tooltip__bubble-title superGlass glass-lgh">{l.title}</div>
                  <svg className="tooltip__bubble-arrow" role="presentation" width="13" height="8" viewBox="0 0 13 8" xmlns="http://www.w3.org/2000/svg">
                    <path d={BUBBLE_ARROW} />
                  </svg>
                </div>
              </div>
            </li>
          ))}
        </ul>

        <div className="footer__B2">
          <small className="copyright"> ©{new Date().getFullYear()} </small>
          <button
            type="button"
            className="seoModalTrigger"
            onClick={() => window.dispatchEvent(new CustomEvent('lbs:seo-modal'))}
          >
            <Icon size={1}>
              <svg className="info" role="presentation" aria-hidden="true" viewBox="0 0 17 17" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d={INFO} /></svg>
            </Icon>
          </button>
        </div>

        <div className="footer__B3">
          <nav className="router socials footer__socials">
            <ul className="contents">
              <li className="contents">
                <a className="footer__social" target="_blank" rel="noreferrer" href="https://www.linkedin.com/company/laboiteaslides/">
                  <Icon size={3} role="img" aria-label="linkedin"><LinkedIn /></Icon>
                </a>
              </li>
              <li className="contents">
                <a className="footer__social" target="_blank" rel="noreferrer" href="https://vimeo.com/laboiteaslides?fl=pp&fe=sh">
                  <Icon size={3} role="img" aria-label="vimeo"><Vimeo /></Icon>
                </a>
              </li>
            </ul>
          </nav>
          <nav className="router footer__legals">
            <ul className="contents">
              {LEGALS.map(([t, h]) => (
                <li key={t} className="contents"><a href={h} className="footer__legal">{t}</a></li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </footer>
  )
}
