from django.test import Client
from django.test import TestCase


class AuthenticationTests(TestCase):
    """
    Signup and Login views are being tested here.
    """
    def setUp(self):
        self.client = Client()
        self.user_name = 'user'
        # also assures that NumericPasswordValidator is off
        self.user_password = '1234'

    def test_signup_does_not_produce_errors(self):
        response = self.client.post('/signup',data={
            'id_username': self.user_name,
            'id_password1': self.user_password  # what is this '1'?
        })
        # error string(s) seem(s) to be bytes, not strings
        self.assertEqual(self.client.errors.read(1024), b'')

    def test_login_does_not_produce_errors(self):
        response = self.client.post('/signup', data={
            'is_username': self.user_name,
            'id_password': self.user_password
        })
        self.assertEqual(self.client.errors.read(1024), b'')
