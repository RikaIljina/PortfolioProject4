from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry, Comment, Like
from django.contrib.auth.models import User
import cloudinary

# Register your models here.

@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'publish', 'created_on', 'updated_on')
    search_fields = ['title', 'author__username', 'tags__name']
    list_filter = ('publish', 'author', 'tags__name', 'created_on', 'updated_on')
   # prepopulated_fields = {'slug': ('title', 'author')}
    summernote_fields = ('description',)
    
    def save_model(self, request, obj, form, change):
        print('saving audio in admin...')
        print(form.cleaned_data['audio_file'])
        #print(form.initial['audio_file'])
        old_file = form.initial.get('audio_file')
        print(old_file)
        if old_file:
            old_file = old_file.public_id
            print(f'file id {old_file}')
            if old_file != form.cleaned_data['audio_file']:
                print('file has changed')
                print(cloudinary.uploader.destroy(old_file, resource_type = "video", invalidate=True))
        super().save_model(request, obj, form, change)

    # def delete_model(self, request, obj):
    #     print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
    #     super().delete_model(request, obj)
        
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
        super().delete_model(request, queryset)

admin.site.register(Comment)

admin.site.register(Like)