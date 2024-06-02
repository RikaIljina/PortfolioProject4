from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Entry

# Create your views here.


def index(request):
    entries = Entry.objects.all().filter(publish=1)
    sorted_param = ''

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
         'page_obj': page_obj})

