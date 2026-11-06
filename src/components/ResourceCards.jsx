// CLONE_SPEC_B §4 Resource cards — `section._resourceCards_1ahqb._home__resourceCards`.
import { useRef } from 'react'
import ActionCTA from './header/ActionCTA'
import WhitePaper from './resource-cards/WhitePaper'
import { useAutoSizes, srcSet } from './resource-cards/useAutoSizes'
import { useWhole, useMotion, wordsRise, fade, gsap } from './tagline/sectionMotion'
import { standalone, st, S_WORDS, S_FADE } from './spotlight/standalone'
import './resource-cards/resource-cards.css'

export default function ResourceCards() {
  const whole = useWhole()
  const root = useRef(null)
  const title = useRef(null)
  const nav = useRef(null)
  useAutoSizes(root)

  // §4.3
  useMotion(() => {
    const trigger = root.current
    wordsRise(standalone, title.current, { stagger: S_WORDS, scrollTrigger: st({ trigger }) })
    fade(standalone, trigger.querySelector('.rcs__header-cta'), 'in', { stagger: S_FADE, scrollTrigger: st({ trigger, start: '0% 50%', end: '0% 20%' }) })
    // CARDS_POP: time-based, plays once on enter, reverses on leave-back
    gsap.fromTo(nav.current.querySelectorAll('.rc'), { y: '25%', scale: 0.95 }, {
      y: '0%', scale: 1, stagger: 0.1, duration: 0.7,
      scrollTrigger: { trigger: nav.current, start: '0 100%', toggleActions: 'play none none reverse' },
    })
  }, whole)

  const tagCls = 'lbsTag rc__category'
  return (
    <section ref={root} data-section="resource-cards" className={`rcs ${whole ? 'is-whole' : ''}`}>
      <header className="rcs__header">
        <h2 ref={title} className="rcs__header-title ff-screamer">
          Nos dernières <strong className="text-prm1">ressources</strong>
        </h2>
        <ActionCTA design="darkGlass" href="/ressources" className="rcs__header-cta">Voir toutes nos ressources</ActionCTA>
      </header>
      <nav
        ref={nav}
        className="rcs__grid superGrid"
        style={{ '--gridColumns': whole ? 3 : 2, '--gridGapBlock': whole ? '1.6rem' : '.8rem', '--gridGapInline': whole ? '1.6rem' : '.8rem' }}
      >
        <ul style={{ display: 'contents' }}>
          <li style={{ display: 'contents' }}>
            <a href="/ressources/gamification-et-powerpoint-mettez-du-jeu-dans-vos-formations" className="rc is-article bg-drk">
              <span className={`${tagCls} @lgh1`}>Article</span>
              <time className="rc__publishedAt" dateTime="2025-01-12T00:00:00.000Z">12/01/2025</time>
              <h3 className="rc__title ff-screamer">Gamification et PowerPoint : mettez du jeu dans vos formations !</h3>
            </a>
          </li>
          <li style={{ display: 'contents' }}>
            <a href="/ressources/ideuzo-presentation-commerciale" className="rc is-client">
              <span className={`${tagCls} @lgh1`}>Cas client</span>
              <time className="rc__publishedAt" dateTime="2026-03-18T00:00:00.000Z">18/03/2026</time>
              <h3 className="rc__title ff-screamer">Ideuzo- Présentation commerciale</h3>
              <img className="rc__image" src="/sk/uploads/large_presentation_equipe_0eebf6541e.jpeg" srcSet={srcSet('presentation_equipe_0eebf6541e.jpeg')} sizes="0px" alt="équipe qui applaudit" loading="lazy" />
            </a>
          </li>
          <li style={{ display: 'contents' }}>
            <a href="/ressources/gagner-en-autonomie-sur-powerpoint" className="rc is-whitePaper">
              <span className={`${tagCls} @drk1`}>Livre blanc</span>
              <time className="rc__publishedAt text-drk1" dateTime="2026-01-27T00:00:00.000Z">27/01/2026</time>
              <WhitePaper className="rc__whitePaper">
                <h3 className="rc__whitePaper-title ff-screamer">Gagner en autonomie sur PowerPoint</h3>
              </WhitePaper>
            </a>
          </li>
        </ul>
      </nav>
    </section>
  )
}
