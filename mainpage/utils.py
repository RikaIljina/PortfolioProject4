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

def get_page_obj(request, entries, amount=3):
    paginator = Paginator(entries, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


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
    elif request.GET.get('sorted') == 'by_published':
        entries = entries.order_by('publish')
        sorted_param = '?sorted=by_published'
    
    else:
        sorted_param = ''
        
    print(request.GET)
    
    return entries, sorted_param




# def save_like(request, source=Entry.objects):
#     entry_id = request.GET.get('liked')
#     entry = get_object_or_404(get_published_entries(request, source), id=entry_id)
#     print(entry.already_liked)
#     print(entry_id)
#     if entry.already_liked == 0:
#         like = Like.objects.create(user=request.user, entry=entry)
#     else:
#         like = request.user.liked.get(entry=entry)
#         like.delete()

#     if request.GET.dict():
#         print(request.GET.dict())
#         q = '?'
#         for key, value in request.GET.items():
#             if key != 'liked':
#                 q += f'{key}=' + f'{value}&'
#         q = q[:-1]

#     else:
#         q = ''
        
#     return HttpResponseRedirect(request.path + q)