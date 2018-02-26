from dal import autocomplete

from django.db.models import Q
from django.http import HttpResponse

from bananas.appointment.models import Appointment
from bananas.appointment.models import AppointmentType


class AppointmentAutocomplete(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponse('Unauthorized', status=401)
        return super(AppointmentAutocomplete, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.filter(deleted=False)

        if self.q:
            qs = qs.filter(
                Q(client_first_name__icontains=self.q) |
                Q(client_last_name__icontains=self.q) |
                Q(client_email__icontains=self.q) |
                Q(client_phone__icontains=self.q)
            )

        return qs


class AppointmentTypeAutocomplete(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponse('Unauthorized', status=401)
        return super(AppointmentTypeAutocomplete, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        qs = AppointmentType.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
