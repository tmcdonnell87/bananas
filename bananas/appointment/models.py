from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from bananas.message.utils import update_scheduled_messages


class AppointmentType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Appointment(models.Model):
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

    def __str__(self):
        contact = self.client_phone or self.client_email
        return (
            self.client_first_name +
            ' ' +
            self.client_last_name +
            ' (' +
            contact +
            ') - ' +
            self.time.strftime('%B %-d') +
            ', ' +
            self.time.strftime('%-I:%M %p')
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


@receiver(post_save, sender=Appointment)
def update_appointment_messages(sender, instance, **kwargs):
    update_scheduled_messages(instance)
