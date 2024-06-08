from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag
import cloudinary

from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries, save_like
from mainpage.forms import CommentForm
from .forms import EntryForm, ProfileForm

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


def dashboard_new_user(request):
        return HttpResponseRedirect(reverse('edit_profile', args=[request.user.username]))
    

def dashboard(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    user = request.user
    profile = user.profile
    entries = user.entries.all()
    most_liked = entries.order_by('-likes').first
    most_recent = entries.order_by('-created_on').first
    entries, sorted_param = sort_by(request, entries)

    # if request.GET.get('newEntry'):
    #     return HttpResponseRedirect(reverse('new_entry'))

    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
# Deactivate sidebar!!
    page_obj = get_page_obj(request, entries)
    # users = get_username_list()
    # tags = get_all_tags()

    context = {'profile': profile,
               'entries': entries,
               'most_liked': most_liked,
               'most_recent': most_recent,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }

    return render(
        request,
        'users/dashboard.html',
        context)
    

def edit_profile(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    profile = request.user.profile
    
    if request.method == 'POST' and profile.user == request.user:
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            #profile = profile_form.save(commit=False)
            #profile.user = request.user
            profile_form.save()
           # profile_form.save_m2m()
        else:
            print('not valid')
            print(profile_form.errors.as_data())

        print(request.POST)
        return HttpResponseRedirect(reverse('dashboard', args=[username]))
    
    profile_form = ProfileForm(initial={'bio': profile.bio, 'pic': profile.pic, 'social': profile.social, 'email': profile.email})
    
    context = {'profile': profile,
               'profile_form': profile_form,
               }

    return render(
        request,
        'users/profile_form.html',
        context)


def dashboard_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.entries.all(), slug=slug)

    # if request.GET.get('edit'):
    #     return HttpResponseRedirect(reverse('edit_entry', args=[username, slug]))

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


def new_entry(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = request.user
            # cloudinary.uploader.upload(request.FILES['audio_file'])
            entry.likes = 0
            entry.save()
            entry_form.save_m2m()
        else:
            print('not valid')
            print(entry_form.errors.as_data())

        print(request.POST)
        return HttpResponseRedirect(reverse('dashboard', args=[username]))

    entry_form = EntryForm()

    context = {
        'entry_form': entry_form,
    }

    return render(
        request,
        'users/entry_form.html',
        context)


def edit_entry(request, username, slug):

    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.entries.all(), slug=slug)

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, instance=entry)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = request.user
            # cloudinary.uploader.upload(request.FILES['audio_file'])
            entry.likes = 0
            entry.save()
            entry_form.save_m2m()
        else:
            print('not valid')
            print(entry_form.errors.as_data())

        print(request.POST)
        return HttpResponseRedirect(reverse('dashboard', args=[username]))
    
    tag_list = [value['name'] for value in entry.tags.all().values()]

    entry_form = EntryForm(initial={'title': entry.title, 'description': entry.description,
                           'audio_file': entry.audio_file, 'tags':(',').join(tag_list), 'publish': entry.publish})

    context = {
        'entry': entry,
        'entry_form': entry_form,
    }

    return render(
        request,
        'users/entry_form.html',
        context)


def delete_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.entries.all(), slug=slug)
    entry.delete()
    
    return HttpResponseRedirect(reverse('dashboard', args=[username]))


def edit_comment(request, current_path, comment_id):
    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)
    next = request.POST.get('next')
    
    if request.method == 'POST' and comment.author == request.user:
        
        if 'updateOld' in request.POST:
            print(request.POST)
            comment_form = CommentForm(data=request.POST, instance=comment)

            if comment_form.is_valid():
                comment_form.save()
            else:
                print(comment_form.errors.as_data())

    return HttpResponseRedirect(next)


def delete_comment(request, current_path, comment_id):
    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)
    next = request.GET.get('old')
    print(next)
    
    if comment.author == request.user:
        comment.delete()

    return HttpResponseRedirect(next)