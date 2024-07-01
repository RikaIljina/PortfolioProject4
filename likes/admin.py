"""
admin.py for the 'Likes' app.

This module registers the Like model on the admin page.
"""

from django.contrib import admin
from .models import Like


admin.site.register(Like)
