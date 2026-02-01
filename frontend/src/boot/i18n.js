import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'
import { api } from './axios'

const locale = localStorage.getItem('lang') || 'en'

const i18n = createI18n({
  legacy: false,
  locale,
  fallbackLocale: 'en',
  messages,
  globalInjection: true
})

api.defaults.headers.common['Accept-Language'] = locale

export default ({ app }) => {
  app.use(i18n)
}

export { i18n }
