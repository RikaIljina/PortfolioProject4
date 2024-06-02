from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all().filter(publish=1)
    
    if request.method == "POST":
        print("Posted")
        if 'by_likes' in request.POST:
            entries = Entry.objects.all().filter(publish=1).order_by('-likes')
        elif 'by_date' in request.POST:
            entries = Entry.objects.all().filter(publish=1).order_by('-created_on')
    
    return render(
        request,
        'mainpage/index.html',
        {'entries': entries})




# For sort button: if 'sort_likes' in request.POST