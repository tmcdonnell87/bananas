from dal import autocomplete

from django import forms
from django.contrib import admin
from bananas.appointments.models import (
    Appointment,
    AppointmentType,
    MessageTemplate,
    ScheduledMessage
)
from bananas.translation.fields import LanguageField
from bananas.users.models import User


class AppointmentForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    counselor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='users:counselor-autocomplete')
    )
    appointment_type = forms.ModelChoiceField(
        queryset=AppointmentType.objects.all(),
        widget=autocomplete.ModelSelect2(url='appointments:appointment-type-autocomplete')
    )
    client_language = LanguageField(
        widget=autocomplete.ListSelect2(url='translation:language-autocomplete')
    )


    class Meta:
        model = Appointment
        fields = ('__all__')


class ScheduledMessageForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='appointments:appointment-autocomplete',
        )
    )
    message = forms.ModelChoiceField(
        queryset=MessageTemplate.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='appointments:message-template-autocomplete',
            forward=['appointment']
        ),
        help_text="Only message templates for the appointment's appointment type "
                  "will be displayed."
    )

    class Meta:
        model = ScheduledMessage
        fields = ('__all__')

class MessageTemplateForm(forms.ModelForm):
    days_before = forms.IntegerField()
    send_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'time-input'}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows':'20'}),
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
    appointment_type = forms.ModelChoiceField(
        queryset=AppointmentType.objects.all(),
        widget=autocomplete.ModelSelect2(url='appointments:appointment-type-autocomplete')
    )

    class Meta:
        model = MessageTemplate
        fields = ('__all__')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'time',
        'client_name',
        'client_phone',
        'client_email',
        'appointment_type_name',
        'counselor_name'
    )
    search_fields = (
        'time',
        'client_first_name',
        'client_last_name',
        'client_email',
        'client_phone',
        'appointment_type__name',
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

    def appointment_type_name(self, obj):
        return obj.appointment_type.name

    client_name.short_description = 'Client'
    counselor_name.short_description = 'Counselor'
    appointment_type_name.short_description = 'Appointment type'

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
        'days_before',
        'short_text',
        'appointment_type_name',
    )
    search_fields = (
        'title',
        'days_before',
        'text',
        'appointment_type__name',
    )
    list_filter = ('days_before', )

    form = MessageTemplateForm

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text

    def appointment_type_name(self, obj):
        return obj.appointment_type.name

    short_text.short_description = 'Text'
    appointment_type_name.short_description = 'Appointment type'


@admin.register(AppointmentType)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'appointment_count',
        'message_template_count'
    )
    search_fields = (
        'name',
    )

    def appointment_count(self, obj):
        return obj.appointments.all().count()

    def message_template_count(self, obj):
        return obj.message_templates.all().count()
