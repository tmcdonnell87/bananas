from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from bananas.apps.message import SEND_EVENTS
from bananas.apps.message.utils import update_scheduled_messages
from bananas.utils.model_mixins import BaseModel


class AppointmentType(BaseModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class AppointmentQuerySet(QuerySet):
    def delete(self):
        # Dangerous. Should probably do in chunks, if at all
        appointments = list(self)
        self.update(deleted=True)
        for appointment in appointments:
            appointment.deleted = True
            appointment.modified = timezone.now()
            post_delete.send(
                sender=Appointment,
                instance=appointment,
                using=self.db
            )
    def update(self, **kwargs):
        super(AppointmentQuerySet, self).update(**kwargs)
        # Dangerous. Should probably do in chunks, if at all
        appointments = list(self)
        for appointment in appointments:
            post_save.send(
                sender=Appointment,
                instance=appointment,
                using=self.db
            )


class AppointmentManager(models.Manager):
    def active(self):
        return self.model.objects.filter(deleted=False)

    def get_queryset(self):
        return AppointmentQuerySet(self.model, using=self._db)


class Appointment(BaseModel):
    client_first_name = models.CharField(max_length=32, blank=True)
    client_last_name = models.CharField(max_length=32, blank=True)
    client_email = models.CharField(max_length=255, blank=True)
    client_phone = models.CharField(max_length=40, blank=True)
    client_language = models.CharField(
        max_length=16,
    )
    time = models.DateTimeField()
    counselor = models.ForeignKey(
        'user.User', on_delete=models.deletion.PROTECT)
    appointment_type = models.ForeignKey(
        'appointment.AppointmentType',
        related_name='appointments',
        on_delete=models.deletion.PROTECT
    )
    deleted = models.BooleanField(default=False)

    objects = AppointmentManager()

    def __str__(self):
        contact = self.client_phone or self.client_email
        return (
            self.client_first_name +
            ' ' +
            self.client_last_name +
            ' (' +
            contact +
            ') - ' +
            self.time.astimezone().strftime('%B %-d') +
            ', ' +
            self.time.astimezone().strftime('%-I:%M %p')
        )

    def clean(self):
        if not self.counselor.is_counselor:
            raise ValidationError('Only a user who is a counselor can be set as '
                                  'a counselor for an appointment.')
        if (
                (self.client_first_name is None or self.client_first_name == '') and
                (self.client_last_name is None or self.client_last_name == '')
        ):
            raise ValidationError('Either a first name or a last name must be '
                                  'entered for a client.')
        if (
                (self.client_email is None or self.client_email == '') and
                (self.client_phone is None or self.client_phone == '')
        ):
            raise ValidationError('Either a phone number or an email address must '
                                  'be entered for a client.')
        return super(Appointment, self).clean()

    def delete(self, using=None):
        Appointment.objects.filter(id=self.id).update(deleted=True)
        post_delete.send(
            sender=Appointment,
            instance=self,
            using=Appointment.objects.db
        )


@receiver(post_save, sender=Appointment)
def update_saved_appointment_messages(sender, instance, **kwargs):
    if kwargs.get('created', False):
        event = SEND_EVENTS.APPOINTMENT_CREATED
    else:
        event = SEND_EVENTS.APPOINTMENT_UPDATED
    update_scheduled_messages(instance, event)


@receiver(post_delete, sender=Appointment)
def update_deleted_appointment_messages(sender, instance, **kwargs):
    update_scheduled_messages(instance, SEND_EVENTS.APPOINTMENT_DELETED)
