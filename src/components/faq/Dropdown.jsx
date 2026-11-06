// UIWrapperDropdown (reference/nuxt/BPFXOrp3.js). Region max-height animates 0 ↔ --dropdownContentHeight
// (the content <p>'s measured height, resize-observed with a 50ms debounce) via CSS .27s ease-out.
import { useEffect, useId, useRef, useState } from 'react'
import MusicString from './MusicString'

function Disclosure({ open }) {
  return (
    <svg className={`disclosure ${open ? '@open' : ''}`} role="presentation" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeLinecap="round" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="2.66992" x2="8" y2="13.3399" />
      <line x1="2.67188" y1="8" x2="13.3419" y2="8" />
    </svg>
  )
}

export default function Dropdown({ question, answer, open, show, onToggle, hub, visible, whole, loaded }) {
  const uid = useId().replace(/:/g, '')
  const content = useRef(null)
  const [height, setHeight] = useState(null)

  useEffect(() => {
    const el = content.current
    let timer = 0
    const measure = () => setHeight(el.getBoundingClientRect().height)
    const ro = new ResizeObserver(() => { clearTimeout(timer); timer = setTimeout(measure, 50) })
    ro.observe(el)
    return () => { clearTimeout(timer); ro.disconnect() }
  }, [])

  return (
    <div className={`dropdown faq__questions-question ${open ? '@open' : ''} ${show ? '@show' : '@hide'}`}>
      <button
        id={`TRIGGER_${uid}`}
        type="button"
        className="dropdown__trigger"
        aria-expanded={open}
        aria-controls={`REGION_${uid}`}
        onClick={onToggle}
      >
        <span className="dropdown__trigger-title">{question}</span>
        <span className="ui-icon s1" role="presentation" aria-hidden="true"><Disclosure open={open} /></span>
      </button>
      <div
        id={`REGION_${uid}`}
        className="dropdown__region"
        style={{ '--dropdownContentHeight': height != null ? `${height}px` : 'auto' }}
        role="region"
        aria-labelledby={`TRIGGER_${uid}`}
        aria-hidden={!open}
      >
        <p ref={content} className="dropdown__region-content">{answer}</p>
      </div>
      <MusicString hub={hub} visible={visible} whole={whole} loaded={loaded} />
    </div>
  )
}
