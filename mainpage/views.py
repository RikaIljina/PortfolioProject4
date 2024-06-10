from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from .models import Entry, Like
from .forms import CommentForm
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries


# Views

def index(request):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    
    entries = get_published_entries(request, Entry.objects)
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
    print(request)

    return render(
        request,
        'mainpage/index.html',
        context)


def entry_details(request, slug):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    
    entry = get_object_or_404(get_published_entries(request, Entry.objects), slug=slug)

    users = get_username_list()
    tags = get_all_tags()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.entry = entry
            comment.save()
        print(request.POST)
            
    comment_form = CommentForm()

    context = {'entry': entry,
               'users': users,
               'tags': tags,
               'comment_form': comment_form,
               }

    return render(
        request,
        'mainpage/entry_details.html',
        context)


def filter_user(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    
    entries = get_published_entries(request, user.entries)
    entries, sorted_param = sort_by(request, entries)
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request, entries)
    
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'users': users,
               'user_filter': username,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def filter_tag(request, tag):
    entries = get_published_entries(request, Entry.objects).filter(tags__name__in=[tag])
    entries, sorted_param = sort_by(request, entries)
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request, entries)
        
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'tag_filter': tag,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'mainpage/index.html',
        context)
    

