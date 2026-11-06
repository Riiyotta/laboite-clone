// APP-FULL (`_full_6udqo`): 100vw block, JS `translateX(-rect.x)` so it bleeds to the viewport edges
// (recomputed on load / resize). rect.x is measured on the untransformed parent box.
import { forwardRef, useLayoutEffect, useRef } from 'react'

const Full = forwardRef(function Full({ as: Tag = 'div', className = '', style, children, ...rest }, fwd) {
  const el = useRef(null)
  useLayoutEffect(() => {
    const n = el.current
    if (!n) return
    const set = () => {
      const p = n.parentElement
      if (!p) return
      const x = p.getBoundingClientRect().left
      n.style.transform = `translateX(${-x}px)`
    }
    set()
    window.addEventListener('load', set)
    window.addEventListener('resize', set)
    return () => { window.removeEventListener('load', set); window.removeEventListener('resize', set) }
  }, [])
  const ref = (n) => {
    el.current = n
    if (typeof fwd === 'function') fwd(n)
    else if (fwd) fwd.current = n
  }
  return (
    <Tag ref={ref} className={`lbsFull ${className}`} style={style} {...rest}>
      {children}
    </Tag>
  )
})

export default Full
