from twilio.rest import TwilioRestClient
from django.conf import settings

TWILIO = dict(
    TWILIO_ACCOUNT_SID='AC373269167f5ffccd05533fb4e860c683',
    TWILIO_AUTH_TOKEN='457c9db470a139d2b26686b8852979b5',
    TWILIO_PHONE_NUMBER='+19253784063'
)

twilio_client = TwilioRestClient(
    TWILIO['TWILIO_ACCOUNT_SID'],
    TWILIO['TWILIO_AUTH_TOKEN']
)

def send_sms(to_number, body):
    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=TWILIO['TWILIO_PHONE_NUMBER']
    )
