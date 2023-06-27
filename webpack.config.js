const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

let core = {
  mode: "development",
  watch: true,
  entry: {
    // hanya untuk mengisi entry sehingga copy plugin dapat dieksekusi
    'js/utility/empty.js': './core/resources/js/utility/empty.js',
  },
  output: {
    filename: '[name]',
    path: path.resolve(__dirname, './static/core/'),
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        // bootstrap
        { from: './node_modules/bootstrap/dist/css/bootstrap.min.css', to: './vendors/bootstrap/bootstrap.min.css' },
        { from: './node_modules/bootstrap/dist/css/bootstrap.min.css.map', to: './vendors/bootstrap/bootstrap.min.css.map' },
        { from: './node_modules/bootstrap/dist/js/bootstrap.bundle.min.js', to: './vendors/bootstrap/bootstrap.bundle.min.js' },
        { from: './node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map', to: './vendors/bootstrap/bootstrap.bundle.min.js.map' },
        // bootstrap icon
        { from: './node_modules/bootstrap-icons/font/bootstrap-icons.css', to: './vendors/bootstrap-icons/bootstrap-icons.css' },
        { from: './node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff', to: './vendors/bootstrap-icons/fonts/bootstrap-icons.woff' },
        { from: './node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2', to: './vendors/bootstrap-icons/fonts/bootstrap-icons.woff2' },
        // chart.js
        { from: './node_modules/chart.js/dist/chart.min.js', to: './vendors/chart.js/chart.min.js' },
        // flatpickr
        { from: './node_modules/flatpickr/dist/flatpickr.min.css', to: './vendors/flatpickr/flatpickr.min.css' },
        { from: './node_modules/flatpickr/dist/flatpickr.min.js', to: './vendors/flatpickr/flatpickr.min.js' },
        { from: './node_modules/flatpickr/dist/plugins/monthSelect/style.css', to: './vendors/flatpickr/plugins/monthSelect/style.css' },
        // js-cookie
        { from: './node_modules/js-cookie/dist/js.cookie.js', to: './vendors/js-cookie/js.cookie.js' },
      ]
    })
  ]
}

module.exports = [
  core
]
