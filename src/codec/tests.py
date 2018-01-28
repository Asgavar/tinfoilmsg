from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

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
