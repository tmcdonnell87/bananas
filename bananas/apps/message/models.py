import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from bananas.apps.message import SEND_EVENTS
from bananas.apps.message import SEND_AFTER_RESTRICTED_EVENTS
from bananas.utils.model_mixins import BaseModel


class MessageTemplate(BaseModel):
    SEND_EVENTS = SEND_EVENTS


    send_event = models.CharField(
        max_length=1, choices=SEND_EVENTS,
        help_text='The event on which the sending of this message is based.'
    )
    send_time = models.TimeField(
        null=True, auto_now=False, default=None,
        help_text='The clock time to send a message. Cannot be used when '
        'a send hours offset is set.'
    )
    send_hours_offset = models.IntegerField(
        default=0,
        help_text='The number of hours before (negative) or after (positive) '
        'the send event to send this message. Cannot be used when a send time '
        'is set.'
    )
    send_days_offset = models.IntegerField(
        default=0,
        help_text='The number of days before (negative) or after (positive) '
        'the send event to send this message.'
    )
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=1000)
    appointment_type = models.ForeignKey(
        'appointment.AppointmentType',
        related_name='message_templates',
        on_delete=models.deletion.PROTECT
    )

    def __str__(self):
        return self.title

    def clean(self):
        if self.send_event in SEND_AFTER_RESTRICTED_EVENTS:
            if self.send_time is not None:
                raise ValidationError(
                    'Cannot set a send time when using {} as the send event'
                    .format(self.get_choice_field_display('send_event'))
                )
            total_send_offset = datetime.timedelta(
                days=self.send_days_offset, hours=self.send_hours_offset)
            if total_send_offset < datetime.timedelta():
                raise ValidationError(
                    'Cannot send a message before the {} event occurs'
                    .format(self.get_choice_field_display('send_event'))
                )
        return super(MessageTemplate, self).clean()

    def get_send_datetime(self, appointment, event=None):
        send_datetime = None
        send_now = False

        if appointment.deleted:
            if self.send_event == SEND_EVENTS.APPOINTMENT_DELETED:
                send_datetime = appointment.modified
        else:
            if self.send_event == SEND_EVENTS.APPOINTMENT_ATTENDED:
                send_datetime = appointment.time
            elif self.send_event == SEND_EVENTS.APPOINTMENT_CREATED:
                send_datetime = appointment.created
            elif self.send_event == SEND_EVENTS.APPOINTMENT_UPDATED:
                send_datetime = appointment.modified

        if send_datetime is not None:
            send_datetime += datetime.timedelta(
                days=self.send_days_offset, hours=self.send_hours_offset)
            if self.send_time is not None:
                send_datetime = send_datetime.replace(
                    hour=self.send_time.hour,
                    minute=self.send_time.minute,
                )

        if self.send_immediately and self.send_event == event:
            send_now = True
            send_datetime = timezone.now()

        return send_now, send_datetime

    @property
    def send_immediately(self):
        return not (self.send_time or
                    self.send_hours_offset or
                    self.send_days_offset)


class ScheduledMessage(BaseModel):
    id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        'appointment.Appointment',
        on_delete=models.deletion.CASCADE
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
