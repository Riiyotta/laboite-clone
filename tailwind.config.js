/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        lgh1: '#ffffff', drk1: '#120042', gry1: '#cecece', gry2: '#aca6bd', gry3: '#5f5f5f',
        prm1: '#6630ff', scd1: '#01daf6', scd2: '#ff61f8', scd3: '#62f740', trt1: '#29daff', trt3: '#70f74a', err1: '#d00000',
      },
      fontFamily: { inter: ['vInter', 'sans-serif', 'arial'], screamer: ['FKScreamer', 'sans-serif'] },
    },
  },
  plugins: [],
}
