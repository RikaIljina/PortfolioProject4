from django import forms
from django.forms import Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from .models import MessageToAdmin


class MessageToAdminForm(forms.ModelForm):

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


# class CommentForm(forms.ModelForm):
#     """
#     Form class for users to comment on a post
#     """

#   #  content = forms.TextInput(widget=forms.TextInput(attrs={'class':'flex-fill form-control me-3'}))

#     class Meta:
#         """
#         Specify the django model and order of the fields
#         """
#         model = Comment
#         fields = ('content',)
#         widgets = {
#             "content": Textarea(attrs={"rows":"3", "class":"flex-fill form-control me-3", "placeholder":"Add comment", "type":"text", "name":"comment"}),
#         }
#         labels = {
#             'content': _('Your comment'),
#         }
