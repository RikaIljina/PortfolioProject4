from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag
from django.conf import settings as django_settings
import os
import json

from entries.models import Entry
from likes.models import Like
from users.utils import get_username_list

# Helper functions


def get_mainpage_context(request, entries):
    entries, sorted_param = sort_by(request, entries)
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    # users = get_users_from_file()
    tags = get_tags_from_file()
    
    return entries, sorted_param, page_obj, users, tags
    
    

def get_page_obj(request, entries, amount=3):
    paginator = Paginator(entries, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_all_tags():
    # tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
    #     entry__publish=1), distinct=True)).filter(amount__gt=0).order_by('name')
    #print(tags)
    #print(tags.values())
    # BUG: Tag doesn't register tagged entry immediately after tag creation or 
    # the entry is not counted for other reasons, thus tag isn't counted
    tags = Tag.objects.annotate(amount=Count('entry', filter=Q(
        entry__publish=1), distinct=True)).filter(amount__gt=0)

    tag_list = {str(value['name']): str(value['amount']) for value in tags.values()}
    tag_dict = json.dumps(tag_list)
    #print(tags) # tags.values_list('name', flat=True): })
    with open(os.path.join(django_settings.STATIC_ROOT, 'tags.txt'), 'w') as file:
        #file.writelines(str(line) + '\n' for line in tag_list)
        file.write(tag_dict)
        
   # tags.filter(amount=0).delete()
    
    return tags

def delete_tags():
    Tag.objects.filter(entry=None).delete()

def get_tags_from_file():
    with open('staticfiles/tags.txt') as f:
        data = f.read()
    #print(data)
    tags = json.loads(data)
    #print(tags)
    return tags


def sort_by(request, entries):
    if request.GET.get('sorted') == 'by_likes':
        entries = entries.annotate(count_likes=Count('all_likes',  distinct=True)).order_by('-count_likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'
    elif request.GET.get('sorted') == 'by_published':
        entries = entries.order_by('publish')
        sorted_param = '?sorted=by_published'
    elif request.GET.get('sorted') == 'by_updated':
        entries = entries.order_by('-updated_on')
        sorted_param = '?sorted=by_updated'
    
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