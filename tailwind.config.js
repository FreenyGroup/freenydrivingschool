/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/**/**/*.html',
    './templates/**/**/**/*.html',
    '*.html',
    '/*.html',
    '/templates/**/*.html',
    '/templates/**/**/*.html',
    '/templates/**/**/**/*.html',
    'templates/**/*.html',
    'templates/**/**/*.html',
    'templates/**/**/**/*.html',
    '**/*.html',
    '**/**/*.html',
    '**/**/**/*.html',
    './**/templates/**/*.html',
    "./node_modules/flowbite/**/*.js",
  ],
  safelist: [
    "active",
    "w-64",
    "w-1/2",
    "rounded-l-lg",
    "rounded-r-lg",
    "bg-gray-200",
    "grid-cols-4",
    "grid-cols-7",
    "h-6",
    "leading-6",
    "h-9",
    "leading-9",
    "shadow-lg",
    "bg-opacity-50"
  ],
  theme: {
    fontFamily: {
      header: ["Lobster Two", "cursive"],
      body: ["Montserrat", "sans-serif"],
    },
    screens: {
      '-sm': { max: '639px'},
      '-md': { max: '767px'},
      '-lg': { max: '1023px'},
      xs: "375px",
      ...defaultTheme.screens,
    },
    colors: {
      transparent: "transparent",
      primary: "#E6A14A",
      secondary: "#8B283E",
      "blue-light": "#d7f5f6",
      blue: "#327C8F",
      orange: "#F49121",
      yellow: "#E6A14A",
      purple: "#560bad",
      neutrals: {
        l00: "#fafafa",
        l01: "#f5f5f5",
        l02: "#f3f3f3",
        l03: "#f1f1f1", //grey-lightest
        g01: "#d0d0d0", //grey-lighter
        g02: "#a2a2a2", //grey-light
        g03: "#5b5b5b", //grey
      },
      'tahiti': {
        100: '#cffafe',
        200: '#a5f3fc',
        300: '#67e8f9',
        400: '#22d3ee',
        500: '#06b6d4',
        600: '#0891b2',
        700: '#0e7490',
        800: '#155e75',
        900: '#164e63',
      },
      white: "#ffffff",
      black: "#000000",
    },
    container: {
      center: true,
      padding: "1rem",
    },
    minHeight: {
      0: "0px",
      full: "100%",
      screen: "100vh",
      "screen-30": "30vh",
      "screen-40": "40vh",
      "screen-45": "45vh",
      "screen-50": "50vh",
      "screen-60": "60vh",
      "screen-70": "70vh",
      "screen-80": "80vh",
      "screen-85": "85vh",
      "screen-90": "90vh",
    },
    extend: {
      flexGrow: {
        '5' : '5'
      },
      spacing: {
        68: "17rem",
        76: "19rem",
        84: "21rem",
        100: "25rem",
        108: "27rem",
        120: "30rem",
        124: "31rem",
        128: "32rem",
        132: "33rem",
        140: "35rem",
        144: "36rem",
        160: "40rem",
        232: "58rem",
      },

      width: {
        "7/25": "28%",
      },

      zIndex: {
        "-1": "-1",
      },

      transitionProperty: {
        width: "width"
      },
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("flowbite/plugin"),
    require('flowbite-typography'),
  ],
}
