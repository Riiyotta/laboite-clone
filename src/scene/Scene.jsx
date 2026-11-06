// Fixed full-screen WebGL canvas (spec §3.4): <canvas id="SYNTHRA"> behind #MAIN.
// The scene API is published through sceneBus once ready (see src/scene/scene.js).
import { useEffect, useRef } from 'react'
import { sceneBus } from '../lib/store'
import { createScene } from './engine'

const style = { position: 'fixed', top: 0, left: 0, width: '100vw', height: '100lvh', zIndex: -1, display: 'block', pointerEvents: 'none' }

export default function Scene() {
  const ref = useRef(null)
  useEffect(() => {
    let api = null
    let cancelled = false
    createScene(ref.current).then((a) => {
      if (cancelled) { a?.dispose(); return }
      api = a
      window.__SYNTHRA = a
      if (a) sceneBus.resolve(a)
    }).catch((e) => console.error('[SYNTHRA] init failed', e))
    return () => { cancelled = true; api?.dispose() }
  }, [])
  return <canvas id="SYNTHRA" ref={ref} style={style} aria-hidden="true" />
}
