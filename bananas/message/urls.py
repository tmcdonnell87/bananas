# -*- coding: utf-8 -*-
from django.conf.urls import url

from bananas.message import views


urlpatterns = [
    url(
        regex=r'^message-template-autocomplete/$',
        view=views.MessageTemplateAutocomplete.as_view(),
        name='message-template-autocomplete',
    ),
]
