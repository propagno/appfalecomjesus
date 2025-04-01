/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Tons de azul, dourado, bege e outras cores que evocam paz e espiritualidade
        spirit: {
          // Azul marinho profundo - principal
          blue: {
            50: '#edf2f7',
            100: '#e2e8f0',
            200: '#c3cfe0',
            300: '#a4b6d3',
            400: '#6582b5',
            500: '#3d6491',
            600: '#1a365d', // Azul principal
            700: '#14294a',
            800: '#0f1f3a',
            900: '#0a172a',
          },
          // Tons de dourado
          gold: {
            50: '#f7f2e5',
            100: '#f1e5c0',
            200: '#e6d29b',
            300: '#d4b978',
            400: '#c9a55c', // Dourado principal
            500: '#b7923e',
            600: '#9c7b33',
            700: '#7d632a',
            800: '#584618',
            900: '#443511',
          },
          // Tons terrosos suaves
          earth: {
            50: '#f8f5f0',
            100: '#e8ded0',
            200: '#d7c8b0',
            300: '#c5b190',
            400: '#b39970',
            500: '#9e8052',
            600: '#876b43',
            700: '#6b5635',
            800: '#4e3f26',
            900: '#332a19',
          },
          // Vermelho suave para avisos
          red: {
            400: '#c86647',
            500: '#b24a24',
            600: '#933a16',
          },
          // Verde para mensagens positivas
          green: {
            400: '#4d9093',
            500: '#3c6e71',
            600: '#2c5456',
          },
        },
        // Mantém as cores primary e secondary originais para compatibilidade
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      fontFamily: {
        sans: ['Montserrat', 'Inter', 'sans-serif'],
        serif: ['Lora', 'Merriweather', 'serif'],
        // Fontes específicas para o app
        heading: ['Montserrat', 'sans-serif'],
        body: ['Lora', 'serif'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      // Sombras suaves
      boxShadow: {
        'spirit': '0 4px 14px 0 rgba(26, 54, 93, 0.1)',
        'spirit-md': '0 6px 16px 0 rgba(26, 54, 93, 0.12)',
        'spirit-lg': '0 10px 25px 0 rgba(26, 54, 93, 0.15)',
      },
      // Gradientes
      backgroundImage: {
        'gradient-spirit': 'linear-gradient(to right, #1a365d, #3d6491)',
        'gradient-gold': 'linear-gradient(to right, #c9a55c, #d4b978)',
      },
    },
  },
  plugins: [],
} 