import json

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from test_plus.test import TestCase

from bananas.apps.appointment.tests.factories import AppointmentFactory
from bananas.apps.appointment.tests.factories import AppointmentTypeFactory
from bananas.apps.appointment.views import AppointmentAutocomplete
from bananas.apps.appointment.views import AppointmentTypeAutocomplete
from bananas.apps.user.tests.factories import UserFactory


class BaseAppointmentTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.appointment = AppointmentFactory.create()
        self.appointment_type = self.appointment.appointment_type
        self.factory = RequestFactory()


class TestAppointmentAutocompleteView(BaseAppointmentTestCase):

    def setUp(self):
        super(TestAppointmentAutocompleteView, self).setUp()
        self.resource = '/appointment/appointment-autocomplete/'
        self.view = AppointmentAutocomplete.as_view()

    def test_get_appointment_suggestions_requires_authentication(self):
        request = self.factory.get(self.resource)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_get_appointment_suggestions(self):
        request = self.factory.get(self.resource)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data['pagination'],
            {
                'more': False
            }
        )
        self.assertEqual(
            data['results'],
            [{
                'text': str(self.appointment),
                'id': self.appointment.id
            }]
        )

    def test_filter_appointment_suggestions(self):
        appointment = AppointmentFactory.create()
        request = self.factory.get(self.resource, {'q': "{} {} {} {}".format(
            appointment.client_first_name,
            appointment.client_last_name,
            appointment.client_email,
            appointment.client_phone
        )})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data['pagination'],
            {
                'more': False
            }
        )
        self.assertEqual(
            data['results'],
            [{
                'text': str(appointment),
                'id': appointment.id
            }]
        )

class TestAppointmentTypeAutocompleteView(BaseAppointmentTestCase):

    def setUp(self):
        super(TestAppointmentTypeAutocompleteView, self).setUp()
        self.resource = '/appointment/appointment-type-autocomplete/'
        self.view = AppointmentTypeAutocomplete.as_view()

    def test_get_appointment_type_suggestions_requires_authentication(self):
        request = self.factory.get(self.resource)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_get_appointment_type_suggestions(self):
        request = self.factory.get(self.resource)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data['pagination'],
            {
                'more': False
            }
        )
        self.assertEqual(
            data['results'],
            [{
                'text': str(self.appointment_type),
                'id': self.appointment_type.id
            }]
        )

    def test_filter_appointment_type_suggestions(self):
        appointment_type = AppointmentTypeFactory.create()
        request = self.factory.get(self.resource, {'q': appointment_type.name})
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200
        )
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            data['pagination'],
            {
                'more': False
            }
        )
        self.assertEqual(
            data['results'],
            [{
                'text': str(appointment_type),
                'id': appointment_type.id
            }]
        )
