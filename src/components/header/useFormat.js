// Format detection (spec §0.1). mobile = max-width 767.9px OR max-height 434.9px.
// "crushed" = the height-only mobile case (original format "C": mobile flags set, but layouts keep desktop columns).
import { useEffect, useState } from 'react'

const MQ_MOBILE = '(max-width: 767.9px), (max-height: 434.9px)'
const MQ_NARROW = '(max-width: 767.9px)'

const read = () => {
  const mobile = window.matchMedia(MQ_MOBILE).matches
  const crushed = mobile && !window.matchMedia(MQ_NARROW).matches
  return { mobile, crushed, whole: !mobile }
}

export default function useFormat() {
  const [f, setF] = useState(read)
  useEffect(() => {
    const a = window.matchMedia(MQ_MOBILE)
    const b = window.matchMedia(MQ_NARROW)
    const on = () => setF(read())
    a.addEventListener('change', on)
    b.addEventListener('change', on)
    return () => { a.removeEventListener('change', on); b.removeEventListener('change', on) }
  }, [])
  return f
}
