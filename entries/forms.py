import json
from datetime import datetime
from django import forms
from django.forms import TextInput, RadioSelect, FileInput, CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget
import cloudinary

from .models import Entry


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
    #tag_list = forms.CharField(required=False)

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
        Checks all titles by the same user to make sure they are unique

        Raises:
            forms.ValidationError: Message to show to user if form is invalid
        """
        
        title = self.cleaned_data.get('title')
        instance = self.instance

        if Entry.objects.filter(
            author=self.user, title=title).exclude(id=instance.id).exists():
            raise forms.ValidationError(
                "You have already used this title for another entry. Please"
                "choose a different title.")
        return title
    
    def save(self, commit=True):
        """
        Override super save method to handle Cloudinary files

        This project uses Cloudinary for uploaded file storage.
        Since replacing an uploaded file with a new file doesn't automatically
        delete the uploaded file in the cloud, this method handles the
        destruction of the file if it is no longer needed.
        The user can opt to keep the file as a previous version by checking
        the 'keep_file' checkbox. In that case, the file url is saved in the
        Entry model's json field 'old_files'.
        """
        
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        keep_file = self.data.get('keep_file')
        
        # What if new_file name and old_file name are the same??? check in admin
        # Isn't there always a new file even when creating a new entry??
        if self.new_file and keep_file:
            old_id = self.initial['audio_file'].public_id
            json_date = json.dumps(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Add old file to the json object 'old_files' together with
            # a timestamp for ordering purposes
            instance.old_files[old_id] = [
                self.initial['audio_file'].url, json_date ]
            instance.save()
        elif self.new_file:
            old_id = self.initial['audio_file'].public_id
            instance.save()
            print(cloudinary.uploader.destroy(
                old_id, resource_type = "video", invalidate=True))
            
        else:
            print('just saving in class')
            instance.save()
            
        if commit:
            print('saving in class with commit true')
            instance.save()
            
        return instance
