"""
admin.py for the 'Comments' app.

This module registers the Comment model on the admin page.
"""

from django.contrib import admin
from .models import Comment


admin.site.register(Comment)
