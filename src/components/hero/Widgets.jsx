// app-widgets (spec §3.2): video card + "go" fullscreen button + rotating Scroll badge.
import { forwardRef, useEffect, useImperativeHandle, useLayoutEffect, useRef, useState } from 'react'
import { gsap, getLenis, lvh } from '../../lib/motion'
import { store } from '../../lib/store'
import Button from '../header/Button'
import { Icon, Plus, ScrollBadge, Xmark } from '../header/icons'

const APP_ALIVE_AT = performance.now()
const VIDEO = '/sk/uploads/home_video_SD_79c96be094.mp4'
const raf = () => new Promise((r) => requestAnimationFrame(r))

const Widgets = forwardRef(function Widgets({ whole }, fwd) {
  const rootRef = useRef(null)
  const a1Ref = useRef(null)
  const containerRef = useRef(null) // Transformer A1 (animated container)
  const videoRef = useRef(null)
  const transformTween = useRef(null)
  const stack = useRef([])
  const [mounted, setMounted] = useState(false) // video mounted 3 frames after LOAD
  const [shown, setShown] = useState(false) // A1 '@hide' until metadata
  const [hide, setHide] = useState(false) // '@hide' after the hero track leaves (y > 2700)
  const [D, setD] = useState(-1) // -1 idle, 1 opening, 2 open, 0 closing
  const Dref = useRef(-1)
  const setDv = (v) => { Dref.current = v; setD(v) }

  // header timeline track (0 → .5): --progress + scale; '@hide' on leave
  useImperativeHandle(fwd, () => ({
    update(p) {
      const el = rootRef.current
      if (!el) return
      el.style.setProperty('--progress', `${p * 100}%`)
      el.style.setProperty('transform', `scale(${1 + p * 0.15})`)
      setHide(p >= 1)
    },
    reset() { setHide(false) },
  }), [])

  // LOAD → wait 3 frames → mount the video
  useEffect(() => {
    let alive = true
    const go = async () => { await raf(); await raf(); await raf(); if (alive) setMounted(true) }
    if (store.get().loaded) go()
    const un = store.subscribe((s) => { if (s.loaded && !mounted) go() })
    return () => { alive = false; un() }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // once metadata is available: reveal A1 + intro tween (desktop only)
  useEffect(() => {
    const v = videoRef.current
    if (!mounted || !v) return
    let done = false
    const intro = () => {
      if (done) return
      done = true
      setShown(true)
      if (whole && a1Ref.current) {
        gsap.fromTo(a1Ref.current, { y: 20, scale: 1.03, autoAlpha: 0 }, {
          y: 0, scale: 1, autoAlpha: 1, duration: 7, ease: 'custom::out',
          delay: Math.max(3.5 - (performance.now() - APP_ALIVE_AT) / 1e3, 0),
        })
      }
    }
    if (v.readyState > HTMLMediaElement.HAVE_METADATA) intro()
    else v.addEventListener('loadedmetadata', intro, { once: true })
    return () => v.removeEventListener('loadedmetadata', intro)
  }, [mounted, whole])

  useEffect(() => { if (videoRef.current) videoRef.current.muted = D < 1 }, [D, mounted])

  // ---- Transformer (UIWrapperTransformer) ----
  const tweenTo = (x, y, width, height) => {
    transformTween.current?.kill()
    transformTween.current = gsap.to(containerRef.current, {
      x, y, width, height, duration: 2, ease: 'custom::out',
      onComplete: () => setDv(Dref.current > 0 ? 2 : -1),
    })
  }
  const place = (rect, save = false) => {
    const n = containerRef.current
    if (!n) return null
    const last = stack.current[stack.current.length - 1]
    if (last && last.top === rect.top && last.left === rect.left && last.width === rect.width && last.height === rect.height) return null
    let top = n.offsetTop
    let left = n.offsetLeft
    let o = n
    while ((o = o.offsetParent)) { top += o.offsetTop; left += o.offsetLeft }
    tweenTo(rect.left - left, rect.top - top, rect.width, rect.height)
    return save ? { top, left, width: n.offsetWidth, height: n.offsetHeight } : null
  }
  const targetRect = () => {
    const el = rootRef.current
    if (!el) return null
    const cs = getComputedStyle(el)
    const pt = parseFloat(cs.paddingTop) || 0
    const pl = parseFloat(cs.paddingLeft) || 0
    return { top: pt + (whole ? 0 : window.scrollY), left: pl, width: window.innerWidth - pl * 2, height: lvh() - pt * 2 }
  }
  const open = () => {
    if (Dref.current > 0) return
    const r = targetRect()
    if (!r) return
    const saved = place(r, true)
    if (saved) stack.current.push(saved)
    setDv(1)
    getLenis()?.stop()
  }
  const close = () => {
    if (Dref.current < 1) return
    stack.current.length = 0
    tweenTo(0, 0, '100%', '100%')
    setDv(0)
    getLenis()?.start()
  }
  const onMedia = () => (Dref.current > 0 ? close() : open())

  useEffect(() => {
    const onResize = () => {
      if (Dref.current < 1) return
      const r = targetRect()
      if (r) { place(r); setDv(1) }
    }
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  })
  useLayoutEffect(() => () => transformTween.current?.kill(), [])

  const cls = [
    'widgets',
    whole ? '@whole' : '',
    whole && hide ? '@hide' : '',
    D !== -1 ? `@up ${D === 0 ? 'up-0' : ''}` : '',
  ].filter(Boolean).join(' ')

  return (
    <div className={cls} style={{ '--transformer-height': '22rem' }} ref={rootRef}>
      <div className={`widgets__A1 ${shown ? '' : '@hide'}`} ref={a1Ref}>
        <div className="transformer widgets__transformer" style={{ width: '30rem', height: '22rem' }}>
          <div className="transformer__A1 widgets__transformer-container" ref={containerRef}>
            <div className="widgets__A2">
              {mounted && (
                <video ref={videoRef} className="container__media" src={VIDEO} autoPlay loop muted playsInline preload="auto" onClick={onMedia} />
              )}
              {whole && (
                <Button round design="lightGlass" hover="bottom" label="Fermer" className={`container__back ${D < 1 ? '@hide' : ''}`} onClick={close}>
                  <Icon size={1}><Xmark /></Icon>
                </Button>
              )}
            </div>
          </div>
        </div>
        {whole && (
          <Button round design="lightGlass" hover="bottom" label="Afficher en pleine écran" className={`widgets__go ${D > 0 ? '@hide' : ''}`} onClick={open}>
            <Icon size={1}><Plus /></Icon>
          </Button>
        )}
      </div>
      {whole && <ScrollBadge className="scrollBadge" />}
    </div>
  )
})

export default Widgets
