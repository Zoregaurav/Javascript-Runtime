import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        soil: "#5A3B20",
        leaf: "#0F6A3C",
        meadow: "#2EB872",
        limewash: "#EAF8DE",
        cream: "#FFF9EE"
      },
      fontFamily: {
        sans: ["var(--font-inter)", "ui-sans-serif", "system-ui"]
      },
      boxShadow: {
        premium: "0 28px 90px rgba(15, 106, 60, 0.18)",
        glow: "0 0 60px rgba(46, 184, 114, 0.34)"
      },
      backgroundImage: {
        "hero-radial": "radial-gradient(circle at top left, rgba(143, 232, 117, 0.5), transparent 35%), radial-gradient(circle at 80% 20%, rgba(15, 106, 60, 0.25), transparent 30%)"
      }
    }
  },
  plugins: []
};

export default config;
