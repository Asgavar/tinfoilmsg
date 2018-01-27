from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import ModelChoiceField

from .models import Algorithm


class AlgorithmForm(ModelForm):
    """
    A form corresponding to the Algorithm model, with the sender
    field hardcoded as the user currently logged in.
    """
    # TODO
    # sender = ModelChoiceField(queryset=User.objects.get)
    class Meta:
        model = Algorithm
        fields = ['receiver', 'red', 'green', 'blue', 'frequency']
