// Image component behaviour of the original (`media` images): the `sizes` attribute is kept equal to the
// element's rendered (untransformed) width in px, so the browser picks the matching srcset candidate.
import { useEffect } from 'react'

export function useAutoSizes(rootRef, selector = 'img[srcset]') {
  useEffect(() => {
    const root = rootRef.current
    if (!root) return
    const imgs = [...root.querySelectorAll(selector)]
    const ro = new ResizeObserver((entries) => {
      for (const e of entries) e.target.setAttribute('sizes', `${e.contentRect.width}px`)
    })
    imgs.forEach((i) => ro.observe(i))
    return () => ro.disconnect()
  }, [rootRef, selector])
}

const U = '/sk/uploads/'
// thumbnail 1w, small 500w, medium 750w, large 1000w (as in reference/original.html)
export const srcSet = (name) =>
  [['thumbnail_', 1], ['small_', 500], ['medium_', 750], ['large_', 1000]].map(([p, w]) => `${U}${p}${name} ${w}w`).join(', ')
