from django import forms
from django.forms import TextInput, Textarea, RadioSelect, FileInput, EmailInput, URLInput
from django.utils.translation import gettext_lazy as _
from cloudinary.forms import CloudinaryFileField

from mainpage.models import Entry
from .models import Profile


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
            "title": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "description": Textarea(attrs={"rows":"3", "class":"flex-fill form-control me-3", "type":"text", "name":"description"}),
            "audio_file": FileInput(attrs={"class":"flex-fill form-control me-3"}),
            "tags": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "publish": RadioSelect(),
        }
        
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'audio_file': _('Audio file (mp3)'),
            'tags': _('Tags (comma-separated)'),
            'publish': _('Publicity'),
        }
        
        
class ProfileForm(forms.ModelForm):
    """
    Form class for users to edit their profile 
    """

    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Profile
        fields = ('bio', 'pic', 'social', 'email')
        widgets = {
            "bio": Textarea(attrs={"rows":"3", "class":"flex-fill form-control me-3", "type":"text", "name":"bio"}),
            "pic": FileInput(attrs={"class":"flex-fill form-control me-3"}),
            "social": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "email": EmailInput(attrs={"class":"flex-fill form-control me-3"}),
        }
        
        labels = {
            'bio': _('About me'),
            'pic': _('Profile pic'),
            'social': _('Social link'),
            'email': _('Email address'),
        }