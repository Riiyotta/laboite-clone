// SEO modal (spec §8) — hidden "still readable" modal. Opened/closed by the footer info trigger (other agent):
//   window.dispatchEvent(new CustomEvent('lbs:seo-modal'))            → toggle
//   window.dispatchEvent(new CustomEvent('lbs:seo-modal', { detail: true|false })) → open / close
import { useEffect, useState } from 'react'
import { getLenis } from '../../lib/motion'
import Button from '../header/Button'
import { Icon, Xmark } from '../header/icons'
import useFormat from '../header/useFormat'
import html from './seoContent'

export default function SeoModal() {
  const [show, setShow] = useState(false)
  const { mobile } = useFormat()

  useEffect(() => {
    const on = (e) => setShow((v) => (typeof e.detail === 'boolean' ? e.detail : !v))
    window.addEventListener('lbs:seo-modal', on)
    return () => window.removeEventListener('lbs:seo-modal', on)
  }, [])
  useEffect(() => {
    const l = getLenis()
    if (show) l?.stop()
    else l?.start()
  }, [show])

  return (
    <div
      className={`seoModal modal @stillReadable ${show ? '@show' : ''}`}
      aria-labelledby="SEO_MODAL__TITLE"
      aria-describedby=""
      data-lenis-prevent=""
    >
      <div className={`modal__A1 superDevice superGrid ${mobile ? '@margin-mobile' : ''}`}>
        <Button
          round
          className={`modal__close ${show ? '' : '@off'}`}
          label="Close"
          tabIndex={show ? 0 : -1}
          disabled={!show}
          aria-hidden={show ? undefined : 'true'}
          onClick={() => setShow(false)}
        >
          <Icon size={2}><Xmark /></Icon>
        </Button>
        <section className="seoContent seoModal__content" dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    </div>
  )
}
