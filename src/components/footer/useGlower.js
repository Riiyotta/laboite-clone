// `Glower` (reference/nuxt/B6fTRVdz.js class p): drives the `superGlass @glow` CSS vars from the pointer.
// Per tick: intensity += (target − intensity)·.03; bgRX/RY += (mouse% − cur)·.05; maskRX/RY += (mouse% − cur)·.07,
// mouse% = clamp(1 − (pointer − rectStart)/rectSize, 0, 1)·100. Ticker unsubscribes once every delta < .001.
import { useEffect } from 'react'
import { gsap } from '../tagline/sectionMotion'

const EPS = 0.001

export function useGlower(ref, enabled) {
  useEffect(() => {
    const el = ref.current
    if (!enabled || !el) return
    const st = el.style
    let target = 0
    let intensity = 0
    let mx = 50
    let my = 50
    let bx = 50
    let by = 50
    let kx = 50
    let ky = 50
    let ticking = false
    const tick = () => {
      const t = target - intensity
      const n = mx - bx
      const r = my - by
      const i = mx - kx
      const a = my - ky
      st.setProperty('--glassIntensity', `${(intensity += t * 0.03)}`)
      st.setProperty('--glassBackgroundRX', `${(bx += n * 0.05)}%`)
      st.setProperty('--glassBackgroundRY', `${(by += r * 0.05)}%`)
      st.setProperty('--glassMaskRX', `${(kx += i * 0.07)}%`)
      st.setProperty('--glassMaskRY', `${(ky += a * 0.07)}%`)
      if (Math.abs(t) < EPS && Math.abs(n) < EPS && Math.abs(r) < EPS && Math.abs(i) < EPS && Math.abs(a) < EPS) setTicking(false)
    }
    const setTicking = (on) => {
      if (on === ticking) return
      if (on) gsap.ticker.add(tick)
      else gsap.ticker.remove(tick)
      ticking = on
    }
    const enter = () => { target = 1; setTicking(true) }
    const leave = () => { target = 0 }
    const move = (e) => {
      const rc = el.getBoundingClientRect()
      mx = gsap.utils.clamp(0, 1, 1 - (e.clientX - rc.left) / rc.width) * 100
      my = gsap.utils.clamp(0, 1, 1 - (e.clientY - rc.top) / rc.height) * 100
      setTicking(true)
    }
    setTicking(true)
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mouseleave', leave)
    el.addEventListener('mousemove', move)
    return () => {
      setTicking(false)
      el.removeEventListener('mouseenter', enter)
      el.removeEventListener('mouseleave', leave)
      el.removeEventListener('mousemove', move)
      for (const p of ['--glassIntensity', '--glassBackgroundRX', '--glassBackgroundRY', '--glassMaskRX', '--glassMaskRY']) st.removeProperty(p)
    }
  }, [ref, enabled])
}
