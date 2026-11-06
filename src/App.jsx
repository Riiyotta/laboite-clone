import { useLayoutEffect } from 'react'
import { initLenis, ScrollTrigger } from './lib/motion'
import Scene from './scene/Scene'
import Header from './components/Header'
import Hero from './components/Hero'
import Tagline from './components/Tagline'
import Works from './components/Works'
import Method from './components/Method'
import Skills from './components/Skills'
import Expertises from './components/Expertises'
import Vr from './components/Vr'
import Spotlight from './components/Spotlight'
import ResourceCards from './components/ResourceCards'
import LabelCards from './components/LabelCards'
import ReviewCards from './components/ReviewCards'
import Faq from './components/Faq'
import Footer from './components/Footer'

export default function App() {
  useLayoutEffect(() => {
    initLenis()
    const refresh = () => ScrollTrigger.refresh()
    // sections register their ScrollTriggers in their own effects; refresh once fonts/layout settle
    document.fonts.ready.then(refresh)
    window.addEventListener('load', refresh)
    window.addEventListener('resize', refresh)
    return () => { window.removeEventListener('load', refresh); window.removeEventListener('resize', refresh) }
  }, [])
  return (
    <>
      <Scene />
      <Header />
      <main id="MAIN" className="superDevice" style={{ marginBottom: '40rem', transition: 'opacity .3s ease-out' }}>
      <section id="HOME">
        <Hero />
        <Tagline />
        <Works />
        <Method />
        <Skills />
        <Expertises />
        <Vr />
        <Spotlight />
        <ResourceCards />
        <LabelCards />
        <ReviewCards />
        <Faq />
      </section>
      </main>
      <Footer />
    </>
  )
}
