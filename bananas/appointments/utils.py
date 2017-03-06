from django.conf import settings
import requests


def send_email(
    subject='Bananas Appointment',
    body,
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
    settings.TWILIO['TWILIO_ACCOUNT_SID'],
    settings.TWILIO['TWILIO_AUTH_TOKEN']
)

def send_sms(to_number, body):
    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO['TWILIO_PHONE_NUMBER']
    )
