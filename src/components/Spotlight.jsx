// CLONE_SPEC_B §3 Spotlight — `section._spotlightItem_1bkwk._home__spotlightItem`.
import { useRef } from 'react'
import ActionCTA from './header/ActionCTA'
import { useAutoSizes, srcSet } from './resource-cards/useAutoSizes'
import { useWhole, useMotion, wordsRise, linesSlide, fade, parallax, gsap } from './tagline/sectionMotion'
import { standalone, st, S_WORDS, S_LINES, S_FADE } from './spotlight/standalone'
import './spotlight/spotlight.css'

export default function Spotlight() {
  const whole = useWhole()
  const root = useRef(null)
  const icon = useRef(null)
  const title = useRef(null)
  const content = useRef(null)
  const image = useRef(null)
  useAutoSizes(root)

  // §3.3 — standalone ScrollTrigger tweens, trigger = section, scrub true
  useMotion(() => {
    const trigger = root.current
    wordsRise(standalone, title.current, { stagger: S_WORDS, scrollTrigger: st({ trigger, start: '0% 50%', end: '0% 0%' }) })
    // BLUR in (default ease)
    gsap.fromTo(icon.current, { filter: 'blur(100px)' }, { filter: 'blur(0px)', scrollTrigger: st({ trigger, start: '0% 50%', end: '0% 10%' }) })
    linesSlide(standalone, content.current, 'in', 'y', { stagger: S_LINES, scrollTrigger: st({ trigger, start: '0% 40%', end: '0% 0%' }) })
    fade(standalone, trigger.querySelector('.spot__cta'), 'in', { stagger: S_FADE, scrollTrigger: st({ trigger, start: '0% 30%', end: '0% -10%' }) })
    // PARALLAX_Y 300, ease linear when standalone
    parallax(standalone, image.current, 300, { ease: 'linear', scrollTrigger: st({ trigger, start: '0% 100%', end: '100% 0%' }) })
  }, whole)

  return (
    <section ref={root} data-section="spotlight" className={`spot ${whole ? '' : 'is-column'}`}>
      <div className="spot__A1">
        <span ref={icon} className="spot__icon" role="presentation" aria-hidden="true">
          <svg className="triangleMirror" role="presentation" aria-hidden="true" width="32" height="32" viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M32 16L16 6.99382e-07L16 16L32 16Z" />
            <path d="M16 16L3.49691e-06 16L16 32L16 16Z" />
          </svg>
        </span>
        <h2 ref={title} className="spot__title ff-screamer">
          Toujours carrés. <strong className="text-prm1">Jamais formatés.</strong>
        </h2>
        <p ref={content} className="spot__content ff-inter">
          Une équipe de spécialistes qui réunit sans concession une culture de la réflexion et le goût de l’inattendu. Ça donne la première agence Powerpoint en France.
        </p>
        <ActionCTA design="darkGlass" href="/nous-connaitre" className="spot__cta">Nous connaître</ActionCTA>
      </div>
      <img ref={image} className="spot__image" src="/sk/uploads/large_Labas_20f4ebe642.jpg" srcSet={srcSet('Labas_20f4ebe642.jpg')} sizes="0px" alt="logo la boite à slides" loading="lazy" />
    </section>
  )
}
