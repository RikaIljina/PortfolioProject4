from django.contrib import admin, messages
from django_summernote.admin import SummernoteModelAdmin
import cloudinary

from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(SummernoteModelAdmin):

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


    def delete_queryset(self, request, queryset):
        """
        Override superclass method to delete Cloudinary files
        
        This method deletes the Cloudinary file in each of the queryset objects
        and logs the result as an info message. After deleting the Cloudinary 
        files, it calls the superclass method to delete the queryset from 
        the database.

        Args:
            request (HttpRequest): The HTTP request object that contains
                metadata about the request.
            queryset (QuerySet): The queryset of model instances to be deleted.
        """
    
        for obj in queryset:
            result = cloudinary.uploader.destroy(
                obj.pic.public_id, invalidate=True
            )
            messages.info(request, result)
        super().delete_model(request, queryset)
