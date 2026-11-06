// UIWrapperMarquee (reference/nuxt/Dh-jUWUt.js), rotate 0, duration 30s.
// Track translateX 0 → −trackWidth/2 every 30s (linear, restart) while the clipper intersects.
import { useEffect, useRef } from 'react'
import { gsap } from '../tagline/sectionMotion'

export default function Marquee({ className = '', duration = 30, children }) {
  const clipper = useRef(null)
  const track = useRef(null)
  const drivers = useRef([])

  useEffect(() => {
    const clip = clipper.current
    const tr = track.current
    let M = 0 // −trackWidth/2
    let O = 0 // current offset
    let N = 0 // loop start timestamp (s)
    let D = 0
    let vw = 0
    let h = 0
    let visible = false
    let resizeTimer = 0

    const write = () => { tr.style.transform = `matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, ${D + O}, 0, 0, 1)` }
    const tick = (time) => {
      const t = (time - N) / duration
      if (t > 1) N = time
      O = M * t
      write()
    }
    const layout = (width, height) => {
      // rotate 0: n = vw, clipper height = track height, D = (vw − vw)/2 = 0, driver min-width = vw
      clip.style.height = `${height}px`
      D = 0
      drivers.current.forEach((d) => d && (d.style.minWidth = `${width}px`))
      tr.style.transformOrigin = `${width * 0.5}px ${height * 0.5}px`
    }
    const onResize = (entry) => {
      const { width, height } = entry.contentRect
      const hh = height << 0
      M = width / -2
      const w = window.innerWidth
      if (vw !== w || h !== hh) { h = hh; vw = w; layout(vw, height) }
    }
    const ro = new ResizeObserver(([e]) => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => onResize(e), 50) })
    ro.observe(tr)
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting === visible) return
      visible = e.isIntersecting
      if (visible) {
        N = gsap.ticker.time - (M ? (O / M) * duration : 0)
        tr.classList.add('is-animated')
        gsap.ticker.add(tick)
      } else {
        tr.classList.remove('is-animated')
        gsap.ticker.remove(tick)
      }
    })
    io.observe(clip)
    write()
    return () => { ro.disconnect(); io.disconnect(); gsap.ticker.remove(tick); clearTimeout(resizeTimer) }
  }, [duration])

  return (
    <div className={`ui-marquee ${className}`} style={{ height: 'auto' }}>
      <div ref={clipper} className="ui-marquee__clipper">
        <div ref={track} className="ui-marquee__track" inert="" tabIndex={-1}>
          {[0, 1].map((i) => (
            <div key={i} ref={(el) => { drivers.current[i] = el }} className="ui-marquee__driver" style={{ minWidth: '100vw' }} role={i ? 'presentation' : undefined}>
              {children(i)}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
