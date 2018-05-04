# -*- coding: utf-8 -*-
from django.conf.urls import url

from bananas.apps.translation import views


urlpatterns = [
    url(
        regex=r'^language-autocomplete/$',
        view=views.LanguageAutocomplete.as_view(),
        name='language-autocomplete',
    ),
]
