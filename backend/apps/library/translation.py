"""
django-modeltranslation registration for the library app.

Registers which model fields are translatable. Modeltranslation will create
*_en, *_hi, *_ta columns for each registered field. The original field name
(e.g. title) becomes a virtual field that returns the value for the active
language (set by Accept-Language middleware).
"""
from modeltranslation.translator import TranslationOptions, register
from .models import Author, Book


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'bio')
    required_languages = ('en',)  # Only English is required; hi/ta can be empty (fallback to en)


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('en',)
