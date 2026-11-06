// §4 Tagline sticker. DOM layer only — green/white background layers and the triangle "fence"
// are drawn by the WebGL scene (it uses data-section="tagline" as its trigger).
import { useRef } from 'react'
import { useWhole, useMotion, sectionTimeline, linesSlide, parallax, fade, lvh } from './tagline/sectionMotion'
import './tagline/sectionMotion.css'
import './tagline/tagline.css'

const TITLE = 'Notre agence PowerPoint amplifie le retentissement des présentations stratégiques des leaders. On équipe ceux qui veulent faire bouger les lignes, dans tous les secteurs'
const CONTENT = 'Nos clients ont des idées fortes, des stratégies à partager, des messages complexes à faire passer.\nAvec des contenus interactifs et des expériences captivantes, ils offrent à leur cible ce qu’il y a de plus puissant : l’évidence. '

export default function Tagline() {
  const whole = useWhole()
  const root = useRef(null)
  const title = useRef(null)
  const content = useRef(null)

  // §4.2 — timeline TAGLINE, overflowStart = overflowEnd = lvh
  useMotion((ctx) => {
    const tl = sectionTimeline(root.current, { overflowStart: lvh, overflowEnd: lvh }, ctx)
    linesSlide(tl, title.current, 'in', '-x', { start: 0.15, end: 0.63, itemDuration: 0.27 })
    linesSlide(tl, content.current, 'in', 'y', { start: 0.35, end: 0.7, itemDuration: 0.17 })
    parallax(tl, content.current, 20, { start: 0.35, end: 1 })
    fade(tl, [title.current, content.current], 'out', { start: 0.87, end: 1 })
    tl.sync()
  }, whole)

  return (
    <section
      ref={root}
      data-section="tagline"
      className={`tagline ui-sticker ${whole ? 'is-whole' : 'is-fit superDevice'}`}
      style={{ height: whole ? '500lvh' : 'fit-content' }}
    >
      <div
        className="tagline__track ui-sticker__track superGrid ff-inter"
        style={{ '--gridColumns': 12, '--gridGapBlock': whole ? '3.2rem' : '10.3rem', '--gridGapInline': '1.6rem' }}
      >
        <h2 ref={title} className="tagline__title">{TITLE}</h2>
        <p ref={content} className="tagline__content">{CONTENT}</p>
      </div>
    </section>
  )
}
