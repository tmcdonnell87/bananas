import json

from dal import autocomplete
from django import http

from bananas.apps.translation.utils import get_languages


class LanguageAutocomplete(autocomplete.Select2ListView):

    def get(self, request, *args, **kwargs):
        """"Return option list json response."""
        languages = get_languages()
        if self.q:
            languages = [lang for lang in languages if
                         self.q.lower() in lang['name'].lower()]
        return http.HttpResponse(json.dumps({
            'results': [dict(id=lang['language'], text=lang['name']) for
                        lang in languages]
        }))
