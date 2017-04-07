from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class Appointment(models.Model):
    client_first_name = models.CharField(max_length=32, blank=True)
    client_last_name = models.CharField(max_length=32, blank=True)
    client_email = models.CharField(max_length=255, blank=True)
    client_phone = models.CharField(max_length=40, blank=True)
    ENGLISH = 'EN'
    SPANISH = 'ES'
    client_language = models.CharField(
        choices=((ENGLISH, 'English'), (SPANISH, 'Spanish')),
        default=ENGLISH,
        max_length=2,
    )
    time = models.DateTimeField()
    counselor = models.ForeignKey('users.User', on_delete=models.deletion.PROTECT)
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
    title = models.CharField(max_length=40)
    text = models.TextField(
        max_length=1000,
        help_text='<h4>Smart Tags</h4>'
        '<ul>'
        '<li><code>{ client_name }</code> The first and last name of the client</li>'
        '<li><code>{ client_first_name }</code> The first name of the client</li>'
        '<li><code>{ client_last_name }</code> The last name of the client</li>'
        '<li><code>{ client_email }</code> The email address of the client</li>'
        '<li><code>{ client_phone }</code> The client\'s phone number</li>'
        '<li><code>{ appointment_date }</code> The month, day, and year of the appointment</li>'
        '<li><code>{ appointment_time }</code> The time of the appointment</li>'
        '<li><code>{ counselor_name }</code> The name of the counselor assigned to the appointment</li>'
        '<li><code>{ counselor_first_name }</code> The first name of the counselor assigned to the appointment</li>'
        '<li><code>{ counselor_last_name }</code> The last name of the counselor assigned to the appointment</li>'
        '<li><code>{ counselor_phone }</code> The phone number of the counselor assigned to the appointment</li>'
        '<li><code>{ counselor_email }</code> The  email address  of the counselor assigned to the appointment</li>'
        '</ul>'
    )
    def __str__(self):
        return self.title + ' (' + str(self.days_before) + ' days before)'


class ScheduledMessage(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.deletion.PROTECT)
    time = models.DateTimeField()
    message = models.ForeignKey(MessageTemplate, on_delete=models.deletion.PROTECT)


@receiver(post_save, sender=Appointment)
def update_scheduled_messages(sender, instance, **kwargs):
    # Remove previous scheduled messages
    ScheduledMessage.objects.filter(appointment=instance).delete()

    # Add new scheduled messages
    templates = MessageTemplate.objects.all()
    current_time = timezone.now()
    for template in templates:
        reminder_time = instance.time - timedelta(days=template.days_before)
        if reminder_time > current_time:
            m = ScheduledMessage(message=template, time=reminder_time, appointment=instance)
            m.save()
