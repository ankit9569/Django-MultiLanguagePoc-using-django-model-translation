"""
One-time (or on-demand) backfill of hi/ta translations for existing records.

Uses deep-translator to fill *_hi and *_ta from *_en where empty.
Run after migration: python manage.py backfill_translations
"""
from django.core.management.base import BaseCommand

from apps.library.models import Author, Book
from apps.library.services.auto_translate import fill_missing_translations


class Command(BaseCommand):
    help = 'Backfill Hindi and Tamil translations from English for existing Authors and Books.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only show what would be translated, do not save.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write('Dry run — no changes will be saved.')

        count_a, count_b = 0, 0

        for author in Author.objects.all():
            fields_with_en = [
                ('first_name', getattr(author, 'first_name_en', None) or author.first_name),
                ('last_name', getattr(author, 'last_name_en', None) or author.last_name),
                ('bio', getattr(author, 'bio_en', None) or author.bio),
            ]
            to_fill = [(n, v) for n, v in fields_with_en if v]
            if to_fill:
                if not dry_run:
                    fill_missing_translations(author, to_fill)
                count_a += 1

        for book in Book.objects.all():
            fields_with_en = [
                ('title', getattr(book, 'title_en', None) or book.title),
                ('description', getattr(book, 'description_en', None) or book.description),
            ]
            to_fill = [(n, v) for n, v in fields_with_en if v]
            if to_fill:
                if not dry_run:
                    fill_missing_translations(book, to_fill)
                count_b += 1

        self.stdout.write(self.style.SUCCESS(
            f'Processed Authors: {count_a}, Books: {count_b}' + (' (dry run)' if dry_run else '')
        ))
