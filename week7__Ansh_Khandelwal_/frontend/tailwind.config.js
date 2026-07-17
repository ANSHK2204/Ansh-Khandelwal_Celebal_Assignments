/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brandDark: "#0c1020",
        brandDarker: "#060913",
        glassBg: "rgba(13, 20, 38, 0.65)",
        glassBorder: "rgba(255, 255, 255, 0.06)",
        accentBlue: "#3b82f6",
        accentCyan: "#06b6d4",
        accentPurple: "#8b5cf6",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      }
    },
  },
  plugins: [],
}
