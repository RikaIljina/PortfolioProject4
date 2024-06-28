from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User
from .models import MessageToAdmin

# Register your models here.
@admin.register(MessageToAdmin)
class MessageToAdminAdmin(SummernoteModelAdmin):
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
    
    list_display = ('user', 'subject', 'created_on')
    search_fields = ['subject', 'user__username', 'message']
    list_filter = ('created_on', 'user',)
 

