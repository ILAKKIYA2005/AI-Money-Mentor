/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neonBlue: "#00f3ff",
        neonPurple: "#bc13fe",
        neonPink: "#ff00ff",
        darkBg: "#010101",
        cardBg: "rgba(255, 255, 255, 0.05)",
      },
      boxShadow: {
        neonBlue: "0 0 10px #00f3ff, 0 0 20px #00f3ff",
        neonPurple: "0 0 10px #bc13fe, 0 0 20px #bc13fe",
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
