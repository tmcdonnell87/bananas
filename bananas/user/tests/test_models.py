from test_plus.test import TestCase

from django.core.exceptions import ValidationError


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_name_required(self):
        # Should raise an error
        self.user.first_name = None
        self.user.last_name = None
        self.assertRaises(ValidationError, self.user.clean)
        self.user.first_name = ''
        self.user.last_name = ''
        self.assertRaises(ValidationError, self.user.clean)

        # Should not raise an error
        self.user.first_name = 'Michael'
        self.user.last_name = None
        self.user.clean()
        self.user.first_name = None
        self.user.last_name = 'Bluth'
        self.user.clean()
        self.user.first_name = 'Michael'
        self.user.last_name = 'Bluth'
        self.user.clean()
