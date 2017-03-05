# must do pip install twilio


from twilio.rest import TwilioRestClient
import json


with open('twilio_config.json', 'r') as infile:
    twilio_config = json.load(infile)


# account_sid
# auth_token
# phone_number

twilio_client = TwilioRestClient(
    twilio_config['account_sid'],
    twilio_config['auth_token']
)

