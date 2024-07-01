"""
forms.py for the 'Mainpage' app.

This module contains the MessageToAdminForm class that handles input by
authenticated users, allowing them to enter MessageToAdmin object data and
create and submit a new message to the admin.
"""

from django import forms
from django.forms import Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from .models import MessageToAdmin


class MessageToAdminForm(forms.ModelForm):
    """
    Form class for users to submit a new message to the admin

    Meta: Specifies the django model, fields, widgets, and labels.
    """

    class Meta:
        model = MessageToAdmin
        fields = (
            "subject",
            "message",
        )
        widgets = {
            "subject": TextInput(
                attrs={
                    "placeholder": "Max 200 characters",
                    "type": "text",
                    "name": "subject",
                }
            ),
            "message": Textarea(
                attrs={
                    "rows": "3",
                    "class": "flex-fill form-control me-3",
                    "placeholder": "Max 5000 characters",
                    "type": "text",
                    "name": "message",
                }
            ),
        }
        labels = {
            "subject": _("Subject"),
            "message": _("Your message"),
        }
