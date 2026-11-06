// §5 Works. DOM layer only — triangle fade-out / camera move are driven by the WebGL scene
// (it uses data-section="works" as its trigger).
import { useEffect, useRef } from 'react'
import { store } from '../lib/store'
import WorkCard from './works/WorkCard'
import { useWhole, useMotion, sectionTimeline, wordsRise, gsap, lvh } from './tagline/sectionMotion'
import './tagline/sectionMotion.css'
import './works/works.css'

const U = '/sk/uploads/'
const set = (name, widths) => widths.map(([p, w]) => `${U}${p}${name} ${w}w`).join(', ')
const WORKS = [
  { title: 'Safran Electronics & Defense', tag: 'Corporate', href: '/realisations/Safran-Electronics-Defense-presentation-corporate', img: 'Safran_0239f5157e.jpg', alt: 'Safran.jpg',
    srcset: set('Safran_0239f5157e.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['', 1920]]) },
  { title: 'Adidas', tag: 'Masque', href: '/realisations/adidas-masque-powerpoint', img: 'Adidas_2_20aaceff99.jpg', alt: 'Adidas-2.jpg',
    srcset: set('Adidas_2_20aaceff99.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['big_', 1920], ['', 2566]]) },
  { title: 'Marriott', tag: 'Commerciale', href: '/realisations/marriott-presentation-commerciale-interactive', img: 'Touchscreen_Mariott_la_boite_a_slides_agence_powerpoint_0415bcab60.jpg', alt: 'une personne utilisant la présentation Interactive pour Mariott sur table tactile',
    srcset: set('Touchscreen_Mariott_la_boite_a_slides_agence_powerpoint_0415bcab60.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['', 1920]]) },
  { title: 'LIPTON', tag: 'Évènement', href: '/realisations/lipton-presentation-evenement-selling-story', img: 'Ekaterra_Tea_Lipton_43f10e2e06.jpg', alt: 'Ekaterra-Tea-Lipton.jpg',
    srcset: set('Ekaterra_Tea_Lipton_43f10e2e06.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['', 1080]]) },
  { title: 'Brasseries Kronenbourg', tag: 'Interactions Live', href: '/realisations/brasseries-kronenbourg-presentation-evenementielle-gamification', img: 'Brasseries_kronenbourg_sceno_72f519a001.jpg', alt: "Mise en situation sur scène d'un quiz géant projeté pour une convention Brasseries Kronenbourg",
    srcset: set('Brasseries_kronenbourg_sceno_72f519a001.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['', 1920]]) },
  { title: 'Nissan', tag: 'Marketing', href: '/realisations/nissan-presentation-marketing', img: 'Nissan_ef41272a76.jpg', alt: 'Nissan.jpg',
    srcset: set('Nissan_ef41272a76.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['big_', 1920], ['', 2630]]) },
  { title: 'Viridien', tag: 'Finance', href: '/realisations/viridien-presentation-financiere-resultats-annuels', img: 'Viridien_e87722da36.jpg', alt: 'Photo aérienne pour illustrer le projet Powerpoint Viridien',
    srcset: set('Viridien_e87722da36.jpg', [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000], ['', 1920]]) },
  { title: 'Upciti', tag: 'Masque', href: '/realisations/upciti-masque-powerpoint', img: 'Upciti_82768aec88.jpg', alt: 'Upciti.jpg',
    srcset: set('Upciti_82768aec88.jpg', [['thumbnail_', 1], ['small_', 400], ['medium_', 600], ['large_', 800], ['big_', 1536], ['', 2732]]) },
]

export default function Works() {
  const whole = useWhole()
  const root = useRef(null)
  const title = useRef(null)
  const nav = useRef(null)

  // Header light region (§1.3): the cards grid forces a light header.
  useEffect(() => {
    const el = nav.current
    const regions = store.get().lightRegions
    regions.push(el)
    return () => { const i = regions.indexOf(el); if (i !== -1) regions.splice(i, 1) }
  }, [])

  // §5.2 — timeline WORKS (overflowStart = overflowEnd = lvh) + cards reveal tween.
  useMotion((ctx) => {
    const tl = sectionTimeline(root.current, { overflowStart: lvh, overflowEnd: lvh }, ctx)
    tl.add(title.current, { y: () => -lvh() / 2 }, { y: 0 }, { end: 0.1, overflowStart: 0.7 })
    wordsRise(tl, title.current, { end: 0.2, overflowStart: 0.7, stagger: 0.05 })
    tl.sync()

    gsap.fromTo(nav.current.querySelectorAll('.workCardsPanoramic__link'), { y: '25%', scale: 0.95 }, {
      y: '0%', scale: 1, stagger: 0.1, duration: 0.7,
      scrollTrigger: { trigger: nav.current, start: '0% 100%', toggleActions: 'play none none reverse' },
    })
  }, whole)

  return (
    <section
      ref={root}
      data-section="works"
      className={`works ${whole ? 'is-whole' : ''} superGrid`}
      style={{ '--gridColumns': 12, '--gridGapBlock': '5.6rem', '--gridGapInline': '1.6rem' }}
    >
      <h2 ref={title} className="works__title ff-screamer">
        Un seul outil, des <strong className="text-prm1">possibilités infinies</strong>
      </h2>
      <nav
        ref={nav}
        className="workCardsPanoramic works__works superGrid"
        style={{ '--gridColumns': whole ? 2 : 1, '--gridGapBlock': '.8rem', '--gridGapInline': '.8rem' }}
      >
        <ul style={{ display: 'contents' }}>
          {WORKS.map((w) => (
            <li key={w.href} style={{ display: 'contents' }}>
              <WorkCard data={w} whole={whole} />
            </li>
          ))}
        </ul>
      </nav>
    </section>
  )
}
