from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry, Comment, Like
from django.contrib.auth.models import User
import cloudinary

# Register your models here.

@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'publish', 'audio_file')
    search_fields = ['title', 'author__username', 'tags__name']
    list_filter = ('publish', 'author', 'tags__name')
   # prepopulated_fields = {'slug': ('title', 'author')}
    summernote_fields = ('description',)
    
    # def save(self, *args, **kwargs):
    #     print('saving...')
    #     super().save(*args, **kwargs)

    # def delete_model(self, request, obj):
    #     print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
    #     super().delete_model(request, obj)
        
    # def delete_queryset(self, request, queryset):
    #     for obj in queryset:
    #         print(cloudinary.uploader.destroy(obj.audio_file.public_id, resource_type = "video", invalidate=True))
    #     super().delete_model(request, queryset)

admin.site.register(Comment)

admin.site.register(Like)