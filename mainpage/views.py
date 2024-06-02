from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all().filter(publish=1)
    sorted_param = ''
    User = get_user_model()
    users = User.objects.all()

    if request.GET.get('sorted') == 'by_likes':
        entries = Entry.objects.all().filter(publish=1).order_by('-likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = Entry.objects.all().filter(publish=1).order_by('-created_on')
        sorted_param = '?sorted=by_date'

    paginator = Paginator(entries, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'mainpage/index.html',
        {'entries': entries,
         'sorted_param': sorted_param,
         'page_obj': page_obj,
         'users': users,
         })


def entry_details(request, slug):
    entry = get_object_or_404(Entry.objects.filter(publish=1), slug=slug)
    User = get_user_model()
    users = User.objects.all()
    
    return render(
        request,
        'mainpage/entry_details.html',
        {'entry': entry,
         'users': users,
         })


def filter_user(request, username):
    User = get_user_model()
    users = User.objects.all()
    user = get_object_or_404(users, username=username)
    entries = user.entries.all().filter(publish=1)
    sorted_param = ''
    
    if request.GET.get('sorted') == 'by_likes':
        entries = entries.order_by('-likes')
        sorted_param = '?sorted=by_likes'
    elif request.GET.get('sorted') == 'by_date':
        entries = entries.order_by('-created_on')
        sorted_param = '?sorted=by_date'

    paginator = Paginator(entries, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'mainpage/index.html',
        {'entries': entries,
         'users': users,
         'page_obj': page_obj,
         'sorted_param': sorted_param,
         })