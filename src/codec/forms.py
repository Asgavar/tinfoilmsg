from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import ModelChoiceField

from .models import Algorithm


class AlgorithmForm(ModelForm):
    """
    A form corresponding to the Algorithm model, with the sender
    field hardcoded as the user currently logged in.
    """
    class Meta:
        model = Algorithm
        fields = ['sender', 'receiver', 'red', 'green', 'blue', 'frequency']
        # sender field will be overwritten anyways
        widgets = {'sender': forms.HiddenInput()}


class EncodeForm(forms.Form):
    # queryset will be updated in __init__
    message_receiver = forms.ModelChoiceField(User.objects.none())
    message_text = forms.CharField()

    def __init__(self, possible_receivers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_receiver'].queryset = possible_receivers


class DecodeForm(forms.Form):
    pass
