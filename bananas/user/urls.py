# -*- coding: utf-8 -*-
from django.conf.urls import url

from bananas.user import views

urlpatterns = [
    url(
        regex=r'^counselor-autocomplete/$',
        view=views.CounselorAutocomplete.as_view(),
        name='counselor-autocomplete',
    ),
]
