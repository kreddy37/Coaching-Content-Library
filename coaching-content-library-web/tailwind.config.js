/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'hockey-blue': '#1e3a5f',
        'ice-blue': '#38bdf8',
        'glacier-white': '#f8fafc',
        'rink-gray': '#64748b',
        'youtube-red': '#ff0000',
        'reddit-orange': '#ff4500',
        'instagram-pink': '#e1306c',
        'tiktok-black': '#000000',
        'difficulty-beginner': '#22c55e',
        'difficulty-intermediate': '#f59e0b',
        'difficulty-advanced': '#ef4444',
        success: '#22c55e',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      fontFamily: {
        display: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 1px 3px rgba(30, 58, 95, 0.1)',
        'card-hover': '0 10px 30px rgba(30, 58, 95, 0.15)',
      }
    },
  },
  plugins: [],
}
