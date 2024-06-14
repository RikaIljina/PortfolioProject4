from django import forms
from django.contrib import admin
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
    the previously uploaded file is saved 
    """

    keep_file = forms.BooleanField(required=False, label='Keep previous file?')

    class Meta:
        model = Entry
        fields = '__all__'


@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):
    
    list_display = ('title', 'slug', 'publish', 'created_on', 'updated_on')
    search_fields = ['title', 'author__username', 'tags__name']
    list_filter = ('publish', 'author', 'tags__name', 'created_on',
                   'updated_on')
    summernote_fields = ('description',)
    
    
    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = EntryFormExtension
        return super().get_form(request, obj, **kwargs)
    
    # TODO: Allow admin to delete individual old files
    
    def save_model(self, request, obj, form, change):
        print('saving audio in admin...')
        keep_file = form.data.get('keep_file')
        old_file = form.initial.get('audio_file')
        new_file = form.cleaned_data['audio_file']
        old_id = old_file.public_id
        
        if old_file != new_file and not keep_file:
            print('file has changed')
            print(cloudinary.uploader.destroy(old_id, resource_type = "video", invalidate=True))
        elif old_file != new_file:
            json_date = json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            instance = form.save(commit=False)
            print( instance.old_files)
            instance.old_files[old_id] = [form.initial['audio_file'].url, json_date]
            print( instance.old_files)
            
        super().save_model(request, obj, form, change)

  
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
            for id, file in obj.old_files.items():
                print(cloudinary.uploader.destroy(id, resource_type = "video", invalidate=True))
        super().delete_model(request, queryset)
