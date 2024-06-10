from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Entry, Comment, Like
from django.contrib.auth.models import User
import cloudinary

# Register your models here.

admin.site.register(Comment)

admin.site.register(Like)