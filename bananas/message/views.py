from dal import autocomplete

from bananas.appointment.models import Appointment
from bananas.message.models import MessageTemplate


class MessageTemplateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return MessageTemplate.objects.none()

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
