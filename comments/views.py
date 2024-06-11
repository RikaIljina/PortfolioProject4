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
from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries
from .forms import CommentForm
from users.forms import ProfileForm
from entries.forms import EntryForm
# Create your views here.


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