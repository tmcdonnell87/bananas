from bananas.appointments.models import ScheduledMessage
from django.conf import settings
from django.utils import timezone
import requests
from twilio.rest import TwilioRestClient


def send_email(
    body,
    subject='Bananas Appointment',
    to_email='Tara Bartholomew <tara@bananasbunch.org>',
    from_email='Tara Bartholomew <tara@bananasbunch.org>'
):
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(
            settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']
        ),
        auth=("api", settings.ANYMAIL['MAILGUN_API_KEY']),
        data={
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "text": body
        }
    )

twilio_client = TwilioRestClient(
    settings.TWILIO['account_sid'],
    settings.TWILIO['auth_token']
)

def send_sms(to_number, body):
    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO['phone_number']
    )

def send_messages():
    messages_to_send = ScheduledMessage.objects.filter(time__lte=timezone.now())
    sent_messages = 0
    failed_messages = 0
    for scheduled_message in messages_to_send:
        if scheduled_message.appointment.client_phone:
            # Send to twilio
            try:
                send_sms(
                    body=scheduled_message.message.text,
                    to_number=scheduled_message.appointment.client_phone
                )
                sent_messages += 1
            except:
                failed_messages += 1

        elif scheduled_message.appointment.client_email:
            # Send to mailgun
            try:
                send_email(
                    body=scheduled_message.message.text,
                    to_email=scheduled_message.appointment.client_email
                )
                sent_messages += 1
            except:
                failed_messages += 1
        scheduled_message.delete()
    return (sent_messages, failed_messages)
