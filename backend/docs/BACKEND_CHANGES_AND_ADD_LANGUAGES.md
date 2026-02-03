# Backend Changes: Multilingual API (What Changed & Why)

This document lists **every change** made to the backend for multilingual support and **why** each change was made. At the end, you will find **how to add more languages** (e.g. Bengali, Telugu, Spanish).

For concepts (what modeltranslation vs deep-translator do, flow, migration strategy), see **[TRANSLATION_GUIDE.md](../TRANSLATION_GUIDE.md)** in the backend root.

---

## Table of contents

1. [Summary of changes](#1-summary-of-changes)
2. [File-by-file changes and reasons](#2-file-by-file-changes-and-reasons)
3. [How to add more languages](#3-how-to-add-more-languages)

---

## 1. Summary of changes

| Area | What changed |
|------|----------------|
| **Dependencies** | Added `django-modeltranslation` and `deep-translator` |
| **Settings** | New app, middleware, language/fallback config, auto-translate flag |
| **New files** | `config/middleware.py`, `apps/library/translation.py`, `apps/library/services/auto_translate.py`, `apps/library/signals.py`, migration `0002_...`, management command `backfill_translations` |
| **Modified files** | `apps/library/apps.py` (signals import), migration `0002` (data copy step) |
| **Unchanged** | Models, serializers, views, URLs — no changes |

---

## 2. File-by-file changes and reasons

### 2.1 `requirements.txt`

**What changed**

- Added:
  - `django-modeltranslation==0.18.11`
  - `deep-translator==1.11.4`

**Why**

- **django-modeltranslation**: Adds per-language database columns (`*_en`, `*_hi`, `*_ta`) and makes the “virtual” field (e.g. `title`) return the value for the **active language**. It does **not** call any translation API.
- **deep-translator**: Used to **generate** Hindi/Tamil (or other languages) from English when saving or when running the backfill command. It is used only on save or in the backfill, never on every API request.

---

### 2.2 `config/settings.py`

**What changed**

1. **INSTALLED_APPS**
   - Added `'modeltranslation'` in `THIRD_PARTY_APPS` **before** `'apps.library'`.

2. **MIDDLEWARE**
   - Added `'django.middleware.locale.LocaleMiddleware'` (so `translation.activate()` is available).
   - Added `'config.middleware.AcceptLanguageMiddleware'` after `LocaleMiddleware`.

3. **Internationalization**
   - `LANGUAGE_CODE = 'en'`.
   - Added `LANGUAGES = [('en', 'English'), ('hi', 'Hindi'), ('ta', 'Tamil')]`.
   - Added:
     - `MODELTRANSLATION_LANGUAGES = ('en', 'hi', 'ta')`
     - `MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'`
     - `MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'hi', 'ta')`

4. **New setting**
   - `AUTO_TRANSLATE_ENABLED = config('AUTO_TRANSLATE_ENABLED', default=True, cast=bool)`.

**Why**

- **modeltranslation before library**: The library app’s `translation.py` registers models with modeltranslation; the app must be loaded **after** `modeltranslation` so that registration runs correctly.
- **LocaleMiddleware**: Required so Django’s translation system (and thus modeltranslation) can switch language per request.
- **AcceptLanguageMiddleware**: Reads the `Accept-Language` header and calls `translation.activate(lang)` so that API responses use the requested language. Without it, the API would always use the default language.
- **LANGUAGES / MODELTRANSLATION_***: Tell Django and modeltranslation which languages exist, which is default, and in which order to fall back when a translation is missing (so the API does not return empty strings).
- **AUTO_TRANSLATE_ENABLED**: Allows turning off deep-translator (e.g. in tests or when no API key) without code changes.

---

### 2.3 `config/middleware.py` (new file)

**What it does**

- Defines `SUPPORTED_LANGUAGES = {'en', 'hi', 'ta'}` and `DEFAULT_LANGUAGE = 'en'`.
- `parse_accept_language(header_value)`: Parses `Accept-Language` (e.g. `"hi-IN,hi;q=0.9,en;q=0.8"`) and returns the first **supported** language code (`en`, `hi`, or `ta`), or `None`.
- `AcceptLanguageMiddleware`: For each request, gets `Accept-Language` from `request.META`, parses it, calls `translation.activate(lang)` (or default), calls the view, then `translation.deactivate()`.

**Why**

- The API must respond in the language the client asks for. The standard way to ask is the `Accept-Language` header. This middleware is the only place we set the active language from that header, so modeltranslation and serializers automatically serve the right language without changing views or serializers.

---

### 2.4 `apps/library/translation.py` (new file)

**What it does**

- Imports `TranslationOptions` and `register` from `modeltranslation.translator`.
- Registers **Author** with translatable fields: `first_name`, `last_name`, `bio`.
- Registers **Book** with translatable fields: `title`, `description`.
- Sets `required_languages = ('en',)` so only English is required; other languages can be empty (fallback will use English).

**Why**

- django-modeltranslation only creates and manages language columns for **registered** models and fields. This file is the single place where we declare which models and which fields get `*_en`, `*_hi`, `*_ta` (and any future language codes). Without registration, no extra columns are added and no language switching happens for those fields.

---

### 2.5 `apps/library/migrations/0002_author_bio_en_author_bio_hi_author_bio_ta_and_more.py`

**What changed**

- **Generated part**: Migration that adds all new language columns:
  - Author: `first_name_en/hi/ta`, `last_name_en/hi/ta`, `bio_en/hi/ta`.
  - Book: `title_en/hi/ta`, `description_en/hi/ta`.
- **Added by us**: A **RunPython** step that runs **after** these columns are added:
  - For each **Author**: if `first_name_en` is empty and `first_name` has a value, set `first_name_en = first_name` (and same for `last_name`, `bio`).
  - For each **Book**: if `title_en` is empty and `title` has a value, set `title_en = title` (and same for `description`).
  - Reverse operation is a no-op.

**Why**

- Existing data lived in the **original** columns (`first_name`, `title`, etc.). Modeltranslation uses the **new** columns (`*_en`, `*_hi`, `*_ta`). If we did not copy old data into `*_en`, all existing content would appear “lost” after the migration. This RunPython step ensures **no English data is lost** and keeps the migration safe for production.

---

### 2.6 `apps/library/services/auto_translate.py` (new file)

**What it does**

- Reads `AUTO_TRANSLATE_ENABLED` from settings (default `True`).
- Defines `SUPPORTED_TARGETS = {'hi', 'ta'}` and `SOURCE_LANG = 'en'`.
- `translate_text(text, target_lang, source_lang)`: Uses `deep_translator.GoogleTranslator` to translate a string from `source_lang` to `target_lang`; returns the original text on failure and logs a warning.
- `fill_missing_translations(instance, field_names_with_en)`: For each `(field_base_name, value_en)` (e.g. `('title', 'Emma')`), for each target language in `SUPPORTED_TARGETS`, if the corresponding `*_hi` or `*_ta` attribute is empty, calls `translate_text` and updates the instance in the DB with `Model.objects.filter(pk=...).update(...)` (so no extra `save()` and no signal loop).

**Why**

- We want new or updated records to get Hindi/Tamil **automatically** from English, but **only when saving**, not on every API read. This module centralizes that logic and uses `update()` to avoid recursive saves.

---

### 2.7 `apps/library/signals.py` (new file)

**What it does**

- Connects **post_save** for **Author** and **Book**.
- For **Author**: Collects `(first_name, first_name_en or first_name)`, same for `last_name`, `bio`; calls `fill_missing_translations(instance, ...)` so missing `*_hi` and `*_ta` are filled from English.
- For **Book**: Same idea for `title` and `description`.

**Why**

- So that whenever an Author or Book is created or updated, any missing Hindi/Tamil (or other target languages) are filled once from English via deep-translator, without touching views or serializers.

---

### 2.8 `apps/library/apps.py`

**What changed**

- Added:
  ```python
  def ready(self):
      import apps.library.signals  # noqa: F401 — register post_save auto-translate
  ```

**Why**

- Django only runs signal handlers if the module that connects them is loaded. Importing `signals` in `ready()` ensures the `post_save` handlers for Author and Book are registered when the app starts.

---

### 2.9 `apps/library/management/commands/backfill_translations.py` (new file)

**What it does**

- Management command: `python manage.py backfill_translations`.
- Option: `--dry-run` (only count, do not save).
- For every **Author** and **Book**, builds the same list of `(field_base_name, value_en)` as in signals and calls `fill_missing_translations`. So all existing records get their missing `*_hi` and `*_ta` filled from `*_en`.

**Why**

- The migration only copies **existing** data into `*_en`. It does **not** fill `*_hi` or `*_ta`. So after the migration, Hindi/Tamil columns are empty until we either run this command or create/update records (which trigger the signals). This command is the one-time (or on-demand) way to backfill Hindi/Tamil for all existing data.

---

### 2.10 What was **not** changed

- **Models** (`models.py`): No changes. Modeltranslation works by adding columns and overriding field access; the model class still has `title`, `first_name`, etc.
- **Serializers**: No changes. They keep using `title`, `first_name`, etc.; modeltranslation makes those return the active language.
- **Views / ViewSets**: No changes.
- **URLs**: No changes.
- **Admin**: No changes required; modeltranslation adds language tabs automatically for registered fields.

---

## 3. How to add more languages

Example: add **Bengali (bn)** and **Telugu (te)** so the API supports `en`, `hi`, `ta`, `bn`, `te`.

### Step 1: Settings — add the new language codes

**File: `config/settings.py`**

- In **LANGUAGES**, add the new entries:
  ```python
  LANGUAGES = [
      ('en', 'English'),
      ('hi', 'Hindi'),
      ('ta', 'Tamil'),
      ('bn', 'Bengali'),   # add
      ('te', 'Telugu'),    # add
  ]
  ```
- In **MODELTRANSLATION_LANGUAGES**, add the new codes:
  ```python
  MODELTRANSLATION_LANGUAGES = ('en', 'hi', 'ta', 'bn', 'te')
  ```
- In **MODELTRANSLATION_FALLBACK_LANGUAGES**, add them (order = fallback order when a value is missing):
  ```python
  MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'hi', 'ta', 'bn', 'te')
  ```

**Why:** Django and modeltranslation need to know which languages exist and how to fall back.

---

### Step 2: Middleware — allow the new codes in Accept-Language

**File: `config/middleware.py`**

- Update **SUPPORTED_LANGUAGES** so the new codes are accepted from the header:
  ```python
  SUPPORTED_LANGUAGES = {'en', 'hi', 'ta', 'bn', 'te'}
  ```

**Why:** So a client can send `Accept-Language: bn` or `Accept-Language: te` and get Bengali or Telugu responses.

---

### Step 3: Auto-translate service — translate into the new languages

**File: `apps/library/services/auto_translate.py`**

- Add the new codes to **SUPPORTED_TARGETS**:
  ```python
  SUPPORTED_TARGETS = {'hi', 'ta', 'bn', 'te'}
  ```

**Why:** So `fill_missing_translations` (used by signals and the backfill command) will fill `*_bn` and `*_te` from English as well.

---

### Step 4: Database — add new columns

Modeltranslation will add `*_bn` and `*_te` columns when you run migrations **after** updating `translation.py`. You do **not** edit `translation.py` to list languages; the languages come from **MODELTRANSLATION_LANGUAGES** in settings. So:

1. In **`config/settings.py`** you already added `'bn'` and `'te'` to `MODELTRANSLATION_LANGUAGES` (Step 1).
2. Run:
   ```bash
   python manage.py makemigrations library
   ```
   This should generate a new migration that adds `first_name_bn`, `first_name_te`, etc. for Author and Book.
3. Run:
   ```bash
   python manage.py migrate
   ```

**Why:** Each new language needs its own column per translatable field (e.g. `title_bn`, `title_te`). Modeltranslation generates that migration from `MODELTRANSLATION_LANGUAGES`.

---

### Step 5: Backfill existing data (optional)

To fill the new language columns for **existing** records from English:

```bash
python manage.py backfill_translations
```

The backfill uses `SUPPORTED_TARGETS` from `auto_translate.py`, so after Step 3 it will also fill `*_bn` and `*_te`. New saves will also fill them via the existing signals.

---

### Step 6: Frontend (if applicable)

- Add the new locale (e.g. `bn`, `te`) to your Vue/Quasar i18n setup.
- When calling the API, send the chosen language in the **Accept-Language** header (e.g. `Accept-Language: bn` or `te`).

---

### Checklist when adding a new language

| Step | File / Action | What to do |
|------|----------------|------------|
| 1 | `config/settings.py` | Add `('code', 'Name')` to `LANGUAGES`; add `'code'` to `MODELTRANSLATION_LANGUAGES` and `MODELTRANSLATION_FALLBACK_LANGUAGES`. |
| 2 | `config/middleware.py` | Add `'code'` to `SUPPORTED_LANGUAGES`. |
| 3 | `apps/library/services/auto_translate.py` | Add `'code'` to `SUPPORTED_TARGETS`. |
| 4 | Migrations | Run `makemigrations` then `migrate` so new `*_code` columns are created. |
| 5 | Backfill | Run `python manage.py backfill_translations` to fill new language for existing rows (optional). |
| 6 | Frontend | Add locale and send `Accept-Language: code` for API calls. |

---

### Supported language codes (deep-translator / Google)

Use codes that **Google Translate** supports (and thus deep-translator), e.g.:

- `en` (English), `hi` (Hindi), `ta` (Tamil), `bn` (Bengali), `te` (Telugu), `mr` (Marathi), `es` (Spanish), `fr` (French), `de` (German), `ja` (Japanese), etc.

If a code is not supported by the translator, `translate_text` will log a warning and return the original text; the rest of the flow still works.

---

This document and the steps above cover everything that was changed in the backend and how to add more languages in a consistent way.
