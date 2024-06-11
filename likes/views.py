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
from .models import Like
from entries.models import Entry
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries
from comments.forms import CommentForm
from users.forms import ProfileForm
from entries.forms import EntryForm
# Create your views here.

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

