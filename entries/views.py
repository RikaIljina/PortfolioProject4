from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import resolve
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
from likes.models import Like
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries
from comments.forms import CommentForm
from .forms import EntryForm
from .models import Entry
from users.forms import ProfileForm


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
        'entries/entry_details.html',
        context)


def new_entry(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    #all_titles = list(request.user.entries.all().values_list('title', flat=True))
    #titles = [title.get('title') for title in all_titles]

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, user=request.user)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            new_slug = Entry.objects.get(id=entry.id).slug
            
           # entry.author = request.user
            # cloudinary.uploader.upload(request.FILES['audio_file'])
            #entry.likes = 0
            entry.save()
            entry_form.save_m2m()
            return HttpResponseRedirect(reverse('dashboard_entry', args=[username, new_slug]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())
            #return reverse('new_entry', args=[entry_form])

        #print(request.POST)

    else:
        entry_form = EntryForm(user=request.user)

    context = {
        'entry_form': entry_form,
    }

    return render(
        request,
        'entries/entry_form.html',
        context)


def edit_entry(request, username, slug):

    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)
    #id = entry.audio_file.public_id

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, instance=entry, user=request.user, new_file=request.FILES.get('audio_file'))

        if entry_form.is_valid():
            print('form is valid')
            entry = entry_form.save(commit=False)
            print('in view now')
            new_slug = Entry.objects.get(id=entry.id).slug
            #print(f'old: {id}')
            # if request.FILES.get('audio_file'):
            #     print(f'changed file: {request.FILES['audio_file']}, old: {id}')
            #     print(cloudinary.uploader.destroy(id, resource_type = "video", invalidate=True))
            entry.author = request.user
            #entry.likes = 0
            entry.save()
            entry_form.save_m2m()
            print('finished saving in view')
            return HttpResponseRedirect(reverse('dashboard_entry', args=[username, new_slug]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())

    else:
        tag_list = [value['name'] for value in entry.tags.all().values()]
        entry_form = EntryForm(instance=entry, user=request.user, initial={'title': entry.title, 'description': entry.description,
                           'audio_file': entry.audio_file, 'tags':(',').join(tag_list), 'publish': entry.publish})

    context = {
        'entry': entry,
        'entry_form': entry_form,
    }

    return render(
        request,
        'entries/entry_form.html',
        context)


def delete_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)
    print(entry.audio_file.public_id)
    print(entry.audio_file.url)
    #print(cloudinary.uploader.destroy(entry.audio_file.public_id, resource_type = "video", invalidate=True))
#    storage_instance.delete(name=entry.audio_file.name)
    #entry.audio_file.delete()

    entry.delete()
    
    return HttpResponseRedirect(reverse('dashboard', args=[username]))