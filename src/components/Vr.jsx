// §2 VR sticker (spec B). DOM layer only — the headset, image sphere, darkening plane and the black / white
// background cuts are drawn by the WebGL scene (src/scene/vr.js), which uses data-section="vr" as its trigger.
import { useRef } from 'react'
import { useWhole, useMotion, sectionTimeline, wordsRise, fade, parallax, SplitText, lvh } from './tagline/sectionMotion'
import VrCta from './vr/VrCta'
import './tagline/sectionMotion.css'
import './skills/skills.css' // shared .ui-cta / .btn.hover-left rules
import './vr/vr.css'

// WORDS_FADE_GREY (B6fTRVdz.js `D`): words autoAlpha 0→1, then `:scope>.word` colour lgh1 → gry3
function wordsFadeGrey(tl, el, item, colorItem) {
  if (!el) return
  const split = SplitText.create(el, { type: 'words', wordsClass: 'word' })
  el.classList.add('superPreAccents')
  tl.add(split.words, { autoAlpha: 0 }, { autoAlpha: 1 }, item)
  tl.add(el.querySelectorAll(':scope>.word'), { color: '#ffffff' }, { color: '#5f5f5f' }, colorItem)
}

export default function Vr() {
  const whole = useWhole()
  const root = useRef(null)

  // §2.3 — timeline "VR" (overflowStart = overflowEnd = lvh); all tweens default power1.out
  useMotion((ctx) => {
    const el = root.current
    const tl = sectionTimeline(el, { overflowStart: lvh, overflowEnd: lvh }, ctx)
    const title = el.querySelector('.vr__track-title')
    const content = el.querySelector('.vr__track-content')
    const cta = el.querySelector('.vr__track-cta')
    const a1 = el.querySelector('.vr__A1')
    wordsRise(tl, title, { start: 0, end: 0.17, stagger: 0.013 })
    fade(tl, [...title.querySelectorAll('.line')].reverse(), 'out', { start: 0.17, end: 0.25, stagger: 0.013 })
    tl.add(title, { y: 100 }, { y: -50 }, { start: 0, end: 0.25 })
    wordsFadeGrey(tl, content, { start: 0.63, end: 0.83, stagger: 0.005 }, { start: 0.73, end: 0.85, stagger: 0.005 })
    parallax(tl, cta, 5, { start: 0.7, end: 1 })
    fade(tl, cta, 'in', { start: 0.7, end: 0.85 })
    fade(tl, content, 'out', { start: 0.9, end: 0.99 })
    fade(tl, a1, 'out', { start: 0.91, end: 1 })
    tl.sync()
  }, whole)

  return (
    <section
      ref={root}
      data-section="vr"
      className={`vr ui-sticker ${whole ? 'is-whole' : 'is-fit superDevice'}`}
      style={{ height: whole ? '600lvh' : 'fit-content' }}
    >
      <div className="vr__track ui-sticker__track">
        <h2 className="vr__track-title ff-screamer">
          Dépassez toutes les <strong>limites de PowerPoint</strong>
        </h2>
        <div className="vr__A1">
          <p className="vr__track-content ff-inter">Une expérience aussi bluffante, vous n’êtes pas prêt de l’oublier. Votre public non plus.</p>
          <VrCta href="/expertises/conferences-interactives" title="En savoir plus" className="vr__track-cta" />
        </div>
      </div>
    </section>
  )
}
