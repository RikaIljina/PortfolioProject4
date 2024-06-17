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
                "You have already used this title for another entry. Please"
                "choose a different title.")
        return title
    
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
