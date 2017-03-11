# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    phone = models.CharField(_('Phone Number'), blank=True, max_length=16)

    def __str__(self):
        return "{} {} ({})".format(
            self.first_name, self.last_name, self.username)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
