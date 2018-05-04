from googleapiclient.discovery import build

from django.conf import settings


if settings.TRANSLATION_ACTIVE:
    service = build('translate', 'v2', developerKey=settings.GOOGLE_KEY)


def get_languages():
    if settings.TRANSLATION_ACTIVE:
        return service.languages().list(
            target='en'
        ).execute()['languages']
    return [{'language':'en', 'name':'English'}, ]


def translate_text(text, language):
    if settings.TRANSLATION_ACTIVE:
        return service.translations().list(
            source='en',
            target=language,
            format='text',
            q=text
        ).execute()['translations'][0]['translatedText']
    return text
