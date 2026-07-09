import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}'
  ],
  darkMode: ['class'],
  theme: {
    extend: {
      boxShadow: {
        soft: '0 20px 45px rgba(15, 23, 42, 0.12)'
      },
      backgroundImage: {
        'hero-pattern': 'radial-gradient(circle at top, rgba(96, 165, 250, 0.16), transparent 40%)'
      }
    }
  },
  plugins: []
};

export default config;
