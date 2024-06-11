from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from entries.models import Entry
from likes.models import Like

# Helper functions


def get_username_list():
    current_usernames = list(User.objects.values_list(
                'username', flat=True).order_by(Lower('username')))
    
    return current_usernames