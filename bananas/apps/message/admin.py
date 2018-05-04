from django.contrib import admin

from bananas.apps.message.forms import MessageTemplateForm
from bananas.apps.message.forms import ScheduledMessageForm
from bananas.apps.message.models import MessageTemplate
from bananas.apps.message.models import ScheduledMessage


@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = (
        'time',
        'client_name',
        'counselor_name',
        'message_title',
        'appointment_type_name',
    )
    search_fields = (
        'time',
        'appointment__client_first_name',
        'appointment__client_last_name',
        'appointment__client_email',
        'appointment__client_phone',
        'appointment__counselor__first_name',
        'appointment__counselor__last_name',
        'message__title',
        'message__text',
    )
    list_filter = ('time', )
    form = ScheduledMessageForm

    def client_name(self, obj):
        return "{} {}".format(
            obj.appointment.client_first_name,
            obj.appointment.client_last_name
        )

    def counselor_name(self, obj):
        return "{} {}".format(
            obj.appointment.counselor.first_name,
            obj.appointment.counselor.last_name
        )

    def message_title(self, obj):
        return obj.message.title

    def appointment_type_name(self, obj):
        return obj.appointment.appointment_type.name

    client_name.short_description = 'Client'
    counselor_name.short_description = 'Counselor'
    message_title.short_description = 'Message'
    appointment_type_name.short_description = 'Appointment type'


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'send_event',
        'send_days_offset',
        'short_text',
        'appointment_type_name',
    )
    search_fields = (
        'title',
        'text',
        'appointment_type__name',
    )
    list_filter = ('send_event', )

    form = MessageTemplateForm

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text

    def appointment_type_name(self, obj):
        return obj.appointment_type.name

    short_text.short_description = 'Text'
    appointment_type_name.short_description = 'Appointment type'
