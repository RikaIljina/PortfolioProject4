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


def get_published_entries(request, source, get_likes=True):
    if request.user.is_authenticated and get_likes:
        entries = source.filter(publish=1).annotate(already_liked=Count(
            'all_likes', filter=Q(all_likes__user = request.user)), likes_received=Count('all_likes'))
        print(f"Annotating: {request.user.liked}")
    else:
        entries = source.filter(publish=1)
        
    return entries