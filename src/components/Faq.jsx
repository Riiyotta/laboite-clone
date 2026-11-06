// CLONE_SPEC_B §7 — FAQ "DES QUESTIONS? ON VOUS RÉPOND" (TemplateFAQ in reference/nuxt/BPFXOrp3.js),
// wrapped in the home's `app-container[HOME-A1] superGrid @columns[12] @gi[16]`.
import { useEffect, useMemo, useRef, useState } from 'react'
import ActionCTA from './header/ActionCTA'
import { useLoaded } from './header/Button'
import { useWhole, useMotion, maskReveal, requestRefresh } from './tagline/sectionMotion'
import { wordsReveal, fadeIn, blurIn } from './review-cards/reveal'
import Dropdown from './faq/Dropdown'
import { QUESTIONS } from './faq/data'
import './tagline/sectionMotion.css'
import './review-cards/reviewCards.css'
import './faq/faq.css'

const STEP = 6
// The live site (and its source: Dropdown keeps its own state and never watches propOpen) lets several
// answers stay open at once; CLONE_SPEC_B §7.2 describes single-open. Flip to true for spec behaviour.
const SINGLE_OPEN = false

export default function Faq() {
  const whole = useWhole()
  const loaded = useLoaded()
  const root = useRef(null)
  const ontitle = useRef(null)
  const title = useRef(null)
  const list = useRef(null)
  const [count, setCount] = useState(STEP)
  const [open, setOpen] = useState(() => new Set())
  const [visible, setVisible] = useState(false)
  const hub = useMemo(() => new Set(), [])
  const more = count < QUESTIONS.length

  const toggle = (i) => setOpen((prev) => {
    const next = SINGLE_OPEN ? new Set() : new Set(prev)
    if (prev.has(i)) next.delete(i)
    else next.add(i)
    return next
  })

  // list visibility (original: iframe intersection sensors) → enables the scroll sag of the strings
  useEffect(() => {
    const io = new IntersectionObserver(([e]) => setVisible(e.isIntersecting))
    io.observe(list.current)
    return () => io.disconnect()
  }, [])

  // section height changes (voir plus / accordion) move every trigger below → refresh
  useEffect(() => { requestRefresh() }, [count])
  const onTransitionEnd = (e) => { if (e.propertyName === 'max-height') requestRefresh() }

  // §7.4 (desktop only)
  useMotion(() => {
    const sec = root.current.querySelector('.faq')
    blurIn(ontitle.current, { trigger: sec, start: '0% 90%', end: '0% 50%' })
    wordsReveal(title.current, { trigger: sec })
    maskReveal(list.current, 200, 90)
    fadeIn(sec.querySelector('.faq__cta'), { trigger: sec, start: '100% 100%', end: '100% 60%' })
  }, whole)

  const emit = (e) => { for (const f of hub) f(e) }

  return (
    <div
      ref={root}
      data-section="faq"
      className="faqWrap superGrid"
      style={{ '--gridColumns': 12, '--gridGapInline': '1.6rem' }}
    >
      <section className="faq home__faq">
        <span ref={ontitle} className="faq__ontitle"> FAQ </span>
        <h2 ref={title} className="faq__title ff-screamer">
          Des questions? <strong>On vous répond</strong>
        </h2>
        <ul
          ref={list}
          className="faq__questions"
          onMouseMove={whole ? emit : undefined}
          onMouseLeave={whole ? () => emit(undefined) : undefined}
          onTransitionEnd={onTransitionEnd}
        >
          {QUESTIONS.map(([q, a], i) => (
            <li key={i} className="contents">
              <Dropdown
                question={q}
                answer={a}
                open={open.has(i)}
                show={i < count}
                onToggle={() => toggle(i)}
                hub={hub}
                visible={visible}
                whole={whole}
                loaded={loaded}
              />
            </li>
          ))}
        </ul>
        <ActionCTA design="darkGlass" className={`faq__cta ${more ? '@show' : '@hide'}`} onClick={() => { if (more) setCount((c) => c + STEP) }}>
          Voir plus de questions
        </ActionCTA>
      </section>
    </div>
  )
}
