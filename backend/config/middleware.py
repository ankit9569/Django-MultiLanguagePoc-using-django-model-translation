"""
Middleware to set Django's active language from the Accept-Language header.

API responses then return translated fields (from django-modeltranslation)
according to the client's preferred language. No serializer or viewset changes
needed — the backend serves the right language automatically.
"""
from django.utils import translation

# Languages we support; first is default
SUPPORTED_LANGUAGES = {'en', 'hi', 'ta'}
DEFAULT_LANGUAGE = 'en'


def parse_accept_language(header_value):
    """
    Parse Accept-Language (e.g. "hi-IN,hi;q=0.9,en;q=0.8") and return
    the first matching supported language code or None.
    """
    if not header_value or not header_value.strip():
        return None
    for part in header_value.split(','):
        part = part.strip().split(';')[0].strip()
        if '-' in part:
            lang = part.split('-')[0].lower()
        else:
            lang = part.lower()
        if lang in SUPPORTED_LANGUAGES:
            return lang
    return None


class AcceptLanguageMiddleware:
    """
    Activate Django language from Accept-Language so modeltranslation
    and any gettext use the correct language for this request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = parse_accept_language(request.META.get('HTTP_ACCEPT_LANGUAGE', ''))
        if lang:
            translation.activate(lang)
        else:
            translation.activate(DEFAULT_LANGUAGE)
        response = self.get_response(request)
        translation.deactivate()
        return response
