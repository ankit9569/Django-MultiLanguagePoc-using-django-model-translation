const { configure } = require('quasar/wrappers');

module.exports = configure(function (ctx) {
  return {
    eslint: {
      warnings: true,
      errors: true
    },

    boot: [
      'axios',
      'i18n'
    ],

    css: [
      'app.scss'
    ],

    extras: [
      'roboto-font',
      'material-icons',
    ],

    build: {
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node16'
      },

      vueRouterMode: 'hash',
    },

    devServer: {
      open: true,
      port: 9000,
    },

    framework: {
      config: {},
      plugins: [
        'Notify',
        'Dialog',
        'Loading'
      ]
    },

    animations: [],

    ssr: {
      pwa: false,
      prodPort: 3000,
      maxAge: 1000 * 60 * 60 * 24 * 30,
      middlewares: [
        ctx.prod ? 'compression' : '',
        'render'
      ]
    },

    pwa: {
      workboxPluginMode: 'GenerateSW',
      workboxOptions: {},
      manifest: {
        name: 'Library Management System',
        short_name: 'Library',
        description: 'A complete library management system',
        display: 'standalone',
        orientation: 'portrait',
        background_color: '#ffffff',
        theme_color: '#027be3',
        icons: [
          {
            src: 'icons/icon-128x128.png',
            sizes: '128x128',
            type: 'image/png'
          },
          {
            src: 'icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'icons/icon-256x256.png',
            sizes: '256x256',
            type: 'image/png'
          },
          {
            src: 'icons/icon-384x384.png',
            sizes: '384x384',
            type: 'image/png'
          },
          {
            src: 'icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    },

    cordova: {},

    capacitor: {
      hideSplashscreen: true
    },

    electron: {
      bundler: 'packager',
      packager: {},
      builder: {
        appId: 'library-frontend'
      }
    },

    bex: {
      contentScripts: [
        'my-content-script'
      ],
    }
  }
});