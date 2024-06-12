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


def get_published_entries(request, source, get_likes=True, get_comments=True):
    if request.user.is_authenticated and get_likes:
        entries = source.filter(publish=1).annotate(
            already_liked=Count('all_likes', filter=Q(
                                all_likes__user=request.user), distinct=True),
            likes_received=Count('all_likes', distinct=True), 
            comments_received=Count('all_comments', distinct=True)) \
            .select_related('author').select_related('author__profile') \
            .prefetch_related('tagged_items__tag', 'tags', 'all_comments')
        print(f"Annotating: {request.user.liked}")
    elif get_comments:
        entries = source.filter(publish=1).annotate(
            likes_received=Count('all_likes', distinct=True), 
            comments_received=Count('all_comments', distinct=True)) \
            .select_related('author').select_related('author__profile') \
            .prefetch_related('tagged_items__tag', 'tags', 'all_comments')
            # .select_related('all_comments__comment') 
            #, 'all_comments__author__profile')
    else:
        entries = source.filter(publish=1).annotate(
            likes_received=Count('all_likes', distinct=True), 
            comments_received=Count('all_comments', distinct=True)) \
            .select_related('author').select_related('author__profile') \
            .prefetch_related('tagged_items__tag', 'tags')
            # .select_related('all_comments__comment') 
            #, 'all_comments__author__profile')

    return entries

def get_all_entries(request, source, get_comments=True):
    if request.user.is_authenticated and get_comments:
        entries = source.annotate(
            likes_received=Count('all_likes', distinct=True),
            comments_received=Count('all_comments', distinct=True)) \
            .select_related('author').select_related('author__profile') \
            .prefetch_related('tagged_items__tag', 'tags', 'all_comments')
        return entries
            
    elif request.user.is_authenticated:
        entries = source.annotate(
            likes_received=Count('all_likes', distinct=True),
            comments_received=Count('all_comments', distinct=True)) \
            .select_related('author').select_related('author__profile') \
            .prefetch_related('tagged_items__tag', 'tags',)
        return entries
        
        
