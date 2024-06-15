from django import forms
from django.contrib import admin, messages
from django_summernote.admin import SummernoteModelAdmin
from datetime import datetime
import cloudinary
import json

from .models import Entry

class EntryFormExtension(forms.ModelForm):
    """
    Extend admin form with additional fields

    This class extends the Entry form shown on the Django Admin page by a
    checkbox. When updating an entry, the admin can check this box to make sure
    the link to previously uploaded file is saved in the Entry model instance
    and not deleted from Cloudinary.
    """

    keep_file = forms.BooleanField(required=False, label='Keep previous file?')

    class Meta:
        model = Entry
        fields = '__all__'


@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):
    """
    Handles admin form and summary display for the Entry model
    
    list_display: Fields to show in the admin list view of all entries
    search_fields: Fields to consider in the admin free text search
    list_filter: Fields to use as filter conditions
    summernote_fields: Fields that use Summernote extension for richtext
    
    Methods:
    get_form: Overrides super method to extend class with EntryFormExtension
    save_model: Overrides super method to handle Cloudinary files when editing
    delete_queryset: Overrides super method to delete uploaded Cloudinary files
    """
    
    list_display = ('title', 'slug', 'publish', 'created_on', 'updated_on')
    search_fields = ['title', 'author__username', 'tags__name']
    list_filter = ('publish', 'author', 'tags__name', 'created_on',
                   'updated_on')
    summernote_fields = ('description',)
    
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Extends super class with EntryFormExtension, adding a checkbox

        Args:
            request (_type_): _description_
            obj (_type_, optional): _description_. Defaults to None.
        """
        
        kwargs['form'] = EntryFormExtension
        return super().get_form(request, obj, **kwargs)
    
    # TODO: Allow admin to delete individual old files
    
    def save_model(self, request, obj, form, change):
        """
        Overrides super method to handle Cloudinary files when editing
        
        This project uses Cloudinary for uploaded file storage.
        Since replacing an uploaded file with a new file doesn't automatically
        delete the uploaded file in the cloud, this method handles the
        destruction of the file if it is no longer needed.
        The admin and the user can opt to keep the file as a previous version
        by checking the 'keep_file' checkbox. In that case, the file url is
        saved in the Entry model's json field 'old_files'.

        Args:
            request (_type_): _description_
            obj (_type_): _description_
            form (_type_): _description_
            change (_type_): _description_
        """

        # Get checkbox value
        keep_file = form.data.get('keep_file')
        # Better?
        old_file = obj.audio_file
        #old_file = form.initial.get('audio_file')
        new_file = form.cleaned_data['audio_file']
        old_id = old_file.public_id

        # Just ask if new_file ??
        if old_file != new_file and not keep_file:
            print('file has changed')
            result = cloudinary.uploader.destroy(
                old_id, resource_type = "video", invalidate=True)
            messages.info(result)
        elif old_file != new_file:
            instance = form.save(commit=False)
            json_date = json.dumps(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Add old file to the json object 'old_files' together with
            # a timestamp for ordering purposes
            instance.old_files[old_id] = [
                form.initial['audio_file'].url, json_date]
            
        super().save_model(request, obj, form, change)

  
    def delete_queryset(self, request, queryset):
        """
        Overrides super method to delete uploaded Cloudinary files in bulk
        
        When deleting multiple objects at once in the admin panel, the 'delete'
        method of the Entry class is not being called. Therefore, this method
        is needed to delete the main audio file as well as all previous
        versions of the file from the Cloudinary storage for every deleted
        Entry object.

        Args:
            request (_type_): _description_
            queryset (_type_): _description_
        """
        
        for obj in queryset:
            result = cloudinary.uploader.destroy(
                obj.audio_file.public_id, resource_type = "video",
                invalidate=True)
            for id, file in obj.old_files.items():
                result_old = cloudinary.uploader.destroy(
                    id, resource_type = "video", invalidate=True)
                messages.info(result_old)
            messages.info(result)

        super().delete_model(request, queryset)
