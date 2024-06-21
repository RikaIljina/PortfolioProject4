from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from taggit.models import Tag
from django.conf import settings as django_settings
import os

from entries.models import Entry
from likes.models import Like

# Helper functions


def get_username_list():
    all_users = User.objects.select_related('profile')
# order list after db query!
    # current_usernames = list(User.objects.values_list(
    #             'username', flat=True).order_by(Lower('username')))
    current_users = dict({value.username: value.profile.pic.url for value in all_users})
    print(current_users)
    users = dict(sorted(current_users.items()))
     
    # with open(os.path.join(django_settings.STATIC_ROOT, 'usernames.txt'), 'w') as file:
    #     file.writelines(line + '\n' for line in current_usernames)
    
    return users

def get_users_from_file():
    with open('staticfiles/usernames.txt') as f:
            users = f.read().splitlines()

    return users