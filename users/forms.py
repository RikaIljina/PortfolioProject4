from django import forms
from django.forms import TextInput, Textarea, RadioSelect, FileInput, EmailInput, URLInput
from django.utils.translation import gettext_lazy as _
from cloudinary.forms import CloudinaryFileField
from django_summernote.widgets import SummernoteWidget
import cloudinary

from entries.models import Entry

from .models import Profile

        
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
            "bio": SummernoteWidget(attrs={"rows":"3", "class":"flex-fill form-control me-3", "type":"text", "name":"bio"}),
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
        
    def __init__(self, *args, **kwargs):
        print("initializing profile")
        self.new_file = kwargs.pop('new_file', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        print('entering class')
        instance = super(ProfileForm, self).save(commit=False)
        print(f'Instance in save: {instance}')
    
        if self.new_file:
            old_id = self.initial['pic'].public_id
            #old_id = Profile.objects.get(id=instance.id).pic.public_id
            print(f'changed file: {self.new_file}, old: {old_id}')
            instance.save()
            print(cloudinary.uploader.destroy(old_id, invalidate=True))
            # print(cloudinary.uploader.destroy(self.old_id, resource_type = "video", invalidate=True))
        else:
            print('just saving in class')
            instance.save()
            
        if commit:
            print('saving in class with commit true')
            instance.save()

        return instance