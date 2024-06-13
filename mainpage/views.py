from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from likes.models import Like
from entries.models import Entry

from comments.forms import CommentForm
from mainpage.utils import get_all_tags, get_page_obj, sort_by
from users.utils import get_username_list, get_users_from_file
from entries.utils import get_published_entries


# Views

def index(request):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    # if request.user.is_authenticated:
    #     profile = request.user.profile
    # else:
    #     profile = None

    entries = get_published_entries(request, Entry.objects, get_comments=False)
    entries, sorted_param = sort_by(request, entries)

    page_obj = get_page_obj(request, entries)
    
    #users = get_username_list()    
    users = get_users_from_file()
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


def filter_user(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    
    entries = get_published_entries(request, user.all_entries, get_comments=False)
    entries, sorted_param = sort_by(request, entries)
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request, entries)
    
    page_obj = get_page_obj(request, entries)
    #users = get_username_list()
    users = get_users_from_file()
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
    entries = get_published_entries(request, Entry.objects, get_comments=False).filter(tags__name__in=[tag])
    entries, sorted_param = sort_by(request, entries)
   # print(entries[0].tags.__dict__)
   # Tag.objects.all().prefetch_related('entries')
   # print(Tag.objects.all().filter(name=tag).__dict__)# _meta.get_fields())
   # tag_obj = get_object_or_404(Tag, pk=Tag.objects.filter(name=tag).first().pk) #.pk=tag.pk)
   # tagged = Entry.objects.filter(tag=tag_obj)
   # print(tagged)
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request, entries)
        
    page_obj = get_page_obj(request, entries)
    #users = get_username_list()
    users = get_users_from_file()
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
    

