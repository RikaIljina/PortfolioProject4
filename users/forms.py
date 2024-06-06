from django import forms
from django.forms import TextInput, EmailInput, Textarea
from mainpage.models import Entry
from cloudinary.forms import CloudinaryFileField
from django.utils.translation import gettext_lazy as _


class EntryForm(forms.ModelForm):
    """
    Form class for users to add a new entry 
    """
        
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Entry
        fields = ('title', 'description', 'audio_file', 'tags', 'publish')
        widgets = {
            "description": Textarea(attrs={"rows":"3", "class":"flex-fill form-control me-3", "placeholder":"Add comment", "type":"text", "name":"comment"}),
        }
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'audio_file': _('Audio file (mp3)'),
            'tags': _('Tags (comma-separated)'),
            'publish': _('Publicity'),
        }