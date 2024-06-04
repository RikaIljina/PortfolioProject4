from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from .models import Entry
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries

# Helper functions

# def get_page_obj(request, entries):
#     paginator = Paginator(entries, 2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return page_obj

# def get_username_list():
#     current_usernames = list(User.objects.values_list(
#                 'username', flat=True).order_by(Lower('username')))
    
#     return current_usernames

# def get_all_tags():
#     tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
#         entry__publish=1), distinct=True)).filter(amount__gt=0).order_by('name')

#     return tags

# def sort_by(request, entries):
#     if request.GET.get('sorted') == 'by_likes':
#         entries = entries.order_by('-likes')
#         sorted_param = '?sorted=by_likes'
#     elif request.GET.get('sorted') == 'by_date':
#         entries = entries.order_by('-created_on')
#         sorted_param = '?sorted=by_date'
#     else:
#         sorted_param = ''
#     print(request.GET)
#     if 'tag' in request.GET:
#         print("Tag found!")
    
#     return entries, sorted_param

# def get_published_entries():
#     return Entry.objects.filter(publish=1)

# Views

def index(request):
    entries = get_published_entries()
    entries, sorted_param = sort_by(request, entries)

    page_obj = get_page_obj(request, entries)
    
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'sorted_param': sorted_param,
               'page_obj': page_obj,
               'users': users,
               'tags': tags,
               }
    print(request.path)

    return render(
        request,
        'mainpage/index.html',
        context)


def entry_details(request, slug):
    entry = get_object_or_404(get_published_entries(), slug=slug)
    users = get_username_list()
    tags = get_all_tags()

    print(entry.tags.all()[0])
    
    context = {'entry': entry,
               'users': users,
               'tags': tags,
               }

    return render(
        request,
        'mainpage/entry_details.html',
        context)


def filter_user(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    
    entries = user.entries.filter(publish=1)
    entries, sorted_param = sort_by(request, entries)
    
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def filter_tag(request, tag):
    entries = get_published_entries().filter(tags__name__in=[tag])
    entries, sorted_param = sort_by(request, entries)
    
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'mainpage/index.html',
        context)
    

