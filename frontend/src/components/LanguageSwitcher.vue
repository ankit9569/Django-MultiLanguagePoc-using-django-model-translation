<!-- <template>
  <q-select
  v-model="$i18n.locale"
  :options="[
    { label: 'English', value: 'en' },
    { label: 'हिंदी', value: 'hi' },
    { label: 'Français', value: 'fr' }
  ]"
  emit-value
  map-options
  dense
  outlined
  @update:model-value="onLangChange"
/>
</template>

<script>
import { i18n } from 'boot/i18n'
import { api } from 'boot/axios'

const onLangChange = (lang) => {
  localStorage.setItem('lang', lang)
  api.defaults.headers.common['Accept-Language'] = lang
}

</script>

<style>

</style> -->



<template>
  <q-select
    :model-value="locale"
    :options="languageOptions"
    option-value="value"
    option-label="label"
    emit-value
    map-options
    dense
    outlined
    @update:model-value="onLangChange"
  />
</template>

<script>
import { api } from 'boot/axios'
import { useI18n } from 'vue-i18n'

export default {
  name: 'LanguageSwitcher',

  setup() {
    const { locale } = useI18n()
    const languageOptions = [
    { label: 'English', value: 'en' },
    { label: 'हिंदी', value: 'hi' },
    { label: 'தமிழ்', value: 'ta' },
    ]

    const onLangChange = (lang) => {
      locale.value = lang
      localStorage.setItem('lang', lang)
      api.defaults.headers.common['Accept-Language'] = lang
    }

    return {
      locale,
      languageOptions,
      onLangChange
    }
  }
}
</script>
