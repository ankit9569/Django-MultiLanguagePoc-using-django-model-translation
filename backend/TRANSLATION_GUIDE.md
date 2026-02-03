# Multilingual API: django-modeltranslation + deep-translator

This guide explains how dynamic database content is translated and served by language, and how to run migrations and backfills safely.

---

## What django-modeltranslation does and does NOT do

### Does

- **Stores** multiple language values in the DB: for each registered field it adds columns `*_en`, `*_hi`, `*_ta`.
- **Serves** the right value by language: the original field name (e.g. `title`) becomes a *virtual* field that returns the value for Django’s **active language** (from `translation.get_language()`).
- **Fallback**: if the active language’s column is empty, it can fall back to another language (e.g. English) so the API never returns blank for that field.
- **Admin**: in Django admin you get one tab/field per language for translated fields.
- **No runtime translation**: it does **not** call any external API. It only reads/writes the columns that already exist.

### Does NOT

- **Translate** text from one language to another. It does not call Google Translate or any service.
- **Create** hi/ta content by itself. You must fill `*_hi` and `*_ta` yourself (e.g. with deep-translator on save or a one-time backfill).
- **Change** the active language per request. Something else (e.g. middleware reading `Accept-Language`) must call `translation.activate(lang)` so modeltranslation knows which column to use.

So: **modeltranslation = storage + “which column to read/write based on current language”.** It does not generate translations.

---

## What deep-translator does and does NOT do

### Does

- **Translates** text from one language to another using a provider (e.g. Google Translate).
- **Returns** a translated string. You decide where to store it (e.g. in `title_hi`, `title_ta`).

### Does NOT

- **Store** anything in the DB. It’s a pure function: text in → text out.
- **Know** about Django, modeltranslation, or the active language. It just translates a string.
- **Run** on every request in this setup. We use it only **on save** (signals) or in a **one-time backfill** command.

So: **deep-translator = “translate this string from en to hi/ta”.** Filling `*_hi` and `*_ta` is our responsibility.

---

## Why both are needed together

| Need | Who does it |
|------|-------------|
| Store en / hi / ta per field | django-modeltranslation (adds `*_en`, `*_hi`, `*_ta`) |
| Generate hi / ta from en | deep-translator (on save or backfill) |
| Serve the right language per request | Middleware sets `translation.activate(lang)` from `Accept-Language`; modeltranslation then returns the correct column |

- **Only modeltranslation**: you’d have to manually enter or import all hi/ta content.
- **Only deep-translator**: you’d have no place to store and serve per-language values, and you’d be tempted to translate on every request (slow, costly).
- **Both**: store languages in DB, auto-fill hi/ta from en on save (or once), and serve by `Accept-Language` with fallback — no frontend `$t()` needed for API data.

---

## Production-safe migration strategy for existing data

1. **Back up the database** before any migration.
2. **Add modeltranslation** (install app, `translation.py`, settings). Do **not** remove or rename existing columns in this step.
3. **Run `makemigrations`** so Django adds only the new `*_en`, `*_hi`, `*_ta` columns (and keep the existing `title`, `first_name`, etc. as they are in the migration that adds the new fields).
4. **Data migration**: in the same (or next) migration, run a `RunPython` that copies existing data into `*_en`:
   - `title` → `title_en`
   - `first_name` → `first_name_en`, `last_name` → `last_name_en`, `bio` → `bio_en`
   - `description` → `description_en`
   This preserves all existing English data.
5. **Apply migrations** (`migrate`). After this, `*_en` is populated; `*_hi` and `*_ta` can stay empty and fallback will use `*_en`.
6. **Optional one-time backfill**: run `python manage.py backfill_translations` to fill `*_hi` and `*_ta` from `*_en` using deep-translator. Can be run during low traffic or in a maintenance window; no need to run on every request.

Important: do **not** delete or drop the original columns until the copy into `*_en` is done and verified. This project’s migration copies in the same migration that adds the new fields, so no data is lost.

---

## Full flow: Frontend language → API header → Django → DB → response

1. **Frontend** (Vue/Quasar) sets the user’s language (e.g. `hi` or `ta`). When calling the API, it sends that in the **Accept-Language** header (e.g. `Accept-Language: hi` or `hi-IN,en;q=0.9`).
2. **Backend** middleware (`AcceptLanguageMiddleware`) reads `Accept-Language`, picks the first supported code (`en`, `hi`, `ta`), and calls **`translation.activate(lang)`** for that request.
3. **Django / modeltranslation**: for the rest of the request, `translation.get_language()` is that language. When the view/serializer accesses `book.title` or `author.first_name`, modeltranslation’s descriptor returns the value from `title_hi` / `first_name_hi` (or `_en`/`_ta` depending on active language). If that column is empty, fallback (e.g. to `en`) is used so the API doesn’t return blank.
4. **Database**: only stored columns are read (`*_en`, `*_hi`, `*_ta`). No translation is done in the DB.
5. **Response**: JSON contains the already-localized strings (e.g. Hindi title) because the serializer read `book.title` and got the active-language value. The frontend does **not** use `$t()` for these API fields; the backend is the single source of language for API data.

