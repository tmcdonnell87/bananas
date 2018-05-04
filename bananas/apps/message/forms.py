from dal import autocomplete

from django import forms

from bananas.apps.appointment.models import Appointment
from bananas.apps.appointment.models import AppointmentType
from bananas.apps.message.models import MessageTemplate
from bananas.apps.message.models import ScheduledMessage


class ScheduledMessageForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='appointment:appointment-autocomplete',
        )
    )
    message = forms.ModelChoiceField(
        queryset=MessageTemplate.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='message:message-template-autocomplete',
            forward=['appointment']
        ),
        help_text="Only message templates for the appointment's appointment type "
                  "will be displayed."
    )

    class Meta:
        model = ScheduledMessage
        fields = ('__all__')


class MessageTemplateForm(forms.ModelForm):
    send_event = forms.ChoiceField(choices=MessageTemplate.SEND_EVENTS)
    send_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'time-input'}),
        help_text='Sends at the time of the event, when blank'
    )
    send_days_offset = forms.IntegerField(
        required=False,
        help_text='Defaults to 0 when blank'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '20'}),
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
        widget=autocomplete.ModelSelect2(url='appointment:appointment-type-autocomplete')
    )

    class Meta:
        model = MessageTemplate
        fields = ('__all__')
