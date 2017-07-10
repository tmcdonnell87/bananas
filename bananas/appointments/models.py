from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta
from django.utils import timezone


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
        'users.User', on_delete=models.deletion.PROTECT)
    appointment_type = models.ForeignKey(
        'appointments.AppointmentType',
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
                (self.client_first_name is None or self.client_first_name=='') and
                (self.client_last_name is None or self.client_last_name=='')
        ):
            raise ValidationError('Either a first name or a last name must be '
                                  'entered for a client.')
        if (
                (self.client_email is None or self.client_email=='') and
                (self.client_phone is None or self.client_phone=='')
        ):
            raise ValidationError('Either a phone number or an email address must '
                                  'be entered for a client.')
        return super(Appointment, self).clean()


class MessageTemplate(models.Model):
    days_before = models.PositiveIntegerField()
    send_time = models.TimeField(auto_now=False)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=1000)
    appointment_type = models.ForeignKey(
        'appointments.AppointmentType',
        related_name='message_templates',
        on_delete=models.deletion.PROTECT
    )

    def __str__(self):
        return self.title + ' (' + str(self.days_before) + ' days before)'


class ScheduledMessage(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.deletion.PROTECT)
    time = models.DateTimeField()
    message = models.ForeignKey(
        MessageTemplate,
        on_delete=models.deletion.PROTECT,
    )

    def clean(self):
        if self.appointment.appointment_type != self.message.appointment_type:
            raise ValidationError("A scheduled message's template must have the same "
                                  "appointment type as the scheduled message's appointment.")
        return super(ScheduledMessage, self).clean()


@receiver(post_save, sender=Appointment)
def update_scheduled_messages(sender, instance, **kwargs):
    # Remove previous scheduled messages
    ScheduledMessage.objects.filter(appointment=instance).delete()

    # Add new scheduled messages
    templates = MessageTemplate.objects.filter(appointment_type=instance.appointment_type)
    current_time = timezone.now()
    for template in templates:
        reminder_time = instance.time - timedelta(days=template.days_before)
        reminder_time.replace(
            hour=template.send_time.hour,
            minute=template.send_time.minute,
        )
        if reminder_time > current_time:
            ScheduledMessage.objects.create(
                message=template,
                time=reminder_time,
                appointment=instance
            )
