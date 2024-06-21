from django import forms
from django.contrib import admin, messages
from django_summernote.admin import SummernoteModelAdmin
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, reverse, redirect
from datetime import datetime
from unidecode import unidecode
import cloudinary
import json

from .models import Entry

class EntryFormExtension(forms.ModelForm):
    """
    Extend admin form with additional fields

    This class extends the Entry form shown on the Django Admin page by a
    checkbox. When updating an entry, the admin can check this box to make sure
    the link to a previously uploaded file is saved in the Entry model instance
    and not deleted from Cloudinary.
    """

    keep_file = forms.BooleanField(required=False, label='Keep previous file?')

    class Meta:
        model = Entry
        fields = '__all__'
        
    def clean(self):
        print('cleaning')
        instance = self.save(commit=False)
        new_slug = f'{self.cleaned_data['title']}-{self.cleaned_data['author'].username}'
        # unidecode is needed to process non-latin titles
        new_slug = slugify(unidecode(new_slug))
        print(new_slug)
        if Entry.objects.filter(slug=new_slug).exclude(
                                                id=instance.id).exists():
            raise ValidationError(
                'Please choose a different title to make sure the entry '
                'slug is unique.')
        else:
            instance.slug = new_slug
    
        super(EntryFormExtension, self).clean()


@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):
    """
    Handle admin form and summary display for the Entry model
    
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
        Customize admin form to add a checkbox

        Args:
            request (HttpRequest): The HTTP request object containing metadata 
                about the request.
            obj (Entry, optional): The model instance being modified.
                Defaults to None.

        Returns:
            Form: The customized form class to be used in the admin interface.
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
        The admin can opt to keep the file as a previous version by checking
        the 'keep_file' checkbox. In that case, the file url is saved in the
        Entry model's json field 'old_files'.

        Args:
            request (HttpRequest): The HTTP request object containing metadata
                about the request.
            obj (Entry): The model instance being saved. Represents the Entry
                being edited.
            form (ModelForm): The form instance with the submitted data.
            change (bool): A flag indicating whether the object is being
                changed (True) or created (False).
        """
        
        instance = form.save(commit=False)

       # new_slug = f'{form.cleaned_data['title']}-{form.cleaned_data['author'].username}'
        # unidecode is needed to process non-latin titles
       # new_slug = slugify(unidecode(new_slug))
        
        # if Entry.objects.filter(slug=new_slug).exclude(
        #                                         id=instance.id).exists():
        #     print(request.path)
            
        #     print('path Error!')
        #     print(request.path)
        #     redirect('admin')
        #     messages.error('The title is not unique')
        
            
        #     raise ValidationError(
        #         'Please choose a different title to make sure the entry '
        #         'slug is unique.')
        # else:
       # instance.slug = new_slug
       # print('Unique slug')
            
        # Get checkbox value
        keep_file = form.data.get('keep_file')
        old_file = form.initial.get('audio_file')
        new_file = form.cleaned_data['audio_file']
        if old_file:
            old_id = old_file.public_id

            # Potential BUG: If for some reason the new_file has the same name as
            # the cloudinary id, the following logic won't work
            if old_file != new_file and not keep_file:
                result = cloudinary.uploader.destroy(
                    old_id, resource_type = "video", invalidate=True)
                messages.info(request, result)
            elif old_file != new_file and keep_file:
                json_date = json.dumps(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # Add old file to the json object 'old_files' together with
                # a timestamp for ordering purposes
                instance.old_files[old_id] = [
                    old_file.url, json_date]
                
        #instance.save()

        super().save_model(request, obj, form, change)

  
    def delete_queryset(self, request, queryset):
        """
        Overrides super method to delete uploaded Cloudinary files in bulk
        
        When deleting multiple objects at once in the admin panel, the 'delete'
        method of the Entry class is not being called. This method ensures that
        the main audio file as well as all previous versions of the file are
        deleted from Cloudinary storage for each deleted Entry object.

        Args:
            request (HttpRequest): The HTTP request object containing metadata
                about the request.
            queryset (QuerySet): The queryset containing the Entry objects to
                be deleted.
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
