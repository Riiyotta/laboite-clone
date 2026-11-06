// UIUtilMusicString (reference/nuxt/BPFXOrp3.js): a quadratic-curve "string" under each FAQ row.
// Control point (cx, cy) in a 0–100 viewBox, rest (50, 50). Desktop only ("earthquake" reactor off on mobile).
//  - pointer inside the svg rect and within 15 units of the current cy → pluck:
//      cx → pointer x (.1s), cy → 50 + (r − 50)·.4 (.1s)
//  - otherwise / mouseleave → release once: cx → 50 (.7s), cy → 50 (.7s elastic.out(1.5, .3))
//  - while the list is visible: on scroll, cy → 50 + clamp(scrollDelta, −15, 15) (.15s)
import { useEffect, useRef } from 'react'
import { gsap } from '../tagline/sectionMotion'

const F = 100
const I = F / 2
const L = 0.4
const R = 15

export default function MusicString({ hub, visible, whole, loaded }) {
  const svg = useRef(null)
  const path = useRef(null)
  const state = useRef(null)
  const loadedRef = useRef(loaded)
  loadedRef.current = loaded

  // earthquake reactor: mouse forwarding
  useEffect(() => {
    if (!whole) return
    const v = { x: I, y: I }
    let released = false
    let O = null
    let k = null
    const draw = () => path.current?.setAttribute('d', `M0,${I} Q${v.x},${v.y} ${F},${I}`)
    const to = (key, value, vars) => gsap.to(v, { [key]: value, ...vars, onUpdate: draw })
    const release = () => {
      if (released) return
      O?.kill(); k?.kill()
      O = to('x', I, { duration: 0.7 })
      k = to('y', I, { duration: 0.7, ease: 'elastic.out(1.5, .3)' })
      released = true
    }
    const onMouse = (e) => {
      if (!loadedRef.current) return
      if (!e) return release()
      const r = svg.current.getBoundingClientRect()
      const x = e.clientX
      const y = e.clientY
      if (!(x > r.left && x < r.right && y > r.top && y < r.bottom)) return release()
      const rr = ((y - r.top) / r.height) * F
      if (Math.abs(v.y - rr) > R) return release()
      released = false
      O?.kill(); k?.kill()
      O = to('x', ((x - r.left) / r.width) * F, { duration: 0.1 })
      k = to('y', I + (rr - I) * L, { duration: 0.1 })
    }
    const sag = (dy) => {
      k?.kill()
      k = to('y', I + gsap.utils.clamp(-15, 15, dy), { duration: 0.15 })
    }
    state.current = { sag }
    hub.add(onMouse)
    return () => {
      hub.delete(onMouse)
      state.current = null
      O?.kill(); k?.kill()
      v.x = v.y = I
      draw()
    }
  }, [hub, whole])

  // visible reactor: scroll sag
  useEffect(() => {
    if (!whole || !visible) return
    let last = window.scrollY
    const onScroll = () => {
      const y = window.scrollY
      const dy = y - last
      last = y
      if (loadedRef.current) state.current?.sag(dy)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [whole, visible])

  return (
    <svg ref={svg} className="musicString dropdown__musicString" viewBox={`0 0 ${F} ${F}`} preserveAspectRatio="none" role="presentation" aria-hidden="true">
      <path ref={path} d={`M0,${I} Q${I},${I} ${F},${I}`} fill="none" strokeWidth="1" vectorEffect="non-scaling-stroke" />
    </svg>
  )
}
