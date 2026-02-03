"""
Auto-translate text from English to Hindi/Tamil using deep-translator.

Used only on save (or one-time migration) — never on every API request.
Fills *_hi and *_ta when *_en is set and the other is empty.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Optional: disable auto-translation via settings (e.g. in tests or if API key missing)
AUTO_TRANSLATE_ENABLED = getattr(settings, 'AUTO_TRANSLATE_ENABLED', True)

SUPPORTED_TARGETS = {'hi', 'ta'}
SOURCE_LANG = 'en'


def translate_text(text, target_lang, source_lang=SOURCE_LANG):
    """
    Translate a single string from source_lang to target_lang.
    Returns the translated string or the original on failure.
    """
    if not text or not text.strip():
        return text
    if target_lang not in SUPPORTED_TARGETS:
        return text
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        logger.warning('auto_translate failed for %s -> %s: %s', source_lang, target_lang, e)
        return text


def fill_missing_translations(instance, field_names_with_en):
    """
    For each (field_base_name, value_en), fill field_hi and field_ta if empty.
    field_names_with_en: list of (base_name, value_en) e.g. [('title', 'Hello'), ('description', '...')]
    Updates instance in DB with update() to avoid triggering save again.
    """
    if not AUTO_TRANSLATE_ENABLED:
        return
    model_class = instance.__class__
    updates = {}
    for base_name, value_en in field_names_with_en:
        if not value_en or not str(value_en).strip():
            continue
        for lang in SUPPORTED_TARGETS:
            attr = f'{base_name}_{lang}'
            if not hasattr(model_class, attr):
                continue
            current = getattr(instance, attr, None)
            if current and str(current).strip():
                continue
            translated = translate_text(str(value_en), lang)
            if translated:
                updates[attr] = translated
    if updates:
        model_class.objects.filter(pk=instance.pk).update(**updates)
        for k, v in updates.items():
            setattr(instance, k, v)
