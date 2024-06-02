from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all().filter(publish=1)

    if request.GET.get('sorted') == 'by_likes':
        entries = Entry.objects.all().filter(publish=1).order_by('-likes')
    elif request.GET.get('sorted') == 'by_date':
        entries = Entry.objects.all().filter(publish=1).order_by('-created_on')
    
    
    return render(
        request,
        'mainpage/index.html',
        {'entries': entries})

