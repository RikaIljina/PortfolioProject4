from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from mainpage.models import Entry, Like

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
        entries = entries.annotate(count_likes=Count('all_likes')).order_by('-count_likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'
    else:
        sorted_param = ''
        
    print(request.GET)
    
    return entries, sorted_param

def get_published_entries(request, source, get_likes=True):
    if request.user.is_authenticated and get_likes:
        entries = source.filter(publish=1).annotate(already_liked=Count(
            'all_likes', filter=Q(all_likes__user = request.user)))
        print(f"Annotating: {request.user.liked}")
    else:
        entries = source.filter(publish=1)

    return entries

def save_like(request):
    entry_id = request.GET.get('liked')
    entry = get_object_or_404(get_published_entries(request, Entry.objects), id=entry_id)
    if entry.already_liked == 0:
        like = Like.objects.create(user=request.user, entry=entry)

    if request.GET.dict():
        print(request.GET.dict())
        q = '?'
        for key, value in request.GET.items():
            if key != 'liked':
                q += f'{key}=' + f'{value}&'
        q = q[:-1]

    else:
        q = ''
        
    return HttpResponseRedirect(request.path + q)