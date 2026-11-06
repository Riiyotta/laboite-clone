// Hero header DOM layer (spec §3.1–3.3, §3.5 DOM parts, §9 mobile). The visible 3D title/triangles live in src/scene.
// Root <header data-section="hero"> is 700lvh on desktop and is the ScrollTrigger trigger of the HEADER timeline.
import { useEffect, useLayoutEffect, useRef } from 'react'
import { gsap, lvh, ScrollTrigger, sectionTimeline, SplitText } from '../lib/motion'
import { store } from '../lib/store'
import useFormat from './header/useFormat'
import Widgets from './hero/Widgets'
import SeoModal from './hero/SeoModal'
import './hero/hero.css'

const SUBTITLE = "La boite à slides® :<br />seule agence au monde<br />certifiée ISO 9001<br />qui transforme Powerpoint<br />en un puissant levier d'impact<br />pour votre business"

export default function Hero() {
  const { whole } = useFormat()
  const ref = useRef(null)
  const subRef = useRef(null)
  const widgetsRef = useRef(null)

  // Mobile: the hero is a "light" header region (purple block) — original registers it with the header only when not whole.
  useEffect(() => {
    if (whole || !ref.current) return
    const el = ref.current
    store.set({ lightRegions: [...store.get().lightRegions.filter((e) => e !== el), el] })
    return () => store.set({ lightRegions: store.get().lightRegions.filter((e) => e !== el) })
  }, [whole])

  // HEADER timeline (DOM items only): trigger = hero, start "0% 0", end "100%+=lvh lvh"
  useLayoutEffect(() => {
    if (!whole) return
    let st = null
    let split = null
    let alive = true
    let timer = 0
    let buildId = 0
    let sync = () => {}
    const onRefresh = () => sync()
    ScrollTrigger.addEventListener('refresh', onRefresh)
    const build = () => {
      if (!alive || !ref.current || !subRef.current) return
      kill()
      const h1 = subRef.current
      split = new SplitText(h1, { type: 'lines', linesClass: 'line' })
      h1.classList.add('superPreAccents')
      // sectionTimeline.add() with a stagger only immediate-renders the first target → pre-set the from-state.
      gsap.set(split.lines, { y: 20, autoAlpha: 0 })
      st = sectionTimeline(ref.current, { overflowEnd: lvh() })
      st.add(split.lines, { y: 20, autoAlpha: 0 }, { y: 0, autoAlpha: 1 }, { start: 0.75, end: 0.99, itemDuration: 0.15 })
      st.add(h1, { autoAlpha: 1 }, { autoAlpha: 0 }, { start: 1, overflowEnd: 0.7 })
      const id = ++buildId
      st.track({ start: 0, end: 0.5 }, (p) => { if (id === buildId) widgetsRef.current?.update(p) })
      st.tl.scrollTrigger?.refresh()
      // invalidateOnRefresh re-renders the track's fromTo start (p=0) on every ScrollTrigger.refresh(), and a scrubbed
      // tween already past its range never fires again → resync the track from the trigger progress after refreshes.
      const { tStart, tEnd } = st.map({ start: 0, end: 0.5 })
      const cur = st
      sync = () => requestAnimationFrame(() => {
        if (id !== buildId || !cur.tl.scrollTrigger) return
        widgetsRef.current?.update(Math.min(Math.max((cur.tl.scrollTrigger.progress - tStart) / (tEnd - tStart), 0), 1))
      })
      sync()
    }
    const kill = () => {
      if (st) { st.tl.scrollTrigger?.kill(); st.tl.kill(); st = null }
      if (split) { split.revert(); split = null }
      if (subRef.current) { subRef.current.style.removeProperty('visibility'); subRef.current.style.removeProperty('opacity') }
    }
    ;(document.fonts?.ready || Promise.resolve()).then(build)
    let lastW = window.innerWidth
    let lastH = window.innerHeight
    const onResize = () => {
      if (window.innerWidth === lastW && window.innerHeight === lastH) return
      lastW = window.innerWidth; lastH = window.innerHeight
      clearTimeout(timer)
      timer = setTimeout(build, 200)
    }
    window.addEventListener('resize', onResize)
    return () => {
      alive = false
      clearTimeout(timer)
      window.removeEventListener('resize', onResize)
      ScrollTrigger.removeEventListener('refresh', onRefresh)
      kill()
      widgetsRef.current?.reset()
    }
  }, [whole])

  return (
    <>
      <header
        data-section="hero"
        ref={ref}
        className={`heroHeader ${whole ? '@whole' : 'superDevice'}`}
      >
        <div className="hero__title">
          <span className="hero__title-block">
            Les meilleures idées font <strong className="hero__title-strong">l&#39;avenir</strong>
          </span>
          <span className="hero__title-block @right">
            Quand elles sont bien <strong className="hero__title-strong">présentées</strong>
          </span>
        </div>
        <h1 className="hero__subtitle" ref={subRef} dangerouslySetInnerHTML={{ __html: SUBTITLE }} />
        <Widgets whole={whole} ref={widgetsRef} />
      </header>
      <SeoModal />
    </>
  )
}
