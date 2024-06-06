from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries, save_like
from mainpage.forms import CommentForm

# Create your views here.


def user_profile(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
   # entries = user.entries.filter(publish=1)
    entries = get_published_entries(request, user.entries)
    most_liked = entries.order_by('-likes').first
    most_recent = entries.order_by('-created_on').first
    entries, sorted_param = sort_by(request, entries)

    if request.GET.get('liked') and request.user.is_authenticated:
        return save_like(request)

    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()

    context = {'profile': profile,
               'entries': entries,
               'most_liked': most_liked,
               'most_recent': most_recent,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'users/profile.html',
        context)


def dashboard(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    user = request.user
    profile = user.profile
    entries = user.entries.all()
    most_liked = entries.order_by('-likes').first
    most_recent = entries.order_by('-created_on').first
    entries, sorted_param = sort_by(request, entries)

    if request.GET.get('liked') and request.user.is_authenticated:
        return save_like(request)
# Deactivate sidebar!! 
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()

    context = {'profile': profile,
               'entries': entries,
               'most_liked': most_liked,
               'most_recent': most_recent,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'users/dashboard.html',
        context)
    

def dashboard_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
        
    entry = get_object_or_404(request.user.entries.all(), slug=slug)

    if request.GET.get('edit'):
        return HttpResponseRedirect(reverse('edit_entry', args=[username, slug]))

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
               'comment_form': comment_form,
               }

    return render(
        request,
        'users/dashboard_entry.html',
        context)
    
    
def edit_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.entries.all(), slug=slug)
    
    
    context = {'entry': entry,
               }
    
    return render(
        request,
        'users/edit_entry.html',
        context)