# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from bananas.users.models import User
from django.utils.translation import ugettext_lazy as _


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


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
