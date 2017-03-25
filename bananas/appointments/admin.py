from dal import autocomplete

from django import forms
from django.contrib import admin
from bananas.appointments.models import (
    Appointment,
    MessageTemplate,
    ScheduledMessage
)


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('__all__')
        widgets = {
            'counselor': autocomplete.ModelSelect2(url='users:counselor-autocomplete')
        }


class ScheduledMessageForm(forms.ModelForm):

    class Meta:
        model = ScheduledMessage
        fields = ('__all__')
        widgets = {
            'appointment': autocomplete.ModelSelect2(
                url='appointments:appointment-autocomplete'),
            'message': autocomplete.ModelSelect2(
                url='appointments:message-template-autocomplete')
        }


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'time',
        'client_name',
        'client_phone',
        'client_email',
        'counselor_name'
    )
    search_fields = (
        'time',
        'client_first_name',
        'client_last_name',
        'client_email',
        'client_phone',
        'counselor__first_name',
        'counselor__last_name',
        'counselor__email',
        'counselor__phone',
    )
    list_filter = ('time', )
    form = AppointmentForm
    def client_name(self, obj):
        return "{} {}".format(
            obj.client_first_name, obj.client_last_name)
    def counselor_name(self, obj):
        return "{} {}".format(
            obj.counselor.first_name, obj.counselor.last_name)
    client_name.short_description = 'Client'
    counselor_name.short_description = 'Counselor'

@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = (
        'time',
        'client_name',
        'counselor_name',
        'message_title',
    )
    search_fields = (
        'time',
        'appointment__client_first_name',
        'appointment__client_last_name',
        'appointment__client_email',
        'appointment__client_phone',
        'appointment__counselor_first_name',
        'appointment__counselor_last_name',
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
    client_name.short_description = 'Client'
    counselor_name.short_description = 'Counselor'
    message_title.short_description = 'Message'


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'days_before',
        'short_text'
    )
    search_fields = (
        'title',
        'days_before',
        'text'
    )
    list_filter = ('days_before', )

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    short_text.short_description = 'Text'
