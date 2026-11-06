// CLONE_SPEC_B §6 — Review cards "ILS NOUS FONT CONFIANCE" (TemplateReviewCards + Swiper + CollectionReviewCard).
import { useRef } from 'react'
import Button, { useLoaded } from './header/Button'
import { Arrow, Icon } from './header/icons'
import { useWhole, useMotion } from './tagline/sectionMotion'
import { wordsReveal, cardsPop } from './review-cards/reveal'
import { useSwiper } from './review-cards/useSwiper'
import { REVIEWS } from './review-cards/data'
import './review-cards/reviewCards.css'

const SLIDE = '.reviewCards__track-reviewCard'

function ReviewCard({ data }) {
  return (
    <article id={data.id} className="reviewCard reviewCards__track-reviewCard superGlass glass-drk">
      <header className="reviewCard__header">
        <img className="reviewCard__header-image" src={data.src} alt={data.alt} loading="lazy" />
        <h3 className="reviewCard__header-title">{data.title}</h3>
        {data.role ? <p className="reviewCard__header-role">{data.role}</p> : null}
      </header>
      <p className="reviewCard__content">{data.content}</p>
    </article>
  )
}

export default function ReviewCards() {
  const whole = useWhole()
  const loaded = useLoaded()
  const root = useRef(null)
  const title = useRef(null)
  const track = useRef(null)
  const { navClass, go } = useSwiper(track, SLIDE, loaded)

  // §6.4 (desktop only): title WORDS_REVEAL (trigger section, 0% 90% → 0% 30%); cards CARDS_POP (trigger track, 0% 100%)
  useMotion(() => {
    wordsReveal(title.current, { trigger: root.current })
    cardsPop(track.current.querySelectorAll(SLIDE), { trigger: track.current, start: '0% 100%' })
  }, whole)

  return (
    <section
      ref={root}
      data-section="review-cards"
      className={`reviewCards home__reviewCards ${whole ? '' : 'superDevice'}`}
    >
      <h2 ref={title} className="reviewCards__title ff-screamer">
        Ils nous font <strong>confiance</strong>
      </h2>
      <nav className={`swiper__nav reviewCards__nav ${navClass}`}>
        <Button round design="darkGlass" hover="right" className="swiper__nav-stepper @prev" onClick={() => go(false)}>
          <Icon size={1}><Arrow className="arrow arrow--r180" /></Icon>
        </Button>
        <Button round design="darkGlass" hover="left" className="swiper__nav-stepper @next" onClick={() => go(true)}>
          <Icon size={1}><Arrow className="arrow" /></Icon>
        </Button>
      </nav>
      <div ref={track} className="swiper__track reviewCards__track">
        <ul className="contents">
          {REVIEWS.map((r) => (
            <li key={r.id} className="contents"><ReviewCard data={r} /></li>
          ))}
        </ul>
      </div>
    </section>
  )
}
