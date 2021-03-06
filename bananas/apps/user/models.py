# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from bananas.apps.appointment.models import Appointment
from bananas.apps.message.models import ScheduledMessage
from bananas.utils.model_mixins import BaseModel


@python_2_unicode_compatible
class User(BaseModel, AbstractUser):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    email = models.CharField(max_length=255, blank=False, unique=True)
    phone = models.CharField(_('Phone Number'), max_length=40, blank=False)
    is_counselor = models.BooleanField(
        _('Counselor'), default=True,
        help_text='Counselors can be assigned to appointments.'
    )
    is_superuser = models.BooleanField(
        _('Superuser'), default=False,
        help_text='Superusers can edit message templates, appointment types, '
        'and other users.'
    )

    def __str__(self):
        return "{} {} ({})".format(
            self.first_name, self.last_name, self.email)

    def clean(self):
        if (
                (self.first_name is None or self.first_name == '') and
                (self.last_name is None or self.last_name == '')
        ):
            raise ValidationError('Either a first name or a last name must be '
                                  'entered for a user.')
        return super(User, self).clean()


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
