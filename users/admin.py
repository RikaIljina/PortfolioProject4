"""
admin.py for the 'Users' app.

This module registers the User model on the admin page.
"""

from django.contrib import admin, messages
from django_summernote.admin import SummernoteModelAdmin
import cloudinary

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(SummernoteModelAdmin):
    """
    Handle admin form and summary display for the Profile model

    list_display: Fields to show in the admin list view of all entries
    search_fields: Fields to consider in the admin free text search
    list_filter: Fields to use as filter conditions
    summernote_fields: Fields with richtext functionality

    Methods:
        save_model(): Overrides superclass method to delete replaced Cloudinary
            image file.
    """

    list_display = (
        "user",
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
    search_fields = [
        "user__username",
        "bio",
    ]
    list_filter = ("user", "joined")
    summernote_fields = ("bio",)

    def save_model(self, request, obj, form, change):
        """
        Override superclass method to delete replaced Cloudinary image file

        This method deletes the old Cloudinary image file if a new image has
        been added to the form and logs the result as an info message.
        After deleting the Cloudinary file, it calls the superclass method to
        save the model.

        Args:
            request (HttpRequest): The HTTP request object containing metadata
                about the request.
            obj (Entry): The model instance being saved. Represents the Profile
                being edited.
            form (ModelForm): The form instance with the submitted data.
            change (bool): A flag indicating whether the object is being
                changed (True) or created (False).
        """

        old_pic = form.initial.get("pic")
        if old_pic:
            old_pic = old_pic.public_id
            if old_pic != form.cleaned_data["pic"]:
                result = cloudinary.uploader.destroy(old_pic, invalidate=True)
                messages.info(request, result)

        super().save_model(request, obj, form, change)
