from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from mainpage.models import Entry

# Helper functions

def get_page_obj(request, entries):
    paginator = Paginator(entries, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

def get_username_list():
    current_usernames = list(User.objects.values_list(
                'username', flat=True).order_by(Lower('username')))
    
    return current_usernames

def get_all_tags():
    tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
        entry__publish=1), distinct=True)).filter(amount__gt=0).order_by('name')

    return tags

def sort_by(request, entries):
    if request.GET.get('sorted') == 'by_likes':
        entries = entries.order_by('-likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'
    else:
        sorted_param = ''
    print(request.GET)
    if 'tag' in request.GET:
        print("Tag found!")
    
    return entries, sorted_param

def get_published_entries():
    return Entry.objects.filter(publish=1)