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
from mainpage.models import Like
from entries.models import Entry
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries
from mainpage.forms import CommentForm
from .forms import ProfileForm
from entries.forms import EntryForm

# Create your views here.


def user_profile(request, username):
    # if request.GET.get('liked') and request.user.is_authenticated:
    #     return save_like(request)

    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
   # entries = user.entries.filter(publish=1)
    entries = get_published_entries(request, user.all_entries)
    print(entries[0].likes_received)
    most_liked = entries.order_by('-likes_received').first
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
    fields = user._meta.get_fields()
    for field in fields:
        print(field)
    print(user.all_entries)
    if hasattr(user, 'all_entries'):
        print('HI')
        entries = user.all_entries.all()
        most_liked = entries.annotate(likes_received=Count('all_likes')).order_by('-likes_received').first
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
    else:
        context = {'profile': profile,
                }
        
    return render(
        request,
        'users/dashboard.html',
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

        else:
            print('not valid')
            print(profile_form.errors.as_data())

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




def edit_comment(request, current_path, comment_id):
    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)
   # next = request.POST.get('next')
    
    if request.method == 'POST' and comment.author == request.user:
        
        if 'updateOld' in request.POST:
            print(request.POST)
            comment_form = CommentForm(data=request.POST, instance=comment)

            if comment_form.is_valid():
                comment_form.save()
            else:
                print(comment_form.errors.as_data())

    return redirect(f'{reverse('home')}{current_path}')


def delete_comment(request, current_path, comment_id):
    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)
   # next = request.GET.get('old')
   # print('resolving:')
   # print(resolve(current_path))
   # print(resolve(request.path))
   # print(next)
    
    if comment.author == request.user:
        comment.delete()
    print(f'current: {current_path}')
    print('going to last path')
    print(f'{reverse('home')}{current_path}')
    return redirect(f'{reverse('home')}{current_path}')


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
                  'users/favorites.html',
                  context)
    

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
                  'users/comments.html',
                  context)
    
def add_like(request, entry_id, current_path=''):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    entry = get_object_or_404(get_published_entries(request, Entry.objects, False), id=entry_id)
    
    if request.method == 'GET':
        print('...getting...')
        params = f'?{request.GET.urlencode()}'
    else:
        params = ''
    #print(request.user.liked.filter(entry=entry).exists())
    #print(entry.already_liked)
    
    #if entry.already_liked == 0:
    if not request.user.liked.filter(entry=entry).exists():
        like = Like.objects.create(user=request.user, entry=entry)
    else:
        like = request.user.liked.get(entry=entry)
        like.delete()

    print('going to last path')
    print(f'{reverse('home')}{current_path}')
    return redirect(f'{reverse('home')}{current_path}{params}')

