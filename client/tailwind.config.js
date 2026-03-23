/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        fighter: {
          primary: '#e63946',
          secondary: '#f4a261',
          bg: '#0d0d0d',
          surface: '#1a1a1a',
          border: '#3d1515',
          text: '#ffd6d6',
        },
        sentinel: {
          primary: '#0077b6',
          secondary: '#00b4d8',
          bg: '#050d1a',
          surface: '#0a1628',
          border: '#0d2d4a',
          text: '#cce8ff',
        },
        arena: {
          gold: '#ffd700',
          silver: '#c0c0c0',
          bronze: '#cd7f32',
        },
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Fira Code', 'monospace'],
        display: ['"Rajdhani"', 'Oswald', 'sans-serif'],
      },
      animation: {
        'rank-up': 'rankUp 0.8s ease-out',
        'pulse-glow': 'pulseGlow 2s infinite',
        'fade-in': 'fadeIn 0.3s ease-in',
      },
      keyframes: {
        rankUp: {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '50%': { transform: 'scale(1.2)', opacity: '0.8' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(230,57,70,0.5)' },
          '50%': { boxShadow: '0 0 20px rgba(230,57,70,0.9)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
