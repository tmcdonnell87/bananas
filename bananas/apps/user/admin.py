# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from bananas.apps.user.forms import MyUserChangeForm
from bananas.apps.user.forms import MyUserCreationForm
from bananas.apps.user.models import User


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = (
        'first_name',
        'last_name',
        'username',
        'email',
        'phone',
        'is_counselor',
        'is_superuser',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
    )
    list_filter = ('is_superuser', 'is_counselor')
    fieldsets = (
        ('Login Info', {
            'fields': (
                'username',
                'password',
            ),
        }),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'last_name',
                'is_counselor',
                'is_superuser',
            ),
        }),
        (_('Contact Info'), {
            'fields': (
                'phone',
                'email',
            ),
        }),
    )
    add_fieldsets = (
        ('Login Info', {
            'fields': (
                'username',
                'password1',
                'password2',
            ),
        }),
        (_('Personal Info'), {
            'fields': (
                'first_name',
                'last_name',
                'is_counselor',
                'is_superuser',
            ),
        }),
        (_('Contact Info'), {
            'fields': (
                'phone',
                'email',
            ),
        }),
    )
