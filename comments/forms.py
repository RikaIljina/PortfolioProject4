from django import forms
from django.forms import TextInput, EmailInput, Textarea
from .models import Comment
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    """ Form class for users to comment on an entry

    The comment form consists of only one input field for the comment text.
    """

    class Meta:
        """ Django model and order of the fields
        """
        model = Comment
        fields = ('content',)
        widgets = {
            "content": Textarea(attrs={"rows": "3",
                                       "class": "flex-fill form-control me-3",
                                       "placeholder": "Add comment",
                                       "type": "text",
                                       "name": "comment"}),
        }
        labels = {
            'content': _('Your comment'),
        }
