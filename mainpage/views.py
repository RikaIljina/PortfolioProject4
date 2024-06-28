from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from taggit.models import Tag
import os

from .models import MessageToAdmin
from .forms import MessageToAdminForm
from likes.models import Like
from entries.models import Entry

from comments.forms import CommentForm
from mainpage.utils import get_all_tags, get_page_obj, sort_by, get_tags_from_file, get_mainpage_context
from users.utils import get_username_list, get_users_from_file
from entries.utils import get_published_entries

# util


# Views

def index(request):
    entries = get_published_entries(request, Entry.objects, get_comments=False)

    entries, sorted_param, page_obj, users, tags = get_mainpage_context(
        request, entries)
   # print(tags)
    # entries, sorted_param = sort_by(request, entries)

    # page_obj = get_page_obj(request, entries)

    # # tags = get_all_tags()
    # #users = get_username_list()
    # users = get_users_from_file()
    # #tags = get_all_tags()
    # tags = get_tags_from_file()
    enable_sorting = True

    context = {'entries': entries,
               'sorted_param': sorted_param,
               'page_obj': page_obj,
               'users': users,
               'tags': tags,
               'enable_sorting': enable_sorting,
               }
    print(request)

    return render(
        request,
        'mainpage/index.html',
        context)


def filter_user(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    entries = get_published_entries(
        request, user.all_entries, get_comments=False)

    entries, sorted_param, page_obj, users, tags = get_mainpage_context(
        request, entries)

    # entries, sorted_param = sort_by(request, entries)

    # # if request.GET.get('liked') and request.user.is_authenticated:
    # #     return save_like(request, entries)

    # page_obj = get_page_obj(request, entries)
    # #users = get_username_list()
    # users = get_users_from_file()
    # tags = get_tags_from_file()
    filter_user = True
    enable_sorting = True

    context = {'entries': entries,
               'users': users,
               'user_filter': username,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               'filter_user': filter_user,
               'enable_sorting': enable_sorting,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def filter_tag(request, tag):
    entries = get_published_entries(
        request, Entry.objects, get_comments=False).filter(tags__name__in=[tag])

    entries, sorted_param, page_obj, users, tags = get_mainpage_context(
        request, entries)

    # entries, sorted_param = sort_by(request, entries)

    # page_obj = get_page_obj(request, entries)
    # #users = get_username_list()
    # users = get_users_from_file()
    # # tags = get_all_tags()
    # tags = get_tags_from_file()
    filter_tag = True
    enable_sorting = True

    context = {'entries': entries,
               'tag_filter': tag,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               'filter_tag': filter_tag,
               'enable_sorting': enable_sorting,
               }

    return render(
        request,
        'mainpage/index.html',
        context)


def about(request):
    users, tags = get_mainpage_context(request, None)

    if request.method == 'POST':
        message_form = MessageToAdminForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, 'Your message has been submitted.')
        else:
            print(message_form.errors.as_data())
            messages.error(request, 'Your message has not been submitted.')            

    message_form = MessageToAdminForm()


    context = {'users': users,
               'tags': tags,
               'message_form': message_form,
               }

    return render(
        request,
        'mainpage/about.html',
        context)
