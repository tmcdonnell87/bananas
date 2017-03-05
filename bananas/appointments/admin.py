from django.contrib import admin
from .models import Appointment, Document, Message

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('time', 'client_last_name', 'client_phone')
    #def get_name(self, obj):
    #    return obj.cousenlor.name

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
