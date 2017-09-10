from googleapiclient.discovery import build

from django.conf import settings


service = build('translate', 'v2', developerKey=settings.GOOGLE_KEY)


def get_languages():
    return service.languages().list(
        target='en'
    ).execute()['languages']


def translate_text(text, language):
    return service.translations().list(
        source='en',
        target=language,
        format='text',
        q=text
    ).execute()['translations'][0]['translatedText']
