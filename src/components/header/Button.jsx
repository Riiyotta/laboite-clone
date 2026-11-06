// UIActionButton (spec §1.2). Designs map to the shared .btn/.d-* classes from src/index.css.
// Hover sweep: '--button-hover-y' 0% → 50% (2.5s custom::out) on enter, → 100% (.4s) then reset on leave.
// Hover is only armed once the app is loaded (original: react only when __APP_IS_LOADED).
import { forwardRef, useEffect, useLayoutEffect, useRef, useState } from 'react'
import { gsap } from '../../lib/motion'
import { store } from '../../lib/store'

const DESIGN = { light: 'd-light', dark: 'd-dark', primary: 'd-primary', lightGlass: 'd-lightGlass', darkGlass: 'd-darkGlass' }

export function useLoaded() {
  const [loaded, setLoaded] = useState(store.get().loaded)
  useEffect(() => store.subscribe((s) => setLoaded(s.loaded)), [])
  return loaded
}

const Button = forwardRef(function Button(
  { as, href, design, round = false, hover = '', hovered = false, className = '', label, onMouseEnter, onMouseLeave, onClick, children, ...rest },
  fwdRef,
) {
  const elRef = useRef(null)
  const tween = useRef(null)
  const loaded = useLoaded()
  const [inside, setInside] = useState(false)
  const active = !!hover && loaded && (inside || hovered)
  const first = useRef(true)

  useLayoutEffect(() => {
    if (first.current) { first.current = false; if (!active) return }
    const el = elRef.current
    if (!el || !hover) return
    tween.current?.kill()
    tween.current = active
      ? gsap.fromTo(el, { '--button-hover-y': '0%' }, { '--button-hover-y': '50%', duration: 2.5, ease: 'custom::out' })
      : gsap.to(el, { '--button-hover-y': '100%', duration: 0.4, onComplete: () => gsap.set(el, { '--button-hover-y': '0%' }) })
  }, [active, hover])
  useEffect(() => () => tween.current?.kill(), [])

  const setRef = (n) => {
    elRef.current = n
    if (typeof fwdRef === 'function') fwdRef(n)
    else if (fwdRef) fwdRef.current = n
  }
  const Tag = as || (href ? 'a' : 'button')
  const cls = [
    'btn lbsBtn',
    round ? 'round' : '',
    hover ? `lbsHover hover-${hover}` : '',
    (hovered || inside) && hover ? '@hovered' : '',
    DESIGN[design] || '',
    className,
  ].filter(Boolean).join(' ')
  return (
    <Tag
      ref={setRef}
      className={cls}
      href={href}
      type={Tag === 'button' ? 'button' : undefined}
      aria-label={label}
      onMouseEnter={(e) => { setInside(true); onMouseEnter?.(e) }}
      onMouseLeave={(e) => { setInside(false); onMouseLeave?.(e) }}
      onClick={onClick}
      {...rest}
    >
      {children}
    </Tag>
  )
})

export default Button
