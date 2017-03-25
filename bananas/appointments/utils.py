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
        message_text = get_message_text(scheduled_message)
        if scheduled_message.appointment.client_phone:
            # Send to twilio
            try:
                send_sms(
                    body=message_text,
                    to_number=scheduled_message.appointment.client_phone
                )
                sent_messages += 1
            except:
                failed_messages += 1

        elif scheduled_message.appointment.client_email:
            # Send to mailgun
            try:
                send_email(
                    body=message_text,
                    to_email=scheduled_message.appointment.client_email
                )
                sent_messages += 1
            except:
                failed_messages += 1
        scheduled_message.delete()
    return (sent_messages, failed_messages)

def get_message_text(scheduled_message):
    return scheduled_message.message.text.format(
        client_name="{} {}".format(scheduled_message.appointment.client_first_name,
                                   scheduled_message.appointment.client_last_name),
        client_first_name=scheduled_message.appointment.client_first_name,
        client_last_name=scheduled_message.appointment.client_last_name,
        client_email=scheduled_message.appointment.client_email,
        client_phone=scheduled_message.appointment.client_phone,
        appointment_date=scheduled_message.appointment.time.strftime('%A, %B %-d'),
        appointment_time=scheduled_message.appointment.time.strftime('%-I:%M %p'),
        counselor_name="{} {}".format(scheduled_message.appointment.counselor.first_name,
                                   scheduled_message.appointment.counselor.last_name),
        counselor_first_name=scheduled_message.appointment.counselor.first_name,
        counselor_last_name=scheduled_message.appointment.counselor.last_name,
        counselor_phone=scheduled_message.appointment.counselor.phone,
        counselor_email=scheduled_message.appointment.counselor.email
    )
