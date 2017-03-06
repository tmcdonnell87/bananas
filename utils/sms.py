# must do pip install twilio


from twilio.rest import TwilioRestClient
import json


with open('twilio_config.json', 'r') as infile:
    twilio_config = json.load(infile)


twilio_client = TwilioRestClient(
    twilio_config['account_sid'],
    twilio_config['auth_token']
)

def send_sms(to_number, body):
    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=twilio_config['phone_number']
    )

if __name__ == '__main__':
    send_sms('+12485203071', 'hello twilio helper works')
