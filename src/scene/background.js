// Background gradient shader (spec §3.4 "Background gradient") — mirrors reference/nuxt/BRhYCSnD.js.
import * as THREE from 'three'

const VERT = `varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, .0, 1.0);
}`

const FRAG_HEAD = `uniform float uTime;
uniform float uSpeed;
uniform float uCurveSharpness;
uniform float uNoiseStrength;
uniform float uWaveFrequency;
uniform float uWaveAmplitude;
uniform float uWaveSpeed;
uniform float uParallax;
uniform vec3 uColorTopInitial;
uniform vec3 uColorBottomInitial;
uniform vec3 uColorTopFinal;
uniform vec3 uColorBottomFinal;
uniform float uTransitionFinal;
uniform float uCurveAmountFinal;
`
const FRAG_BODY = `
varying vec2 vUv;

vec3 linearToSrgb(vec3 linear) {
    return mix(linear * 12.92, pow(linear, vec3(1.0 / 2.4)) * 1.055 - 0.055, step(0.0031308, linear));
}

float computeCurvedLineMask(float transition, float curveSharpness, float curveAmount, float uvX, float uvY) {
    if (transition <= 0.0) {
        return 0.0;
    }
    float normalizedX = (uvX - 0.5) * 2.0;
    float curveOffset = normalizedX * normalizedX * curveAmount;
    float maxCurveOffset = abs(curveAmount);
    float baseHeight = mix(-maxCurveOffset, 1.0, transition);
    float curveHeight = baseHeight - curveOffset;
    curveHeight = clamp(curveHeight, 0.0, 1.0);
    float edgeSmooth = 0.015 * (10.0 - curveSharpness);
    return 1.0 - smoothstep(curveHeight - edgeSmooth, curveHeight + edgeSmooth, uvY);
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

void main() {
    float wave1      = sin((vUv.x + uTime * uWaveSpeed) * uWaveFrequency) * uWaveAmplitude;
    float wave2      = sin((vUv.x * 1.7 - uTime * uWaveSpeed * 1.3) * (uWaveFrequency * 0.6) + vUv.y * 3.14159) * (uWaveAmplitude * 0.6);
    float waveOffset = wave1 + wave2;

    float scroll       = fract(vUv.y + waveOffset + uTime * uSpeed);
    float curvedScroll = pow(scroll, 1.2);

    vec3 baseGradient = mix(linearToSrgb(uColorBottomInitial), linearToSrgb(uColorTopInitial), curvedScroll);
`
const FRAG_TAIL = `
    baseGradient = mix(baseGradient, mix(linearToSrgb(uColorBottomFinal), linearToSrgb(uColorTopFinal), curvedScroll), computeCurvedLineMask(uTransitionFinal, uCurveSharpness, uCurveAmountFinal, vUv.x, vUv.y));

    float grain = noise(vec2(vUv.x * 4.0 + waveOffset * 2.0, vUv.y * 4.0 + uTime * 0.25));
    baseGradient += (grain - 0.5) * uNoiseStrength;

    float vignette = smoothstep(1.1, 0.35, distance(vUv, vec2(0.5)));
    baseGradient *= mix(0.85, 1.05, vignette + uParallax * waveOffset);

    gl_FragColor = vec4(baseGradient, 1.0);
}`

// Colour pairs (spec §0.3) — strings go through THREE.Color (sRGB → linear), numbers via setHex, as in the original.
export const COLORS = {
  LGH: ['#FFFFFF', 0xededed],
  PRM: ['#6630FF', 0x612ef1],
  SCD: ['#62F740', 0x61ed40],
  TRT: ['#29DAFF', 0x27cef1],
  DRK: ['#120042', 0x10003d],
  GRY: ['#CECECE', 0xcbcbcb],
  BLK: [0x080808, 0x080808],
}
// Home layer order (spec §3.4): 1 PRM, 2 LGH, 3 SCD, 4 LGH, 5 TRT, 6 LGH, 7 BLK, 8 LGH, 9 DRK, 10 LGH
export const HOME_LAYERS = ['PRM', 'LGH', 'SCD', 'LGH', 'TRT', 'LGH', 'BLK', 'LGH', 'DRK', 'LGH']

