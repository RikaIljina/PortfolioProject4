from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Profile

# Register your models here.
admin.site.register(Profile)