const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  mode: 'jit',
  purge: ['./tracker_app/templates/*.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: 'Inter var',
        ...defaultTheme.fontFamily.sans,
        display: 'Gilroy'
      }
    }
  },
  variants: {},
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/typography')
  ]
}
