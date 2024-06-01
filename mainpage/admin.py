from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Profile, Entry, Comment, Like

# Register your models here.
admin.site.register(Profile)

@admin.register(Entry)
class EntryAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'publish', 'audio_file')
    search_fields = ['title',]
    list_filter = ('publish',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)


admin.site.register(Comment)

admin.site.register(Like)