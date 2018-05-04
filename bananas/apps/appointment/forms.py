from dal import autocomplete

from django import forms

from bananas.apps.appointment.models import Appointment
from bananas.apps.appointment.models import AppointmentType
from bananas.apps.translation.fields import LanguageField
from bananas.apps.user.models import User


class AppointmentForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'datetime-input'}))
    counselor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user:counselor-autocomplete')
    )
    appointment_type = forms.ModelChoiceField(
        queryset=AppointmentType.objects.all(),
        widget=autocomplete.ModelSelect2(url='appointment:appointment-type-autocomplete')
    )
    client_language = LanguageField(
        widget=autocomplete.ListSelect2(url='translation:language-autocomplete')
    )

    class Meta:
        model = Appointment
        fields = ('__all__')
        exclude = ('deleted', )
