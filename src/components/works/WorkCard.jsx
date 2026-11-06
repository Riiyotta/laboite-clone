// CollectionWorkCard (reference/nuxt/ChMElkfr.js) — hover physics + title word swap (desktop only).
import { useEffect, useRef } from 'react'
import { gsap, SplitText } from '../tagline/sectionMotion'

export default function WorkCard({ data, whole }) {
  const card = useRef(null)
  const title = useRef(null)

  // Hover physics: targets {x, y, scale, blur}; each tick v += (target - v)·(1 − e^(−7·dt)) → CSS vars.
  useEffect(() => {
    const el = card.current
    if (!el || !whole) return
    let tx = 0, ty = 0, ts = 0, tb = 0
    let x = 0, y = 0, sc = 0, bl = 0
    let H = 0, U = 0
    let ticking = false
    let timer = -1
    const measure = () => { const r = el.getBoundingClientRect(); H = r.width / 2; U = r.height / 2 }
    const k = (d, dt) => d * (1 - Math.exp(-7 * dt))
    const tick = (time, deltaTime) => {
      const dt = deltaTime / 1000
      const dx = tx - x, dy = ty - y, ds = ts - sc, db = tb - bl
      x += k(dx, dt); y += k(dy, dt); sc += k(ds, dt); bl += k(db, dt)
      const done = Math.abs(dx) < 0.001 && Math.abs(dy) < 0.001 && Math.abs(ds) < 0.001 && Math.abs(db) < 0.001
      if (done) bl |= 0
      el.style.setProperty('--x', x)
      el.style.setProperty('--y', y)
      el.style.setProperty('--scale', sc)
      el.style.setProperty('--blur', `${bl}px`)
      if (done) setTicking(false)
    }
    const setTicking = (on) => {
      if (on === ticking) return
      on ? gsap.ticker.add(tick) : gsap.ticker.remove(tick)
      ticking = on
    }
    const clear = () => { if (timer !== -1) { clearTimeout(timer); timer = -1 } }
    const enter = () => { clear(); ts = 0.3; tb = 50 }
    const move = (e) => { tx = (e.offsetX - H) * 0.03; ty = (e.offsetY - U) * 0.03; setTicking(true) }
    const leave = () => { timer = setTimeout(() => { tx = ty = ts = tb = 0; setTicking(true) }, 250) }
    // original measures on app LOAD (cards may still be at the reveal's scale .95) and on RESIZE
    if (document.readyState === 'complete') measure()
    else window.addEventListener('load', measure, { once: true })
    window.addEventListener('resize', measure)
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mousemove', move)
    el.addEventListener('mouseleave', leave)
    return () => {
      clear(); setTicking(false)
      window.removeEventListener('load', measure)
      window.removeEventListener('resize', measure)
      el.removeEventListener('mouseenter', enter)
      el.removeEventListener('mousemove', move)
      el.removeEventListener('mouseleave', leave)
    }
  }, [whole])

  // Title hover (helper `N`, stagger .045): clone after the title; words y 100%→0%, clone words 0%→−100% + fade.
  useEffect(() => {
    const el = card.current
    const t = title.current
    if (!el || !t || !whole) return
    let tl = null
    let clone = null
    const ctx = gsap.context(() => {})
    const create = () => {
      if (tl) return
      ctx.add(() => {
        tl = gsap.timeline({ paused: true })
        clone = t.cloneNode(true)
        clone.setAttribute('role', 'presentation')
        clone.setAttribute('aria-hidden', 'true')
        t.after(clone)
        ;[t, clone].forEach((node, i) => {
          const [a, b] = i ? ['0%', '-100%'] : ['100%', '0%']
          const sp = SplitText.create(node, { type: 'lines,words', linesClass: 'line' })
          sp.lines.forEach((l) => l.parentElement?.classList.add('superPreAccents'))
          tl.fromTo(sp.words, { y: a, ...(i ? { opacity: 1 } : null) }, { y: b, ...(i ? { opacity: 0 } : null), duration: 2.5, stagger: 0.045, ease: 'custom::out' }, 0)
        })
      })
    }
    const play = () => {
      if (!tl || (tl.progress() < 0.15 && !tl.paused())) return
      tl.progress(0)
      tl.play()
    }
    const enter = () => { create(); play() }
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mouseleave', play)
    return () => {
      el.removeEventListener('mouseenter', enter)
      el.removeEventListener('mouseleave', play)
      ctx.revert()
      clone?.remove()
    }
  }, [whole])

  const { title: name, tag, href, img, srcset, alt } = data
  return (
    <a href={href} className="workCardsPanoramic__link">
      <section
        ref={card}
        className="workCard"
        style={{ '--x': 0, '--y': 0, '--scale': 0, '--blur': '0px', '--bgImage': `url(/sk/uploads/thumbnail_${img})` }}
      >
        <div className="workCard__A1">
          <h3 ref={title} className="workCard__title ff-screamer">{name}</h3>
        </div>
        <ul className="workCard__categories">
          <li style={{ display: 'contents' }}>
            <span className="ui-tag ff-inter">{tag}</span>
          </li>
        </ul>
        <div className="workCard__A2">
          <img className="workCard__image" src={`/sk/uploads/${img}`} srcSet={srcset} sizes="(max-width: 767.9px) calc(100vw - 4rem), calc((min(83vw, 1480px) - 6.4rem - .8rem) / 2)" alt={alt} loading="lazy" />
        </div>
      </section>
    </a>
  )
}
