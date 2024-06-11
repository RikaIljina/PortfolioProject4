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
from mainpage.utils import get_all_tags, get_page_obj, sort_by
from users.utils import get_username_list
from entries.utils import get_published_entries
from comments.forms import CommentForm
from users.forms import ProfileForm
from entries.forms import EntryForm
# Create your views here.

def add_like(request, entry_id, current_path=''):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    #entry = get_object_or_404(get_published_entries(request, Entry.objects, get_likes=True, get_comments=False), id=entry_id)
    entry = get_object_or_404(Entry.objects.filter(publish=1).annotate(already_liked=Count('all_likes', filter=Q(
                                    all_likes__user=request.user), distinct=True)), id=entry_id)
    
    
    if request.GET.dict():
        print('...getting...')
        params = f'?{request.GET.urlencode()}'
    else:
        params = ''
    #print(entry.already_liked)
    
    #if entry.already_liked == 0:
   # if not request.user.liked.filter(entry=entry).exists():
    if not entry.already_liked:
        like = Like.objects.create(user=request.user, entry=entry)
    else:
        like = request.user.liked.get(entry=entry)
        like.delete()

    print('going to last path')
    print(f'{reverse('home')}{current_path}')
    return redirect(f'{reverse('home')}{current_path}{params}')

