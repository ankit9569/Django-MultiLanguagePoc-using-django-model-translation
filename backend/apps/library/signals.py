"""
Signals to auto-translate new or updated content into hi/ta using deep-translator.

Runs only on save (create/update) — never on every request.
Fills *_hi and *_ta from *_en when missing.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Author, Book
from .services.auto_translate import fill_missing_translations


@receiver(post_save, sender=Author)
def author_auto_translate(sender, instance, created, **kwargs):
    """After Author save, fill first_name_hi/ta, last_name_hi/ta, bio_hi/ta from _en if empty."""
    fields_with_en = [
        ('first_name', getattr(instance, 'first_name_en', None) or instance.first_name),
        ('last_name', getattr(instance, 'last_name_en', None) or instance.last_name),
        ('bio', getattr(instance, 'bio_en', None) or instance.bio),
    ]
    fill_missing_translations(instance, [(n, v) for n, v in fields_with_en if v])


@receiver(post_save, sender=Book)
def book_auto_translate(sender, instance, created, **kwargs):
    """After Book save, fill title_hi/ta, description_hi/ta from _en if empty."""
    fields_with_en = [
        ('title', getattr(instance, 'title_en', None) or instance.title),
        ('description', getattr(instance, 'description_en', None) or instance.description),
    ]
    fill_missing_translations(instance, [(n, v) for n, v in fields_with_en if v])
