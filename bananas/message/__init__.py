from bananas.utils.collections import ModelChoices


SEND_EVENTS = ModelChoices(
    APPOINTMENT_CREATED=('c', 'Appointment Created'),
    APPOINTMENT_UPDATED=('u', 'Appointment Updated'),
    APPOINTMENT_DELETED=('d', 'Appointment Deleted'),
    APPOINTMENT_ATTENDED=('a', 'Appointment Attended'),
)

# Events that can only be sent after they have occurred
# * send_time must be None
# * send_hours_offset and send_days_offset must be zero or positive
SEND_AFTER_RESTRICTED_EVENTS = (
    SEND_EVENTS.APPOINTMENT_CREATED,
    SEND_EVENTS.APPOINTMENT_UPDATED,
    SEND_EVENTS.APPOINTMENT_DELETED
)
