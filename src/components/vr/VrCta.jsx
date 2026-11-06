// UIActionCTA, design "light" (spec B §2.1/§2.2): round white arrow button (`@round @hover @left @lgh @color[drk1]`)
// + white pill (`@hover @bottom @lgh @color[drk1]`), 0 gap. Hovering either button hovers both (spec A §1.2).
import { useEffect, useRef } from 'react'
import { gsap } from '../../lib/motion'
import { Arrow } from '../method/icons'

export default function VrCta({ href, title, className = '' }) {
  const root = useRef(null)
  useEffect(() => {
    const el = root.current
    const btns = el.querySelectorAll('.btn')
    let tweens = []
    let hovered = false
    const kill = () => { tweens.forEach((t) => t.kill()); tweens = [] }
    const set = (on) => {
      if (on === hovered) return
      hovered = on
      kill()
      btns.forEach((b) => {
        b.classList.toggle('@hovered', on)
        tweens.push(on
          ? gsap.fromTo(b, { '--button-hover-y': '0%' }, { '--button-hover-y': '50%', duration: 2.5, ease: 'custom::out' })
          : gsap.to(b, { '--button-hover-y': '100%', duration: 0.4, onComplete: () => gsap.set(b, { '--button-hover-y': '0%' }) }))
      })
    }
    let count = 0
    const flush = () => queueMicrotask(() => set(count > 0))
    const on = () => { count++; flush() }
    const off = () => { count = Math.max(count - 1, 0); flush() }
    btns.forEach((b) => { b.addEventListener('mouseenter', on); b.addEventListener('mouseleave', off) })
    return () => { kill(); btns.forEach((b) => { b.removeEventListener('mouseenter', on); b.removeEventListener('mouseleave', off) }) }
  }, [])
  return (
    <a ref={root} href={href} className={`ui-cta ${className}`}>
      <span className="btn round hover-left d-light cta__icon" tabIndex={0}>
        <span className="ui-icon s1" role="presentation" aria-hidden="true"><Arrow /></span>
      </span>
      <span className="btn hover-bottom d-light ui-cta__button" tabIndex={0}>
        <span className="ui-cta__button-content"><span>{title}</span></span>
      </span>
    </a>
  )
}
