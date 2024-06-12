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
from entries.models import Entry
from mainpage.utils import get_all_tags, get_page_obj, sort_by
from .utils import get_username_list
from entries.utils import get_published_entries, get_all_entries
from comments.forms import CommentForm
from .forms import ProfileForm
from entries.forms import EntryForm
from comments.utils import process_comment_form
from django.contrib import messages

# Create your views here.


def user_profile(request, username):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)

    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
   # entries = user.entries.filter(publish=1)
    if hasattr(user, 'all_entries'):
        entries = get_published_entries(request, user.all_entries, get_comments=False)
    # print(entries[0].likes_received)
        most_liked = Entry.objects.filter(publish=1).annotate(likes_received=Count('all_likes')).order_by('-likes_received').first()
        most_recent = Entry.objects.filter(publish=1).order_by('-created_on').first()
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
    else:
         context = {'profile': profile,
              
               'users': users,
               'tags': tags,
              
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
    # fields = user._meta.get_fields()
    # for field in fields:
    #     print(field)
   # print(user.all_entries)
    if hasattr(user, 'all_entries'):
        entries = get_all_entries(request, user.all_entries, get_comments=False) #user.all_entries.all()
        most_liked = Entry.objects.annotate(likes_received=Count('all_likes')).order_by('-likes_received').first()
        most_recent = Entry.objects.order_by('-created_on').first()
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
    else:
        context = {'profile': profile,
                }
        
    return render(
        request,
        'users/dashboard.html',
        context)


def dashboard_entry(request, username, slug):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))

    entry = get_object_or_404(get_all_entries(request, request.user.all_entries), slug=slug)
    old_files = entry.old_files
    print('In details:')
    print(old_files.items())
    sorted_files = dict(sorted(old_files.items(), key=lambda item: item[1][1], reverse=True))
    print(sorted_files)
    
    comments = entry.all_comments.select_related('author', 'author__profile')

    # if request.GET.get('edit'):
    #     return HttpResponseRedirect(reverse('edit_entry', args=[username, slug]))

    comment_form = process_comment_form(request, entry)
    
    context = {'entry': entry,
               'old_files': sorted_files,
               'comments': comments,
               'comment_form': comment_form,
               }

    return render(
        request,
        'users/dashboard_entry.html',
        context)


def edit_profile(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    profile = request.user.profile
    #id = profile.pic.public_id
    
    if request.method == 'POST' and profile.user == request.user:
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile, new_file=request.FILES.get('pic'))
        if profile_form.is_valid():
            # if request.FILES.get('pic'):
            #     print(cloudinary.uploader.destroy(id, invalidate=True))
            profile_form.save()
            messages.success(request, "Your profile has been saved.")

        else:
            print('not valid')
            print(profile_form.errors.as_data())
            messages.warning(request, "There was an error saving your profile.")            

        print(request.POST)
        return HttpResponseRedirect(reverse('dashboard', args=[username]))
    
    profile_form = ProfileForm(instance=profile, initial={'bio': profile.bio, 'pic': profile.pic, 'social': profile.social, 'email': profile.email})
    
    context = {'profile': profile,
               'profile_form': profile_form,
               }

    return render(
        request,
        'users/profile_form.html',
        context)


def user_favorites(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    
    likes = request.user.liked.select_related('entry')
    is_favorite = 1

    page_obj = get_page_obj(request, likes)
    
    context = {#'likes': likes,
               'page_obj': page_obj,
                'is_favorite': is_favorite,
               }
    
    return render(request,
                  'users/dashboard_user_likes.html',
                  context)

# TODO: Where to put comments and likes? move utils! make like snippets!

def user_comments(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        return HttpResponseRedirect(reverse('home'))
    
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)
    
    comments = request.user.commenter.select_related('entry')


    page_obj = get_page_obj(request, comments, 10)
    
    context = {#'comments': comments,
               'page_obj': page_obj,
               }
    
    return render(request,
                  'users/dashboard_user_comments.html',
                  context)
    