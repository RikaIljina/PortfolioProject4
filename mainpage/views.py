from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all()
    return render(
        request,
        'mainpage/index.html',
        {'entries': entries})