---

## translation.py setup

- **Location**: `apps/library/translation.py`
- **Role**: Register which models and fields get `*_en`, `*_hi`, `*_ta`.
- **Example** (already in the project):

```python
from modeltranslation.translator import TranslationOptions, register
from .models import Author, Book

@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'bio')
    required_languages = ('en',)

@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('en',)
```

After registration, modeltranslation adds the language columns and replaces the original field with a descriptor that uses the active language (and fallback).

---

## settings.py changes (languages + fallback)

- **`modeltranslation`** in `INSTALLED_APPS` (before `apps.library`).
- **`LANGUAGES`**: list of (`code`, `name`) for supported languages (`en`, `hi`, `ta`).
- **`MODELTRANSLATION_LANGUAGES`**: same codes, used by modeltranslation.
- **`MODELTRANSLATION_DEFAULT_LANGUAGE`**: e.g. `'en'`.
- **`MODELTRANSLATION_FALLBACK_LANGUAGES`**: e.g. `('en', 'hi', 'ta')` so missing hi/ta fall back to en and APIs don’t return empty.
- **Middleware**: `django.middleware.locale.LocaleMiddleware` and `config.middleware.AcceptLanguageMiddleware` so the active language is set from `Accept-Language`.

---

## One-time data migration strategy

1. **Migration 0002** (or equivalent) adds `*_en`, `*_hi`, `*_ta` and includes a **`RunPython`** that:
   - For each `Author`: set `first_name_en` from `first_name`, `last_name_en` from `last_name`, `bio_en` from `bio` (only where currently empty).
   - For each `Book`: set `title_en` from `title`, `description_en` from `description` (only where currently empty).
2. Run **`migrate`**. All existing content is now in `*_en`; English data is preserved.
3. (Optional) Run **`python manage.py backfill_translations`** to fill `*_hi` and `*_ta` from `*_en` using deep-translator. Use **`--dry-run`** first if you want to see what would be updated.

---

## Optional auto-translation for old data

- **On save**: post_save signals call a small helper that, for each translatable field, if `*_en` is set and `*_hi` or `*_ta` is empty, uses deep-translator to fill them and then **`Model.objects.filter(pk=...).update(...)`** so no extra save is triggered.
- **One-time**: use **`python manage.py backfill_translations`** to backfill hi/ta for all existing records. Disable auto-translate in tests with **`AUTO_TRANSLATE_ENABLED = False`** (or env) if needed.

---

## Common mistakes to avoid

1. **Translating on every request**  
   Use deep-translator only in save (signals) or in the backfill command, never in views/serializers on read.

2. **Removing original columns before copying to *_en**  
   Always copy existing data into `*_en` in a migration before dropping or reusing the original column.

3. **Relying on frontend `$t()` for API payloads**  
   Backend should return the correct language in the JSON; frontend sends `Accept-Language` and displays the API values as-is.

4. **Forgetting fallback**  
   Set `MODELTRANSLATION_FALLBACK_LANGUAGES` so empty hi/ta columns don’t result in blank strings in responses.

5. **Putting `modeltranslation` after your app in `INSTALLED_APPS`**  
   It must be listed **before** any app that uses it (e.g. before `apps.library`).

6. **Not activating language per request**  
   Without middleware (or equivalent) that sets `translation.activate(lang)` from `Accept-Language`, modeltranslation will always use the default language.

7. **Running backfill in a tight loop without rate limiting**  
   deep-translator calls an external API; run backfill in batches or during off-peak if you have many rows.

8. **Assuming modeltranslation “translates”**  
   It only stores and serves; you must fill `*_hi` and `*_ta` (e.g. with deep-translator) if you want them populated.

---

## Files touched in this project

| File | Purpose |
|------|--------|
| `requirements.txt` | Added `django-modeltranslation`, `deep-translator` |
| `config/settings.py` | modeltranslation config, LANGUAGES, fallback, middleware, `AUTO_TRANSLATE_ENABLED` |
| `config/middleware.py` | `AcceptLanguageMiddleware`: set language from `Accept-Language` |
| `apps/library/translation.py` | Register Author and Book translated fields |
| `apps/library/migrations/0002_...` | Add `*_en`/`*_hi`/`*_ta` + RunPython copy to `*_en` |
| `apps/library/services/auto_translate.py` | deep-translator wrapper; fill missing hi/ta from en |
| `apps/library/signals.py` | post_save auto-translate for Author and Book |
| `apps/library/apps.py` | `ready()` imports signals |
| `apps/library/management/commands/backfill_translations.py` | One-time backfill hi/ta from en |

Serializers and views remain unchanged; they still use `title`, `first_name`, etc., and modeltranslation serves the correct language for the active request.
