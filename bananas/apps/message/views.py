from dal import autocomplete

from django.http import HttpResponse

from bananas.apps.appointment.models import Appointment
from bananas.apps.message.models import MessageTemplate


class MessageTemplateAutocomplete(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponse('Unauthorized', status=401)
        return super(MessageTemplateAutocomplete, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        appointment_id = self.forwarded.get('appointment', None)

        if appointment_id:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_type = appointment.appointment_type
            qs = MessageTemplate.objects.filter(appointment_type=appointment_type)
        else:
            return MessageTemplate.objects.none()

        if self.q:
            qs = qs.filter(
                title__icontains=self.q
            )

        return qs
