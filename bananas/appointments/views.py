from dal import autocomplete

from django.db.models import Q

from bananas.appointments.models import Appointment
from bananas.appointments.models import MessageTemplate


class AppointmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Appointment.objects.none()

        qs = Appointment.objects.all()

        if self.q:
            qs = qs.filter(
                Q(client_first_name__icontains=self.q) |
                Q(client_last_name__icontains=self.q) |
                Q(client_email__icontains=self.q) |
                Q(client_phone__icontains=self.q)
            )

        return qs


class MessageTemplateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return MessageTemplate.objects.none()

        qs = MessageTemplate.objects.all()

        if self.q:
            qs = qs.filter(
                title__icontains=self.q
            )

        return qs
