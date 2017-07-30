import logging
import re

from django.utils import timezone

from bananas.appointments.models import ScheduledMessage
from bananas.translation.utils import translate_text
from bananas.utils.messaging import send_email
from bananas.utils.messaging import send_sms


logger = logging.getLogger(__name__)


def send_messages():
    messages_to_send = ScheduledMessage.objects.filter(time__lte=timezone.now())
    sent_messages = 0
    failed_messages = 0
    for scheduled_message in messages_to_send:
        message_text = get_message_text(scheduled_message)
        if (scheduled_message.appointment.client_language and
                scheduled_message.appointment.client_language != 'en'):
            message_text = translate_text(
                message_text, scheduled_message.appointment.client_language)
        if scheduled_message.appointment.client_phone:
            # Send to twilio
            try:
                send_sms(
                    body=message_text,
                    to_number=scheduled_message.appointment.client_phone
                )
                logger.info('Sent text message "{message}" to {client}'.format(
                    message=scheduled_message.message.title,
                    client=scheduled_message.appointment.client_phone
                ))
                sent_messages += 1
            except:
                logger.exception('Failed to send text message "{message}" '
                                 'to {client}'.format(
                        message=scheduled_message.message.title,
                        client=scheduled_message.appointment.client_phone
                    ))
                failed_messages += 1

        elif scheduled_message.appointment.client_email:
            # Send to mailgun
            try:
                send_email(
                    body=message_text,
                    to_email=scheduled_message.appointment.client_email
                )
                logger.info('Sent email "{message}" to {client}'.format(
                    message=scheduled_message.message.title,
                    client=scheduled_message.appointment.client_email
                ))
                sent_messages += 1
            except:
                logger.exception(
                    'Failed to send email "{message}" to {client}'.format(
                        message=scheduled_message.message.title,
                        client=scheduled_message.appointment.client_email
                    ))
                failed_messages += 1
        scheduled_message.delete()
    return (sent_messages, failed_messages)

def get_message_text(scheduled_message):
    return re.sub(
        # trim the whitespace between tag brackets
        # {   example_tag   } => {example_tag}
        r'(\{)\s*(\S+)\s*(?=})',
        r'\1\2',
        scheduled_message.message.text,
        0,
        re.MULTILINE | re.IGNORECASE
    ).format(
        # Fill in tags
        # {example_tag} => example_value
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

