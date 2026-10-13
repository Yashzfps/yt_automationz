import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        surface: '#0A0F1E',
        panel: '#131D36',
        accent: '#7C3AED',
      },
    },
  },
  plugins: [],
} satisfies Config;
