# Language Integration Guide

## Overview
This application supports multilingual content through Django's modeltranslation and Vue i18n integration.

## How It Works

### Backend (Django)
1. **Models**: `Author` and `Book` models have translatable fields defined in `translation.py`
   - Author: `first_name`, `last_name`, `bio`
   - Book: `title`, `description`

2. **Middleware**: `AcceptLanguageMiddleware` reads the `Accept-Language` header and activates the corresponding Django language

3. **Database**: Modeltranslation creates separate columns for each language:
   - `title_en`, `title_hi`, `title_ta`
   - `description_en`, `description_hi`, `description_ta`
   - etc.

4. **API Response**: The API returns the translated fields based on the active language

### Frontend (Vue/Quasar)
1. **Language Detection**: Current language is stored in localStorage and managed by Vue i18n

2. **API Headers**: The `Accept-Language` header is automatically set in axios requests

3. **Language Switching**: When language changes:
   - Vue i18n locale is updated
   - `Accept-Language` header is updated
   - Data is automatically refreshed to show translated content

## Testing Translation

### In Development
1. Use the language switcher in the UI
2. Check browser console for translation debug logs
3. Use the "Test Language Data" button (development only) to compare responses

### Manual API Testing
```bash
# Test English
curl -H "Accept-Language: en" http://localhost:8000/api/books/

# Test Hindi  
curl -H "Accept-Language: hi" http://localhost:8000/api/books/

# Test Tamil
curl -H "Accept-Language: ta" http://localhost:8000/api/books/
```

## Expected Behavior
- When you switch languages, book titles and descriptions should change
- Author names should also change if translated data exists
- If no translation exists for a field, it falls back to English
- The UI language (buttons, labels) changes immediately
- The data language changes after the API refresh

## Troubleshooting
1. **Data not changing**: Check browser console for API request headers
2. **Missing translations**: Verify database has translated content
3. **UI not updating**: Ensure language watcher is working in components

## Adding New Translatable Fields
1. Add field to `translation.py`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update serializers if needed
4. Add translated content to database