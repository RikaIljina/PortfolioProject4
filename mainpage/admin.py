from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry, Comment, Like
from django.contrib.auth.models import User

# Register your models here.

@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'publish', 'audio_file')
    search_fields = ['title', 'author__username', 'tags__name']
    list_filter = ('publish', 'author', 'tags__name')
   # prepopulated_fields = {'slug': ('title', 'author')}
    summernote_fields = ('description',)


admin.site.register(Comment)

admin.site.register(Like)