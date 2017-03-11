from django.contrib import admin
from .models import Appointment, MessageTemplate, ScheduledMessage

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ('time', 'client_last_name', 'client_phone')
    list_display = ('time', 'client_last_name', 'client_phone', 'counselor_name')
    def counselor_name(self, obj):
        return obj.counselor.name
    counselor_name.short_description = 'Counselor'

@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ('time', 'client_name', 'message_title')
    def client_name(self, obj):
        return obj.appointment.client_name
    def message_title(self, obj):
        return obj.message.title
    client_name.short_description = 'Client'
    message_title.short_description = 'Message'
    pass

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    pass

