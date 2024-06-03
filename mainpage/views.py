from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from taggit.models import Tag

from .models import Entry
from .signals import current_usernames

# Helper functions

def get_page_obj(request, entries):
    paginator = Paginator(entries, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_all_tags():
    tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
        entry__publish=1), distinct=True)).filter(amount__gt=0).order_by('name')

    return tags


# Views

def index(request):
    entries = Entry.objects.all().filter(publish=1)
    sorted_param = ''
    users = current_usernames
    
    tags = get_all_tags()

    if request.GET.get('sorted') == 'by_likes':
        entries = entries.order_by('-likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'

    # tag_names = dict()
    # for tag in tags:
    #     tag_names[tag.name] = entries.filter(
    #         tags__name__in=[tag.name]).distinct().count()
    # print(tag_names)
    # print(entries.filter(tags__name__in=['guitar']).count())
        # Entry.objects.filter(
        # tags__name__in=[tag.name]).distinct().count())
    # print(tags.__dir__())

    page_obj = get_page_obj(request, entries)

    context = {'entries': entries,
               'sorted_param': sorted_param,
               'page_obj': page_obj,
               'users': users,
               'tags': tags,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def entry_details(request, slug):
    entry = get_object_or_404(Entry.objects.filter(publish=1), slug=slug)
   # users = get_all_users()
    users = current_usernames

    print(entry.tags.all()[0])
    
    context = {'entry': entry,
               'users': users,
               }

    return render(
        request,
        'mainpage/entry_details.html',
        context)


def filter_user(request, username):
    users = current_usernames
    
    user = get_object_or_404(User.objects.all(), username=username)
    
    entries = user.entries.all().filter(publish=1)
    sorted_param = ''

    if request.GET.get('sorted') == 'by_likes':
        entries = entries.order_by('-likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'

    page_obj = get_page_obj(request, entries)
    context = {'entries': entries,
               'users': users,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def filter_tags():
    entries = entries.filter(tags__name__in=['german', 'cover'])
