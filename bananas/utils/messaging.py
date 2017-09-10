from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import TwilioRestClient


twilio_client = TwilioRestClient(
    settings.TWILIO['account_sid'],
    settings.TWILIO['auth_token']
)


def send_sms(to_number, body):
    return twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO['phone_number']
    )


def send_email(
    body,
    to_email,
    from_email=None,
    subject='Bananas Appointment'
):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    return send_mail(subject, body, from_email, [to_email])
