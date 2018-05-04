import json

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from test_plus.test import TestCase

from bananas.apps.user.tests.factories import UserFactory
from bananas.apps.user.views import CounselorAutocomplete


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.factory = RequestFactory()


class TestCounselorAutocompleteView(BaseUserTestCase):

    def setUp(self):
        super(TestCounselorAutocompleteView, self).setUp()
        self.resource = '/user/counselor-autocomplete/'
        self.view = CounselorAutocomplete.as_view()
        self.user.is_counselor = True
        self.user.save()

    def test_get_counselor_suggestions_requires_authentication(self):
        request = self.factory.get(self.resource)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_get_counselor_suggestions(self):
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
                'text': str(self.user),
                'id': self.user.id
            }]
        )

    def test_filter_counselor_suggestions(self):
        counselor = UserFactory.create(is_counselor=True)
        request = self.factory.get(self.resource, {'q': '{} {} {}'.format(
            counselor.first_name, counselor.last_name, counselor.email)})
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
                'text': str(counselor),
                'id': counselor.id
            }]
        )
