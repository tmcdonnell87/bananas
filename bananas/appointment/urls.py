# -*- coding: utf-8 -*-
from django.conf.urls import url

from bananas.appointment import views


urlpatterns = [
    url(
        regex=r'^appointment-autocomplete/$',
        view=views.AppointmentAutocomplete.as_view(),
        name='appointment-autocomplete',
    ),
    url(
        regex=r'^appointment-type-autocomplete/$',
        view=views.AppointmentTypeAutocomplete.as_view(),
        name='appointment-type-autocomplete',
    ),
]
