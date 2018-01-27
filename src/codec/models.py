from django.contrib.auth.models import User
from django.db import models

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
