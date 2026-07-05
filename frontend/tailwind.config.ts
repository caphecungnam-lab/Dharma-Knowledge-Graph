import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./store/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#05070b",
        panel: "#0d121a",
        line: "#1f2a38",
        mist: "#93a4b8",
        lotus: "#e3c770",
        core: "#6ee7b7",
        doctrinal: "#60a5fa",
        interpretive: "#c4b5fd",
        esoteric: "#f0abfc",
        unknown: "#64748b"
      },
      boxShadow: {
        glow: "0 0 28px rgba(110, 231, 183, 0.25)",
        violet: "0 0 26px rgba(240, 171, 252, 0.22)"
      }
    }
  },
  plugins: []
};

export default config;
