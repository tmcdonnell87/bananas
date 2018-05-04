from test_plus.test import TestCase

from ..admin import MyUserCreationForm


class TestMyUserCreationForm(TestCase):

    def setUp(self):
        self.user = self.make_user('first_user', 'first_user_password')

    def test_clean_username_success(self):
        # Instantiate the form with a new username
        form = MyUserCreationForm({
            'username': 'michael_bluth',
            'first_name': 'Michael',
            'last_name': 'Bluth',
            'email': 'michael@bluth.com',
            'phone': '18005556666',
            'password1': '7jefB#f@Cc7YJB]2v',
            'password2': '7jefB#f@Cc7YJB]2v',
        })
        # Run is_valid() to trigger the validation
        valid = form.is_valid()
        self.assertTrue(valid, form.errors)

        # Run the actual clean_username method
        username = form.clean_username()
        self.assertEqual('michael_bluth', username)

    def test_clean_username_false(self):
        # Instantiate the form with the same username as self.user
        form = MyUserCreationForm({
            'username': self.user.username,
            'first_name': 'Michael',
            'last_name': 'Bluth',
            'email': 'michael@bluth.com',
            'phone': '18005556666',
            'password1': '7jefB#f@Cc7YJB]2v',
            'password2': '7jefB#f@Cc7YJB]2v',
        })
        # Run is_valid() to trigger the validation, which is going to fail
        # because the username is already taken
        valid = form.is_valid()
        self.assertFalse(valid)

        # The form.errors dict should contain a single error called 'username'
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('username' in form.errors)
