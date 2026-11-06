// Port of the original `Swiper` component (reference/nuxt/CfSd5rt5.js) as used by ReviewCards:
// propInertia, propBounds, propEdgeResistance .7, no snap. Prev/next tween x to -offsetLeft[index±1]
// (.7s power2.out); index follows drag/throw; nav state @start/@end/@off. Lenis is NOT stopped (original doesn't).
import { useEffect, useRef, useState } from 'react'
import { gsap } from '../tagline/sectionMotion'
import { Draggable } from 'gsap/Draggable'
import { InertiaPlugin } from 'gsap/InertiaPlugin'

gsap.registerPlugin(Draggable, InertiaPlugin)

export function useSwiper(trackRef, slideSelector, loaded) {
  const [edge, setEdge] = useState(-1) // -1 none, 0 @start, 1 @end, 2 both
  const [off, setOff] = useState(false)
  const api = useRef({ go: () => {} })
  const loadedRef = useRef(loaded)
  loadedRef.current = loaded

  useEffect(() => {
    const track = trackRef.current
    if (!track) return
    let N = 0 // max scroll
    let M = [] // snap offsets per slide
    let F = 0 // last reachable index
    let P = -1 // current index
    let drag = null
    let step = null
    let throwing = false
    let dead = false

    const getX = () => {
      const v = gsap.getProperty(track, 'x')
      return typeof v === 'string' ? parseFloat(v) : v
    }
    const updateEdge = (x) => {
      let t = -1
      if (x >= 0) t++
      if (x <= -N) t += 2
      setEdge(t)
    }
    const measure = () => {
      N = track.scrollWidth - track.offsetWidth
      M = []
      const slides = track.querySelectorAll(slideSelector)
      for (let t = 0, n = 0; t < slides.length; t++) {
        const s = slides[t]
        const e = s.offsetParent === track ? s.offsetLeft : s.offsetLeft - track.offsetLeft
        if (e > N) {
          F = n < N ? ((M[t] = N), t) : t - 1
          break
        }
        M[t] = n = e
      }
    }
    const onUpdate = () => {
      const x = drag.x
      let t = 0
      for (let n = F; n > -1; n--) if (-M[n] > x) { t = n; break }
      P = t
      updateEdge(x)
    }
    const goTo = (i) => {
      if (i < 0 || i > F) return
      step?.kill()
      P = i
      step = gsap.to(track, {
        x: -M[P], duration: 0.7, ease: 'power2.out',
        onComplete: () => { step = null; updateEdge(getX()) },
      })
    }
    api.current.go = (next) => {
      if (!loadedRef.current || throwing) return
      goTo(next ? P + 1 : P - 1)
    }

    const init = () => {
      if (dead) return
      measure()
      drag = Draggable.create(track, {
        type: 'x',
        inertia: true,
        bounds: { minX: -N, maxX: 0 },
        edgeResistance: 0.7,
        onDrag: onUpdate,
        onThrowUpdate: onUpdate,
        onDragStart: () => { step?.kill(); step = null },
        onDragEnd: () => { throwing = true; setOff(true) },
        onThrowComplete: () => { throwing = false; setOff(false) },
      })[0]
      P = 0
      updateEdge(0)
    }
    document.fonts.ready.then(init)

    // propResize (100ms delay): re-measure + re-apply bounds
    let timer = 0
    const ro = new ResizeObserver(() => {
      clearTimeout(timer)
      timer = setTimeout(() => {
        if (!drag || dead) return
        measure()
        drag.applyBounds({ minX: -N, maxX: 0 })
        drag.update()
      }, 100)
    })
    ro.observe(track)

    return () => {
      dead = true
      clearTimeout(timer)
      ro.disconnect()
      step?.kill()
      drag?.kill()
      gsap.set(track, { clearProps: 'transform' })
    }
  }, [trackRef, slideSelector])

  const navClass = [off ? '@off' : '', edge === 0 || edge === 2 ? '@start' : '', edge === 1 || edge === 2 ? '@end' : '']
    .filter(Boolean).join(' ')
  return { navClass, go: (next) => api.current.go(next) }
}
