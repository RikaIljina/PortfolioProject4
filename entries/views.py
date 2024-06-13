from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.core.files.storage import FileSystemStorage 
from taggit.models import Tag
import cloudinary
from django.core.exceptions import ValidationError
#import cloudinary.uploader
from likes.models import Like
from mainpage.utils import get_all_tags, get_page_obj, sort_by, get_tags_from_file
from users.utils import get_username_list, get_users_from_file
from .utils import get_published_entries
from comments.forms import CommentForm
from .forms import EntryForm
from .models import Entry
from users.forms import ProfileForm
from comments.utils import process_comment_form


def entry_details(request, slug):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    
    entry = get_object_or_404(get_published_entries(request, Entry.objects), slug=slug)
    old_files = entry.old_files
    print('In details:')
    print(old_files.items())
    sorted_files = dict(sorted(old_files.items(), key=lambda item: item[1][1], reverse=True))
    print(sorted_files)
    
    comments = entry.all_comments.select_related('author', 'author__profile')
  #  print(comments)
   # entry_tags = entry.tags.prefetch_related('tagged_items__tag')
   # print(entry_tags)
    
    #users = get_username_list()
    users = get_users_from_file()
    #tags = get_all_tags()
    tags = get_tags_from_file()
    
    if request.method == 'POST':
        process_comment_form(request, entry)
        # TODO: make sure to go back the same path, via js
        return redirect(f'{reverse('entry_details', args=[slug])}')

    comment_form = CommentForm()

    context = {'entry': entry,
               'old_files': sorted_files,
               'comments': comments,
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
            messages.success(request, "Your entry has been saved.")
           # return HttpResponseRedirect(reverse('dashboard_entry', args=[username, new_slug]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())
            messages.warning(request, "Your entry could not be saved.")
            raise ValidationError("Your title is empty.")
            
            #return reverse('new_entry', args=[entry_form])
        return HttpResponseRedirect(reverse('dashboard_entry', args=[username, new_slug]))
        

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
    old_files = dict(sorted(entry.old_files.items(), key=lambda item: item[1][1], reverse=True))
    # print('In details:')
    # print(old_files.items())
    # sorted_files = dict(sorted(entry.old_files.items(), key=lambda item: item[1][1], reverse=True))
    # print(sorted_files)

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
            messages.success(request, "Your entry has been saved.")
            
            print('finished saving in view')
            return HttpResponseRedirect(reverse('dashboard_entry', args=[username, new_slug]))
            
        else:
            print('not valid')
            print(entry_form.errors.as_data())
            messages.warning(request, "Your entry could not be saved.")
            

    else:
        tag_list = [value['name'] for value in entry.tags.all().values()]
        entry_form = EntryForm(instance=entry, user=request.user, initial={'title': entry.title, 'description': entry.description,
                           'audio_file': entry.audio_file, 'keep_file': True, 'tags':(',').join(tag_list), 'publish': entry.publish})

    context = {
        'entry': entry,
        'entry_form': entry_form,
        'old_files': old_files,
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
    messages.success(request, "Your entry has been deleted.")
    
    
    return HttpResponseRedirect(reverse('dashboard', args=[username]))


def delete_old_file(request, username, slug, file_id):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)
    if entry.old_files.get(file_id):
        del entry.old_files[file_id]
        entry.save()
        print(f'{username}, {slug}, {file_id}')
        print(cloudinary.uploader.destroy(file_id, resource_type = "video", invalidate=True))
        messages.success(request, "Your file has been deleted.")
    
    return redirect('edit_entry', username=username, slug=slug)
