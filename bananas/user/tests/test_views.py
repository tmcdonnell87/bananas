import json

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from test_plus.test import TestCase

from ..views import (
    CounselorAutocomplete
)


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class TestCounselorAutocompleteView(BaseUserTestCase):

    def setUp(self):
        super(TestCounselorAutocompleteView, self).setUp()
        self.view = CounselorAutocomplete.as_view()
        self.username = 'michael@bluth.com'
        self.user.is_counselor = True
        self.user.first_name = 'Michael'
        self.user.last_name = 'Bluth'
        self.user.save()

    def test_get_counselor_suggestions_requires_authentication(self):
        request = self.factory.get('/user/counselor-autocomplete/')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_get_counselor_suggestions(self):
        request = self.factory.get('/user/counselor-autocomplete/')
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
        counselor = self.make_user('george@bluth.com')
        counselor.is_counselor = True
        counselor.first_name = 'George'
        counselor.last_name = 'Bluth'
        counselor.save()
        request = self.factory.get('/user/counselor-autocomplete/',
                                   {'q': 'George Bluth'})
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
