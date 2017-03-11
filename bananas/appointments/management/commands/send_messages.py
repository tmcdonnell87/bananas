from django.core.management.base import BaseCommand, CommandError
from bananas.appointments.utils import send_messages

class Command(BaseCommand):
    help = 'Sends messages that are past their due date.'

    def handle(self, *args, **kwargs):
        sent_messages, failed_messages = send_messages()
        if sent_messages:
            self.stdout.write(self.style.SUCCESS(
                'Successfully sent {0} messages'.format(sent_messages)))
        if failed_messages:
            self.stdout.write(self.style.WARNING(
                'Failed to send {0} messages'.format(failed_messages)))
