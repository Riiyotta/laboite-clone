// Fixed #HEADER (spec §1) + loader (§2) + menu overlay (§1.5).
import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { gsap, getLenis, isWhole } from '../lib/motion'
import { store, sceneBus } from '../lib/store'
import Button from './header/Button'
import Loader from './header/Loader'
import Menu from './header/Menu'
import useFormat from './header/useFormat'
import { Icon, Logo, Points } from './header/icons'
import './header/header.css'

// App LOAD: window load + fonts + (desktop) the WebGL scene signalling ready.
// SPEC GAP: the original waits on its own asset queue (__app_addWait); the 12s cap below is a safety net only.
function waitForAppLoad() {
  const winLoad = document.readyState === 'complete' ? null : new Promise((r) => window.addEventListener('load', r, { once: true }))
  const scene = isWhole() ? new Promise((r) => sceneBus.onReady(r)) : null
  const all = Promise.all([winLoad, document.fonts?.ready, scene])
  return Promise.race([all, new Promise((r) => setTimeout(r, 12000))])
}

export default function Header() {
  const { mobile, crushed } = useFormat()
  const [s, setS] = useState(() => ({ ...store.get() }))
  const [loaderState, setLoaderState] = useState('show')
  const ref = useRef(null)
  const { loaded, menuOpen: open, headerLight: light } = s

  useEffect(() => store.subscribe((st) => setS({ ...st })), [])

  useEffect(() => {
    let alive = true
    waitForAppLoad().then(() => { if (alive && !store.get().loaded) store.set({ loaded: true }) })
    return () => { alive = false }
  }, [])

  // Load intro (desktop only): logo from x:-7, CTA from x:7 — 7s, delay .7, custom::out
  useLayoutEffect(() => {
    if (!loaded || !ref.current || !isWhole()) return
    const root = ref.current
    const ctx = gsap.context(() => {
      gsap.from(root.querySelector('.header__reload'), { x: -7, duration: 7, delay: 0.7, ease: 'custom::out' })
      gsap.from(root.querySelector('.header__cta'), { x: 7, duration: 7, delay: 0.7, ease: 'custom::out' })
    }, root)
    return () => ctx.revert()
  }, [loaded])

  const setMenu = (v) => {
    if (!store.get().loaded) return
    const l = getLenis()
    if (v) l?.stop(); else l?.start()
    store.set({ menuOpen: v })
  }
  const onMenuLink = (e) => {
    const a = e.currentTarget
    if (a instanceof HTMLAnchorElement && window.location.pathname === new URL(a.href).pathname) setMenu(false)
  }

  const logoColor = light && !open ? '@color[lgh1]' : '@color[drk1]'
  const triggerDesign = open ? 'light' : light || loaderState ? 'lightGlass' : 'darkGlass'
  const ctaDesign = light && !open ? 'light' : 'dark'

  return (
    <header id="HEADER" data-section="header" ref={ref}>
      <Loader menuOpen={open} loaded={loaded} onState={setLoaderState} />
      <div className={`header__A1 superDevice ${mobile && !crushed ? '@mobile' : ''}`}>
        <a className="header__reload" href="/">
          <Logo className={`logo header__reload-logo superFont ${logoColor}`} />
        </a>
        <Button
          design={triggerDesign}
          hover="bottom"
          className={`header__menuTrigger ${loaded ? '' : '@hidden'} ${open ? '@open' : '@close'}`}
          onClick={() => setMenu(!store.get().menuOpen)}
        >
          <Icon size={3} className="header__menuTrigger-icon"><Points /></Icon>
          <span className="header__B1">
            <span className="header__C1">Menu</span>
            <span className="header__C2">Fermer</span>
          </span>
        </Button>
        <Button href="/contact" design={ctaDesign} hover="bottom" className="header__cta">
          Demander un devis
        </Button>
      </div>
      <Menu show={open} loaded={loaded} mobile={mobile} crushed={crushed} onClose={onMenuLink} />
    </header>
  )
}
