import requests
from django.conf import settings


def send_simple_message(
    subject,
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
