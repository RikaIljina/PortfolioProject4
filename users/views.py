from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.core.files.storage import FileSystemStorage 
from taggit.models import Tag
import cloudinary
from django.core.exceptions import ValidationError
#import cloudinary.uploader

from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries, save_like
from mainpage.forms import CommentForm
from .forms import EntryForm, ProfileForm

# Create your views here.


def user_profile(request, username):
    if request.GET.get('liked') and request.user.is_authenticated:
        return save_like(request)

    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
   # entries = user.entries.filter(publish=1)
    entries = get_published_entries(request, user.entries)
    most_liked = entries.order_by('-likes').first
    most_recent = entries.order_by('-created_on').first
    entries, sorted_param = sort_by(request, entries)

    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()

    context = {'profile': profile,
               #'entries': entries,
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
               #'entries': entries,
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
    id = profile.pic.public_id
    
    if request.method == 'POST' and profile.user == request.user:
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            if request.FILES.get('pic'):
                print(cloudinary.uploader.destroy(id, invalidate=True))
            profile_form.save()

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
    
    #all_titles = list(request.user.entries.all().values_list('title', flat=True))
    #titles = [title.get('title') for title in all_titles]

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, author=request.user)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = request.user
            # cloudinary.uploader.upload(request.FILES['audio_file'])
            entry.likes = 0
            entry.save()
            entry_form.save_m2m()
            return HttpResponseRedirect(reverse('dashboard', args=[username]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())
            #return reverse('new_entry', args=[entry_form])

        #print(request.POST)

    else:
        entry_form = EntryForm(author=request.user)

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
    #id = entry.audio_file.public_id

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, instance=entry, author=request.user, new_file=request.FILES.get('audio_file'))

        if entry_form.is_valid():
            print('form is valid')
            entry = entry_form.save(commit=False)
            print('in view now')
            #print(f'old: {id}')
            # if request.FILES.get('audio_file'):
            #     print(f'changed file: {request.FILES['audio_file']}, old: {id}')
            #     print(cloudinary.uploader.destroy(id, resource_type = "video", invalidate=True))
            entry.author = request.user
            entry.likes = 0
            entry.save()
            entry_form.save_m2m()
            print('finished saving in view')
            return HttpResponseRedirect(reverse('dashboard', args=[username]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())

    else:
        tag_list = [value['name'] for value in entry.tags.all().values()]
        entry_form = EntryForm(instance=entry, author=request.user, initial={'title': entry.title, 'description': entry.description,
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
    print(entry.audio_file.public_id)
    print(entry.audio_file.url)
    #print(cloudinary.uploader.destroy(entry.audio_file.public_id, resource_type = "video", invalidate=True))
#    storage_instance.delete(name=entry.audio_file.name)
    #entry.audio_file.delete()

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


def user_favorites(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    if request.GET.get('liked') and request.user.is_authenticated:
        return save_like(request)
    
    likes = request.user.liked.select_related('entry')
    is_favorite = 1

    page_obj = get_page_obj(request, likes)
    
    context = {#'likes': likes,
               'page_obj': page_obj,
                'is_favorite': is_favorite,
               }
    
    return render(request,
                  'users/favorites.html',
                  context)
    

def user_comments(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    if request.GET.get('liked') and request.user.is_authenticated:
        return save_like(request)
    
    comments = request.user.commenter.select_related('entry')


    page_obj = get_page_obj(request, comments, 10)
    
    context = {#'comments': comments,
               'page_obj': page_obj,
               }
    
    return render(request,
                  'users/comments.html',
                  context)