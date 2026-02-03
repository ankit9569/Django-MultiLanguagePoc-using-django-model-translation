/**
 * Language utility functions for handling multilingual data
 */
import { api } from 'src/boot/axios'
import { useI18n } from 'vue-i18n'

/**
 * Get the current language code
 */
export function getCurrentLanguage() {
  const { locale } = useI18n()
  return locale.value
}

/**
 * Update the Accept-Language header for API requests
 */
export function updateApiLanguage(lang) {
  api.defaults.headers.common['Accept-Language'] = lang
}

/**
 * Get language display name
 */
export function getLanguageLabel(langCode) {
  const langMap = {
    'en': 'English',
    'hi': 'हिंदी', 
    'ta': 'தமிழ்'
  }
  return langMap[langCode] || langCode
}

/**
 * Make an API request with explicit language header
 */
export async function apiWithLanguage(url, options = {}, language = null) {
  const lang = language || getCurrentLanguage()
  const config = {
    ...options,
    headers: {
      ...options.headers,
      'Accept-Language': lang
    }
  }
  
  return api(url, config)
}

/**
 * Debug function to log API response data for translation verification
 */
export function logTranslationData(data, context = '') {
  if (process.env.NODE_ENV === 'development') {
    console.group(`🌐 Translation Data ${context}`)
    console.log('Current Language:', getCurrentLanguage())
    console.log('API Headers:', api.defaults.headers.common)
    console.log('Response Data:', data)
    console.groupEnd()
  }
}