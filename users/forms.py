from django import forms
from django.forms import TextInput, Textarea, RadioSelect, FileInput, EmailInput, URLInput
from django.utils.translation import gettext_lazy as _
from cloudinary.forms import CloudinaryFileField
from django.core.exceptions import ValidationError

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
        fields = ('bio', 'pic', 'website', 'email', 'facebook', 'twitter', 'instagram', 'youtube', 'spotify')
        widgets = {
            "bio": SummernoteWidget(attrs={"rows":"3", "class":"flex-fill form-control me-3", "type":"text", "name":"bio"}),
            "pic": FileInput(attrs={"class":"flex-fill form-control me-3"}),
            "website": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "email": EmailInput(attrs={"class":"flex-fill form-control me-3"}),
            "facebook": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "twitter": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "instagram": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "youtube": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            "spotify": URLInput(attrs={"class":"flex-fill form-control me-3"}),
            
        }
        
        labels = {
            'bio': _('About me'),
            'pic': _('Profile pic'),
            'website': _('Website'),
            'email': _('Email address'),
            'facebook': _('Facebook'),
            'twitter': _('Twitter'),
            'Instagram': _('Instagram'),
            'youtube': _('Youtube'),
            'spotify': _('Spotify'),
            
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
    
    def clean_pic(self):
        file = self.cleaned_data.get('pic', False)
        print(type(file))
        if file and 'cloudinary' not in str(type(file)):
            print('checking stuff')
            # if not file.content_type in ["audio/mpeg"]:
            #     print('checking type')                
            #     raise ValidationError("Content type is not mpeg")
            if file.size > 1*1024*1024:
                print('checking size')
                raise ValidationError("Image file too large ( > 1MB )")

            return file
        elif 'cloudinary' in str(type(file)):
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")