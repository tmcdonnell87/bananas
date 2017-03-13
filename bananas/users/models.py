# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from bananas.appointments.models import Appointment
from bananas.appointments.models import ScheduledMessage

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


@receiver(post_save, sender=User)
def set_default_user_permissions(sender, instance, created, **kwargs):
    """ Set Default permissions for new users """
    if created:
            permissions = (
                list(Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(Appointment)
                )) +
                list(Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(ScheduledMessage)
                ))
            )
            for permission in permissions:
                instance.user_permissions.add(permission)

            instance.is_staff = True
            instance.save()
