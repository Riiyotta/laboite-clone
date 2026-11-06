// UIActionCTA: round arrow button (@hover @left) + pill (@hover @bottom); hovering either sweeps both.
import { useState } from 'react'
import Button from './Button'
import { Arrow, Icon } from './icons'

export default function ActionCTA({ design = 'light', href, className = '', onClick, children }) {
  const [hov, setHov] = useState(false)
  const Tag = href ? 'a' : 'button'
  const on = () => setHov(true)
  const off = () => setHov(false)
  return (
    <Tag className={`lbsCta ${className}`} href={href} type={href ? undefined : 'button'} onClick={onClick}>
      <Button as="span" round design={design} hover="left" hovered={hov} className="cta__icon" onMouseEnter={on} onMouseLeave={off}>
        <Icon size={1}><Arrow /></Icon>
      </Button>
      <Button as="span" design={design} hover="bottom" hovered={hov} className="lbsCta__button" onMouseEnter={on} onMouseLeave={off}>
        <span className="lbsCta__button-content">{children}</span>
      </Button>
    </Tag>
  )
}
