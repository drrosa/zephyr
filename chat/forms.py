from django.forms import ModelForm
from django import forms
from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "name": "message",
                    "placeholder": "Add message ...",
                    "class": "w-full h-20 p-4 rounded-xl",
                    "autofocus": True,
                    "autocomplete": "off",
                }
            )
        }
