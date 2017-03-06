from bananas.appointments.models import ScheduledMessage
from bananas.appointments.utils import send_message
from bananas.appointments.utils import send_sms
from datetime import datetime
from django_cron import CronJobBase, Schedule


class SendMessages(CronJobBase):
    RUN_EVERY_MINS = 60 # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(
        run_every_mins=RUN_EVERY_MINS,
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS
    )

    code = 'appointments.send_messages'

    def do(self):
        messages_to_send = ScheduledMessage.objects.filter(time__lte=datetime.now())
        for message in messages_to_send:
            if message.appointment.client_phone:
                # Send to twilio
                send_sms(
                    body=message.text,
                    to_number=message.appointment.client_phone
                )

            elif message.appointment.client_email:
                # Send to mailgun
                send_email(
                    body=message.text,
                    to_email=message.appointment.client_email
                )
