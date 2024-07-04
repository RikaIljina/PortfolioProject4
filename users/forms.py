"""
forms.py for the 'Users' app.

This module contains the ProfileForm class that handles input by authenticated
users, allowing them to enter Profile object data and edit their user profile.
"""

from django import forms
from django.forms import FileInput, EmailInput, URLInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget
import cloudinary

from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form class for users to edit their profile

    Meta: Specifies the django model, fields, widgets, and labels.

    Methods:
        clean_pic(): Performs custom validation of the uploaded picture.
        save(): Overrides super method to deal with Cloudinary files.
    """

    class Meta:
        model = Profile
        fields = (
            "bio",
            "pic",
            "website",
            "email",
            "facebook",
            "twitter",
            "instagram",
            "youtube",
            "spotify",
        )
        widgets = {
            "bio": SummernoteWidget(
                attrs={
                    "rows": "3",
                    "class": "flex-fill form-control me-3",
                    "type": "text",
                    "name": "bio",
                }
            ),
            "pic": FileInput(attrs={"class": "flex-fill form-control me-3"}),
            "website": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "email": EmailInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "facebook": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "twitter": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "instagram": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "youtube": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
            "spotify": URLInput(
                attrs={"class": "flex-fill form-control me-3"}
            ),
        }

        labels = {
            "bio": _("About me"),
            "pic": _("Profile pic"),
            "website": _("Website"),
            "email": _("Email address"),
            "facebook": _("Facebook"),
            "twitter": _("Twitter"),
            "Instagram": _("Instagram"),
            "youtube": _("Youtube"),
            "spotify": _("Spotify"),
        }

    def save(self, commit=True):
        """
        Overrides superclass save method to handle Cloudinary file deletion

        Args:
            commit (bool, optional): If True, the changes are saved to the
            database. Defaults to True.

        Returns:
            Profile: The Profile model instance.
        """

        instance = self.instance

        if "pic" in self.changed_data:
            old_id = self.initial["pic"].public_id
            if old_id != "placeholder":
                # The response could be used to send an error message to the
                # admin if the file couldn't be destroyed
                cl_response = cloudinary.uploader.destroy(
                    old_id, invalidate=True
                )

        if commit:
            super().save()

        # Return the instance in case further modifications are needed in the
        # view
        return instance

    def clean_pic(self):
        """
        Validate image file before passing it on to Cloudinary

        This method performs a few basic checks before Cloudinary runs its own
        validation and attempts to upload the file.

        Raises:
            ValidationError: If content type is not image
            ValidationError: If the file is too large ( > 1MB )
            ValidationError: If none of the attributes could be read

        Returns:
            file (UploadedFile): An abstract uploaded file
        """

        file = self.cleaned_data.get("pic", False)
        if file and "cloudinary" not in str(type(file)):
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise ValidationError(
                    f"This is not an image file, please"
                    f" choose a valid file."
                )
            if file.size > 1 * 1024 * 1024:
                raise ValidationError(
                    f"The image file is too large. The"
                    f" maximum allowed size is 1MB."
                )
            return file
        elif "cloudinary" in str(type(file)):
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")
