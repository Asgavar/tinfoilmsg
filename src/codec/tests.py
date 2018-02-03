import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from tinfoilmsg import settings

from .models import Algorithm


class AlgorithmModelValidationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='validationtestuser',
            password='AndH1sPassword'
        )
        self.user2 = User.objects.create_user(
            username='validationUsersColleague',
            password='s3cr3t'
        )

    def test_negative_frequency_fails(self):
        with self.assertRaises(ValidationError):
            invalid_algorithm = Algorithm(
                sender=self.user1, receiver=self.user2, red=True, green=False,
                blue=True, frequency=-777
            )
            invalid_algorithm.full_clean()

    def test_no_color_selected_fails(self):
        with self.assertRaises(ValidationError):
            another_invalid_algorithm = Algorithm(
                sender=self.user1, receiver=self.user2, red=False, green=False,
                blue=False, frequency=4
            )
            another_invalid_algorithm.full_clean()

    def test_repeteated_users_pair_fails(self):
        correct_and_valid1 = Algorithm(
            sender=self.user1, receiver=self.user2, red=True, green=True,
            blue=True, frequency=123
        )
        correct_and_valid2 = Algorithm(
            sender=self.user1, receiver=self.user2, red=True, green=False,
            blue=True, frequency=321
        )
        correct_and_valid1.save()
        with self.assertRaises(ValidationError):
            correct_and_valid2.full_clean()


class FunctionalityTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='functionalitytestuser',
            password='AndH1sPassword'
        )
        self.user2 = User.objects.create_user(
            username='colleagueoftheonementionedbefore',
            password='s3cr3t'
        )
        Algorithm.objects.create(
            sender=self.user1,
            receiver=self.user2,
            red=True,
            green=True,
            blue=True,
            frequency=2048
        )

    @override_settings(DEBUG=True, MEDIA_ROOT=settings.MEDIA_ROOT)
    def test_encode_encodes_and_then_decode_decodes(self):
        client = Client()
        # password field contains a hash now, not a password
        client.login(username=self.user1.username, password='AndH1sPassword')
        msg_to_convey = 'please, do not tell anyone!'
        encode_payload = {
            'message_receiver': self.user2.id,
            'message_text': msg_to_convey
        }
        encoded_response = client.post('/encode/results/', encode_payload, follow=True)
        filename = encoded_response.context['image']
        # user1 logs out, user2 logs in
        client.logout()
        client.login(username=self.user2.username, password='s3cr3t')
        file_handle = open(settings.MEDIA_ROOT + filename, 'rb')
        decode_payload = {
            'image_sender': self.user1.id,
            'image_file': file_handle
        }
        hopefully_decoded_response = client.post('/decode/results/', decode_payload)
        decoded_msg_pattern = r'<p id="decoded">(.+)</p>'
        decoded_msg = re.search(decoded_msg_pattern,
                hopefully_decoded_response.content.decode('utf-8')).groups(0)
        self.assertEqual(decoded_msg[0], msg_to_convey)
