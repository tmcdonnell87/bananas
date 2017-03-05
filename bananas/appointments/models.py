from django.db import models

# Create your models here.
from ..users.models import User

# Create your models here.

# Create your models here.
class Appointment(models.Model):
    client_first_name = models.CharField(max_length=32)
    client_last_name = models.CharField(max_length=32)
    client_email = models.CharField(max_length=255,null=True)
    client_phone = models.CharField(max_length=40,null=True)
    ENGLISH = 'EN'
    SPANISH = 'ES'
    client_language = models.CharField(
        choices=((ENGLISH, 'English'), (SPANISH, 'Spanish')),
        default=ENGLISH,
        max_length=2,
    )
    time = models.DateTimeField()
    counselor = models.ForeignKey(User, on_delete=models.deletion.PROTECT)
    def __str__(self):
        return str(self.time) + '-' + str(self.client_last_name) + '-' + self.client_phone

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=255)

class Message(models.Model):
    days_before = models.PositiveIntegerField()
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=1000)
