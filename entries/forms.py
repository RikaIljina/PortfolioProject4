import json
import os
from datetime import datetime
from django import forms
from django.forms import TextInput, RadioSelect, FileInput, CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
from unidecode import unidecode
from django.utils.text import slugify


import cloudinary

from .models import Entry

from django.core.exceptions import ValidationError



class EntryForm(forms.ModelForm):
    """
    Form class for users to add a new entry
    
    The form contains the boolean field 'keep_file' that is not part of the
    Entry model. It allows users to keep uploaded files as previous versions
    when updating entries.
    
    keep_file (BooleanField): Optional checkbox
    
    Meta: Specifies the django model, fields, widgets and labels.
    
    Methods:
    __init__: Initializes the form with additional arguments
    clean_title: Performs custom validation of the entry title
    save: Overrides super method to deal with Cloudinary files
    """
    
    keep_file = forms.BooleanField(required=False, label='Keep previous file?')

    class Meta:
        """
        Specify the django model, the fields, widgets and labels
        """
        model = Entry
        fields = (
            'title', 'description', 'audio_file', 'tags', 'publish',
            'old_files')
        widgets = {
            "title": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "description": SummernoteWidget(
                attrs={"rows":"3", "class":"flex-fill form-control me-3",
                       "type":"text", "name":"description"}),
            "audio_file": FileInput(
                attrs={"class":"flex-fill form-control me-3"}),
            "tags": TextInput(attrs={"class":"flex-fill form-control me-3"}),
            "publish": RadioSelect(),
            "keep_file":  CheckboxInput(),
            }
        
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'audio_file': _('New audio file (mp3)'),
            'tags': _('Tags (comma-separated)'),
            'publish': _('Publicity'),
        }

    def __init__(self, *args, **kwargs):
        # Save user and new_file on form initialization, but remove them from
        # kwargs because the super init method is not expecting them
        self.user = kwargs.pop('user', None)
        self.new_file = kwargs.pop('new_file', None)
        super(EntryForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        """
        Validate the uniqueness of the title for entries by the same user.

        This method ensures that the title for an entry is unique among the
        entries created by the same user. Raises a ValidationError if the user
        has already used the same title for another entry.

        Returns:
            str: The validated title.

        Raises:
            forms.ValidationError: If the user has already used this title for
                another entry.
        """
        
        title = self.cleaned_data.get('title')
        instance = self.instance

        if Entry.objects.filter(
            author=self.user, title=title).exclude(id=instance.id).exists():
            raise forms.ValidationError(
                "You have already used this title for another entry. Please "
                "choose a different title.")
        else:
            new_slug = f'{title}-{self.user.username}'
            # unidecode is needed to process non-latin titles
            new_slug = slugify(unidecode(new_slug))
            
            if Entry.objects.filter(slug=new_slug).exclude(
                                                    id=instance.id).exists():
                print('Error!')
                raise ValidationError(
                    'Please choose a different title to make sure the entry '
                    'slug is unique.')
            else:
                instance = super(EntryForm, self).save(commit=False)
                instance.slug = new_slug
                print('Unique slug')
        
        return title
    
    # https://stackoverflow.com/a/6195691
    def clean_audio_file(self):
        """
        Validate audio file before passing it on to Cloudinary
        
        This method performs a few basic checks before Cloudinary runs its own
        validation and attempts to upload the file.

        Raises:
            ValidationError: If content type is not mpeg
            ValidationError: If the audio file is too large ( > 10MB )
            ValidationError: If none of the attributes could be read

        Returns:
            file (UploadedFile): An abstract uploaded file
        """
        file = self.cleaned_data.get('audio_file', False)
        print(type(file))
        if file and 'cloudinary' not in str(type(file)):
            print('checking stuff')
            if not file.content_type in ["audio/mpeg"]:
                print('checking type')                
                raise ValidationError("Content type is not mpeg")
            if file.size > 10*1024*1024:
                print('checking size')
                raise ValidationError("Audio file too large ( > 10MB )")

            return file
        elif 'cloudinary' in str(type(file)):
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")
         
         
    def save(self, commit=True):
        """
        Override superclass save method to handle Cloudinary files

        This project uses Cloudinary for uploaded file storage.
        Since replacing an uploaded file with a new file doesn't automatically
        delete the uploaded file in the cloud, this method handles the
        destruction of the file if it is no longer needed.
        The user can opt to keep the file as a previous version by checking
        the 'keep_file' checkbox. In that case, the file url is saved in the
        Entry model's JSON field 'old_files'.
        
        Args:
            commit (bool): If True, the changes are saved to the database. 
                Defaults to True.

        Returns:
            Entry: The saved Entry model instance.
        """
        
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        keep_file = self.data.get('keep_file')

        # new_file is only passed on from the edit_entry view
        if self.new_file and keep_file:
            old_id = self.initial['audio_file'].public_id
            json_date = json.dumps(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Add old file to the json object 'old_files' together with
            # a timestamp for ordering purposes
            instance.old_files[old_id] = [
                self.initial['audio_file'].url, json_date ]
        elif self.new_file:
            old_id = self.initial['audio_file'].public_id
            print(cloudinary.uploader.destroy(
                old_id, resource_type = "video", invalidate=True))

        if commit:
            instance.save()
            
        return instance
