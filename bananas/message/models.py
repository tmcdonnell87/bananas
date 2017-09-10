from django.core.exceptions import ValidationError
from django.db import models


class MessageTemplate(models.Model):
    days_before = models.PositiveIntegerField()
    send_time = models.TimeField(auto_now=False)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=1000)
    appointment_type = models.ForeignKey(
        'appointment.AppointmentType',
        related_name='message_templates',
        on_delete=models.deletion.PROTECT
    )

    def __str__(self):
        return self.title + ' (' + str(self.days_before) + ' days before)'


class ScheduledMessage(models.Model):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        'appointment.Appointment',
        on_delete=models.deletion.PROTECT
    )
    time = models.DateTimeField()
    message = models.ForeignKey(
        'message.MessageTemplate',
        on_delete=models.deletion.PROTECT,
    )

    def clean(self):
        if self.appointment.appointment_type != self.message.appointment_type:
            raise ValidationError("A scheduled message's template must have the same "
                                  "appointment type as the scheduled message's appointment.")
        return super(ScheduledMessage, self).clean()
