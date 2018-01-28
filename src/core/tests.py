from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase


class AuthenticationTests(TestCase):
    """
    Signup and Login views are being tested here.
    """
    def setUp(self):
        self.client = Client()
        self.user_name = 'testuser'
        self.user_password = '1234'

    def test_signup_procedure(self):
        post_data = {
            'username': self.user_name,
            'password1': self.user_password,
            'password2': self.user_password
        }
        response = self.client.post('/signup/', data=post_data)
        self.assertRedirects(response, '/')

    def test_logout_button_is_visible_after_login(self):
        User.objects.create_user(username=self.user_name, password=self.user_password)
        post_data = {
            'username': self.user_name,
            'password': self.user_password
        }
        response = self.client.post('/login/', data=post_data, follow=True)
        self.assertRedirects(response, '/')
        self.assertContains(response, 'Log out')
