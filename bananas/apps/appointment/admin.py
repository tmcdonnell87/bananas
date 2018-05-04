from django.contrib import admin

from bananas.apps.appointment.forms import AppointmentForm
from bananas.apps.appointment.models import Appointment
from bananas.apps.appointment.models import AppointmentType


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

    def get_queryset(self, request):
        queryset = super(AppointmentAdmin, self).get_queryset(request)
        return queryset.filter(deleted=False)

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


@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
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
