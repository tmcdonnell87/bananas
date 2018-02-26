from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.user = self.make_user()

    def test_counselor_autocomplete_reverse(self):
        """
        user:counselor-autocomplete should reverse to
        /user/counselor-autocomplete/
        """
        self.assertEqual(reverse('user:counselor-autocomplete'),
                         '/user/counselor-autocomplete/')

    def test_counselor_autocomplete_resolve(self):
        """
        /user/counselor-autocomplete should resolve to
        user:counselor-autocomplete
        """
        self.assertEqual(resolve('/user/counselor-autocomplete/').view_name,
                         'user:counselor-autocomplete')

