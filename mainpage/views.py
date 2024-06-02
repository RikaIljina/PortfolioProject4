from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all().order_by('-likes')
    return render(
        request,
        'mainpage/index.html',
        {'entries': entries})




# For sort button: if 'sort_likes' in request.POST