export function createBackground(layerNames = HOME_LAYERS) {
  const uniforms = {
    uTime: { value: 0 }, uSpeed: { value: 0.06 }, uCurveSharpness: { value: 10 }, uNoiseStrength: { value: 0.12 },
    uWaveFrequency: { value: 2.3 }, uWaveAmplitude: { value: 0.59 }, uWaveSpeed: { value: 0.06 }, uParallax: { value: 0.15 },
    uColorTopInitial: { value: new THREE.Color(COLORS.LGH[0]) },
    uColorBottomInitial: { value: new THREE.Color(COLORS.LGH[1]) },
    // "final" layer (PRM) — drawn above every numbered layer; driven by the footer (spec B §0.2 / §8.4)
    uColorTopFinal: { value: new THREE.Color(COLORS.PRM[0]) },
    uColorBottomFinal: { value: new THREE.Color().setHex(COLORS.PRM[1]) },
    uTransitionFinal: { value: 0 },
    uCurveAmountFinal: { value: 0.3 },
  }
  const final = {
    name: 'PRM', index: 'Final', top: uniforms.uColorTopFinal.value, bottom: uniforms.uColorBottomFinal.value,
    uTransition: uniforms.uTransitionFinal, uCurveAmount: uniforms.uCurveAmountFinal,
    get transition() { return this.uTransition.value },
  }
  const base = { name: 'LGH', top: uniforms.uColorTopInitial.value, bottom: uniforms.uColorBottomInitial.value, transition: 1 }
  let decl = ''
  let grad = ''
  // layers[k-1] ↔ uTransition{k}/uCurveAmount{k}
  const layers = layerNames.map((name, i) => {
    const k = i + 1
    const top = new THREE.Color(COLORS[name][0])
    const b = COLORS[name][1]
    const bottom = typeof b === 'number' ? new THREE.Color().setHex(b) : new THREE.Color(b)
    const L = {
      name, index: k, top, bottom,
      uTransition: { value: 0 }, uCurveAmount: { value: 0.3 },
      get transition() { return this.uTransition.value },
    }
    uniforms[`uColorTop${k}`] = { value: top }
    uniforms[`uColorBottom${k}`] = { value: bottom }
    uniforms[`uTransition${k}`] = L.uTransition
    uniforms[`uCurveAmount${k}`] = L.uCurveAmount
    decl += `uniform vec3 uColorTop${k};uniform vec3 uColorBottom${k};uniform float uTransition${k};uniform float uCurveAmount${k};\n`
    grad += `    baseGradient = mix(baseGradient, mix(linearToSrgb(uColorBottom${k}), linearToSrgb(uColorTop${k}), curvedScroll), computeCurvedLineMask(uTransition${k}, uCurveSharpness, uCurveAmount${k}, vUv.x, vUv.y));\n`
    return L
  })
  const material = new THREE.ShaderMaterial({
    uniforms, vertexShader: VERT, fragmentShader: FRAG_HEAD + decl + FRAG_BODY + grad + FRAG_TAIL,
    depthWrite: false, depthTest: false,
  })
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), material)
  mesh.frustumCulled = false
  mesh.renderOrder = -10
  mesh.name = 'BACKGROUND'

  // State stack exactly like BACKGROUND.#A/#M: later layers with ≥ transition drop the ones below them.
  function states() {
    const y = [base]
    for (const L of layers) {
      const t = L.uTransition.value
      if (!t) continue
      let r = y.length - 1
      do { if (y[r].transition > t) break } while (--r > -1)
      y.splice(r + 1, y.length, { name: L.name, top: L.top, bottom: L.bottom, transition: t })
    }
    const tf = final.uTransition.value
    if (tf) {
      let r = y.length - 1
      do { if (y[r].transition > tf) break } while (--r > -1)
      y.splice(r + 1, y.length, { name: final.name, top: final.top, bottom: final.bottom, transition: tf })
    }
    return y
  }
  return { mesh, material, uniforms, layers, final, base, states, tick(dt) { uniforms.uTime.value += dt } }
}
