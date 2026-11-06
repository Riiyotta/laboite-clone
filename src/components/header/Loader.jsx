// app-loader (spec §2). Single purple panel (the shipped Loader uses `[,]` → one panel; see report) with the
// three-layer mask; spinner animates while the loader is showing/hiding and the menu is closed.
import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { gsap, lvh } from '../../lib/motion'

const parked = () => ({ '--loaderRadiusX': '70%', '--loaderRadiusY': `${Math.min(lvh(), 1500)}px`, maskPosition: '50% 0%' })

export default function Loader({ menuOpen, loaded, onState }) {
  const panelRef = useRef(null)
  const [state, setState] = useState(loaded ? '' : 'show') // 'show' | 'hide' | ''
  const stateRef = useRef(state)
  const tween = useRef(null)
  const set = (v) => { stateRef.current = v; setState(v); onState?.(v) }

  const run = (fromMenu) => {
    const panels = [panelRef.current]
    if (!menuOpen && loaded) {
      if (stateRef.current === 'hide') return
      tween.current?.kill()
      set(fromMenu ? '' : 'hide')
      tween.current = gsap.fromTo(
        panels.reverse(),
        { '--loaderRadiusX': '70%', '--loaderRadiusY': `${Math.min(lvh(), 1500)}px`, maskPosition: '50% 50%' },
        {
          '--loaderRadiusX': '100%', '--loaderRadiusY': '0px', maskPosition: '50% 100%',
          duration: fromMenu ? 1.5 : 1, ease: fromMenu ? 'power2.out' : 'power2.in',
          onComplete: () => { if (stateRef.current) set(''); gsap.set(panels, parked()) },
        },
      )
    } else if (stateRef.current !== 'show') {
      tween.current?.kill()
      set('show')
      tween.current = gsap.to(panels, { '--loaderRadiusX': '100%', '--loaderRadiusY': '0px', maskPosition: '50% 50%', duration: 0.7, ease: 'power2.out' })
    }
  }

  const mounted = useRef(false)
  useLayoutEffect(() => { if (mounted.current) run(true) }, [menuOpen]) // eslint-disable-line react-hooks/exhaustive-deps
  useLayoutEffect(() => { if (mounted.current) run(false) }, [loaded]) // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { mounted.current = true; onState?.(stateRef.current); return () => tween.current?.kill() }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className={`loader ${state === 'show' ? '@show' : ''}`} role="presentation" aria-hidden="true">
      <div className="loader__panel" ref={panelRef}>
        <div className={`loader__panel-spinner ${!menuOpen && state ? '@animated' : ''}`} />
      </div>
    </div>
  )
}
