from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta
from django.utils import timezone


# Create your models here.
from ..users.models import User

# Create your models here.
class Appointment(models.Model):
    client_first_name = models.CharField(max_length=32)
    client_last_name = models.CharField(max_length=32)
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
    counselor = models.ForeignKey(User, on_delete=models.deletion.PROTECT)
    def __str__(self):
        return str(self.time) + '-' + str(self.client_last_name) + '-' + self.client_phone

class MessageTemplate(models.Model):
    days_before = models.PositiveIntegerField()
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=1000)

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
