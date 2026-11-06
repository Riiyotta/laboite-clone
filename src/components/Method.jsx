// §6 Method — marquee + tagline + content/metrics. No 3D content (white background from the scene).
import { useRef } from 'react'
import Marquee from './method/Marquee'
import { TriangleMirror, CheckmarkBadge } from './method/icons'
import { useWhole, useMotion, sectionTimeline, linesSlide, parallax, charsIn, maskReveal, lvh } from './tagline/sectionMotion'
import './tagline/sectionMotion.css'
import './method/method.css'

const MARQUEE = 'Depuis 2002 ● ISO 9001 ● 5/5 Note Google Avis ● +8 000 projets ● 85% de réachat ● MOS PowerPoint'
const TAGLINE = 'Tirer parti des dernières avancées technologiques et intelligences artificielles pour valoriser vos messages les plus importants'
const CONTENT = "À la boite à slides, on maximise l'engagement de votre public depuis 2002. On repousse les limites de PowerPoint pour vous faire gagner en impact, en performance et en autonomie. Pour votre plus grande satisfaction."
const METRICS = [
  'La seule agence PPT au monde certifiée ISO 9001',
  '85% de réachat',
  '5/5 Note Google Avis',
  'Certifiés Microsoft Office Specialist PowerPoint',
]

export default function Method() {
  const whole = useWhole()
  const root = useRef(null)
  const titles = useRef([])
  const tagline = useRef(null)
  const content = useRef(null)
  const metrics = useRef(null)

  // §6.2 — timeline METHOD (overflowStart = overflowEnd = lvh), charsIn + maskReveal tweens.
  useMotion((ctx) => {
    const tl = sectionTimeline(root.current, { overflowStart: lvh, overflowEnd: lvh }, ctx)
    const marquee = root.current.querySelector('.method__marquee')
    if (marquee) {
      for (const t of titles.current) if (t) charsIn(marquee, [t.querySelector('.title__icon>*'), t])
      parallax(tl, marquee, 200, { overflowStart: 0.6, overflowEnd: 0.5 })
    }
    parallax(tl, tagline.current, 120, { overflowStart: 0.5, overflowEnd: 0.7 })
    parallax(tl, content.current, 40, { overflowStart: 0.2, overflowEnd: 1 })
    linesSlide(tl, tagline.current, 'in', '-x', { overflowStart: 0.25, overflowEnd: 0.2, itemDuration: 0.7 })
    linesSlide(tl, content.current, 'in', 'y', { overflowStart: 0.05, overflowEnd: 0.4, itemDuration: 0.7 })
    maskReveal(metrics.current, 200, 90)
    tl.sync()
  }, whole)

  return (
    <section
      ref={root}
      data-section="method"
      className={`method ${whole ? 'is-whole' : ''} superGrid`}
      style={{ '--gridColumns': 12, '--gridGapBlock': '10.3rem', '--gridGapInline': '1.6rem' }}
    >
      <Marquee className="method__marquee">
        {(i) => (
          <h2 ref={(el) => { titles.current[i] = el }} className="method__marquee-title ff-screamer">
            <span className={`ui-icon ${whole ? 's8' : 's7'} title__icon`} role="presentation" aria-hidden="true">
              <TriangleMirror />
            </span>
            <span className="method__marquee-text">{MARQUEE}</span>
          </h2>
        )}
      </Marquee>
      <p ref={tagline} className="method__tagline ff-inter">{TAGLINE}</p>
      <div className="method__A1">
        <p ref={content} className="method__content ff-inter">{CONTENT}</p>
        <ul ref={metrics} className="method__metrics ff-inter">
          {METRICS.map((m) => (
            <li key={m} className="method__metrics-metric">
              <span className="ui-icon s2" role="presentation" aria-hidden="true"><CheckmarkBadge /></span>
              <span>{m}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
