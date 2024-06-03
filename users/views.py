from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag

from musiclab.utils import get_all_tags, get_page_obj, get_username_list, sort_by, get_published_entries

# Create your views here.
def user_profile(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    entries = user.entries.filter(publish=1)
    
    entries, sorted_param = sort_by(request, entries)
    
    page_obj = get_page_obj(request, entries)
    users = get_username_list()
    tags = get_all_tags()
    
    context = {'entries': entries,
               'users': users,
               'tags': tags,
               'page_obj': page_obj,
               'sorted_param': sorted_param,
               }
    
    return render(
        request,
        'users/profile.html',
        context)