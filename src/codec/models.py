from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Algorithm(models.Model):
    """
    A behaviour scheme connecting two users, distinguishing between the one
    who sends and the one who receives a message.
    """
    # CASCADE means that once the user account gets deleted all of his
    # algorithms are also removed
    sender = models.ForeignKey(User, models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, models.CASCADE, related_name='receiver')
    red = models.BooleanField()
    green = models.BooleanField()
    blue = models.BooleanField()
    frequency = models.IntegerField()

    def clean(self):
        """
        Performs form validation, checks if:
        1) sender-receiver pair does not already exist in the database
        2) frequency field is greater than zero
        3) at least one color channel is selected
        """
        super().clean()
        print(self.sender)
        print(self.receiver)
        sr_pair_query = Q(sender=self.sender) & Q(receiver=self.receiver)
        if Algorithm.objects.filter(sr_pair_query).count() != 0:
            raise ValidationError(
                'An algorithm connecting these two users already exists!',
                code='pair_exists'
            )
        if self.frequency <= 0:
            raise ValidationError(
                'Frequency parameter must be greater than zero!',
                code='frequency_le_zero'
            )
        if not (self.red or self.green or self.blue):
            raise ValidationError(
                'At least one color channel must be selected!',
                code='no_color_selected'
            )
