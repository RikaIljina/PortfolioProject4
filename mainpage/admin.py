"""
admin.py for the 'Mainpage' app.

This module registers the MessageToAdmin model on the admin page.
"""

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import MessageToAdmin


# Register your models here.
@admin.register(MessageToAdmin)
class MessageToAdminAdmin(SummernoteModelAdmin):
    """
    Handle admin form and summary display for the MessageToAdmin model

    list_display: Fields to show in the admin list view of all entries
    search_fields: Fields to consider in the admin free text search
    list_filter: Fields to use as filter conditions
    """

    list_display = ("user", "subject", "created_on")
    search_fields = ["subject", "user__username", "message"]
    list_filter = (
        "created_on",
        "user",
    )
