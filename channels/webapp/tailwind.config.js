/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#5D5CDE',
          50: '#F5F5FE',
          100: '#E9E9FC',
          200: '#D1D1F9',
          300: '#B8B8F7',
          400: '#7B7AE8',
          500: '#5D5CDE',
          600: '#3433D3',
          700: '#2928AB',
          800: '#1F1E80',
          900: '#151456',
        },
        green: {
          50: '#F3FAEB',
          100: '#E7F6D7',
          200: '#D0EDC0',
          300: '#B8E3A8',
          400: '#93D07F',
          500: '#5EAF48',
          600: '#47883B',
          700: '#376A2E',
          800: '#2C5525',
          900: '#1E3919',
        }
      }
    },
  },
  plugins: [],
}