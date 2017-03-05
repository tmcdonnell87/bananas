from django.contrib import admin
from .models import Appointment, Document, Message

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ('time', 'client_last_name', 'client_phone')
    list_display = ('time', 'client_last_name', 'client_phone', 'counselor_name')
    def counselor_name(self, obj):
        return obj.counselor.name
    counselor_name.short_description = 'Counselor'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
