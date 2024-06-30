"""
forms.py for the 'Entries' app.

This module contains the form class that handles the input by authenticated
users, allowing them to enter Entry object data and create a new entry.
"""

from django import forms
from django.forms import TextInput, RadioSelect, FileInput, CheckboxInput
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget
import json
from datetime import datetime
from unidecode import unidecode
import cloudinary

from .models import Entry

class EntryForm(forms.ModelForm):
    """
    Form class for users to add a new entry

    The form contains the boolean field 'keep_file' that is not part of the
    Entry model. It allows users to keep uploaded files as previous versions
    when updating entries.

    Attributes:
        keep_file (BooleanField): Optional checkbox
        user (User object): The user making the request
        new_file (TemporaryUploadedFile): The file selected by the user for
            upload

    Meta: Specifies the django model, fields, widgets, and labels.

    Methods:
        clean_title(): Performs custom validation of the entry title.
        clean_audio_file(): Performs custom validation of the uploaded file.
        save(): Overrides super method to deal with Cloudinary files.
    """

    keep_file = forms.BooleanField(required=False, label="Keep previous file?")

    class Meta:
        """
        Specify the django model, the fields, widgets, and labels
        """

        model = Entry
        fields = (
            "title",
            "description",
            "audio_file",
            "tags",
            "publish",
            "old_files",
        )
        widgets = {
            "title": TextInput(attrs={"class": "flex-fill form-control me-3"}),
            "description": SummernoteWidget(
                attrs={
                    "rows": "3",
                    "class": "flex-fill form-control me-3",
                    "type": "text",
                    "name": "description",
                }
            ),
            "audio_file": FileInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "tags": TextInput(attrs={"class": "flex-fill form-control me-3"}),
            "publish": RadioSelect(),
            "keep_file": CheckboxInput(),
        }

        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "audio_file": _("New audio file (mp3)"),
            "tags": _("Tags (comma-separated)"),
            "publish": _("Publicity"),
        }


    def __init__(self, *args, **kwargs):
        # Save user on form initialization, but remove it from kwargs because
        # the super init method is not expecting it
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


    def clean_title(self):
        """
        Validate the uniqueness of the entry's slug

        This method ensures that the slug for an entry is unique among all
        entries in the database. Raises a ValidationError if the slug already
        exists and prompts the user to choose a different title.
        If the slug is valid, it is saved in the instance.

        Returns:
            str: The validated title.

        Raises:
            ValidationError: If the user has already used this title for
                another entry.
        """

        instance = self.instance
        title = self.cleaned_data.get("title")
        new_slug = f"{title}-{self.user.username}"
        # unidecode is needed to process non-latin titles
        new_slug = slugify(unidecode(new_slug))

        if (
                Entry.objects.filter(slug=new_slug)
                .exclude(id=instance.id)
                .exists()
            ):
            raise ValidationError(
                "Please choose a different title to make sure the entry link"
                " is unique."
                )
        else:
            instance.slug = new_slug

        return title

    # Adapted from https://stackoverflow.com/a/6195691
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
            file (TemporaryUploadedFile): File uploaded to a temporary location
        """
        
        file = self.cleaned_data.get("audio_file", False)

        if file and "cloudinary" not in str(type(file)):
            if not file.content_type in ["audio/mpeg"]:
                raise ValidationError(f"This is not an mp3 file, please choose"
                                      f" a valid file.")
            if file.size > 10 * 1024 * 1024:
                raise ValidationError(f"The audio file is too large. The"
                                      f" maximum allowed size is 10MB.")
            return file
        elif "cloudinary" in str(type(file)):
            return file
        else:
            raise ValidationError("Couldn't read the uploaded file")


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
            Entry: The Entry model instance.
        """

        # For some reason, entry_form.save_m2m() doesn't work in the view if
        # instance = self.instance is used instead of the following line,
        # even if the view initializes the instance with
        # entry_form.save(commit=False).
        # I have yet to figure out the reason for this.
        instance = super().save(commit=False)
        instance.author = self.user
        keep_file = self.data.get("keep_file")

        if 'audio_file' in self.changed_data and keep_file:
            old_id = self.initial["audio_file"].public_id
            json_date = json.dumps(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            # Add old file to the json object 'old_files' together with
            # a timestamp for ordering purposes
            instance.old_files[old_id] = [
                self.initial["audio_file"].url,
                json_date,
            ]
        elif 'audio_file' in self.changed_data:
            old_id = self.initial["audio_file"].public_id
            # The response could be used to send an error message to the admin
            # if the file couldn't be destroyed
            cl_response = cloudinary.uploader.destroy(
                    old_id, resource_type="video", invalidate=True
                )

        if commit:
            super().save()

        # Return the instance in case further modifications are needed in the
        # view
        return instance
