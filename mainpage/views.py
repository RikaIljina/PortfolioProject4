from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from mainpage.utils import get_page_context
from entries.utils import get_published_entries
from entries.models import Entry

from .forms import MessageToAdminForm


def index(request):
    entries = get_published_entries(request, Entry.objects, get_comments=False)

    entries, sorted_param, page_obj, users, tags = get_page_context(
        request, entries
    )

    # Tells the sidebar to enable sorting buttons for the user entries
    enable_sorting = True

    context = {
        "entries": entries,
        "sorted_param": sorted_param,
        "page_obj": page_obj,
        "users": users,
        "tags": tags,
        "enable_sorting": enable_sorting,
    }
    print(request)

    return render(request, "mainpage/index.html", context)


def filter_user(request, username):
    user = get_object_or_404(User.objects.all(), username=username)
    entries = get_published_entries(
        request, user.all_entries, get_comments=False
    )

    entries, sorted_param, page_obj, users, tags = get_page_context(
        request, entries
    )

    # Tells the sidebar to keep clicked-on filter section open
    filter_user = True
    # Tells the sidebar to enable sorting buttons for the user entries
    enable_sorting = True

    context = {
        "entries": entries,
        "users": users,
        "user_filter": username,
        "tags": tags,
        "page_obj": page_obj,
        "sorted_param": sorted_param,
        "filter_user": filter_user,
        "enable_sorting": enable_sorting,
    }

    return render(request, "mainpage/index.html", context)


def filter_tag(request, tag):
    entries = get_published_entries(
        request, Entry.objects, get_comments=False
    ).filter(tags__name__in=[tag])

    entries, sorted_param, page_obj, users, tags = get_page_context(
        request, entries
    )

    # entries, sorted_param = sort_by(request, entries)

    # page_obj = get_page_obj(request, entries)
    # #users = get_username_list()
    # users = get_users_from_file()
    # # tags = get_all_tags()
    # tags = get_tags_from_file()
    filter_tag = True
    enable_sorting = True

    context = {
        "entries": entries,
        "tag_filter": tag,
        "users": users,
        "tags": tags,
        "page_obj": page_obj,
        "sorted_param": sorted_param,
        "filter_tag": filter_tag,
        "enable_sorting": enable_sorting,
    }

    return render(request, "mainpage/index.html", context)


def about(request):
    users, tags = get_page_context(request, None)

    if request.method == "POST":
        message_form = MessageToAdminForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, "Your message has been submitted.")
        else:
            print(message_form.errors.as_data())
            messages.error(request, "Your message has not been submitted.")

    message_form = MessageToAdminForm()

    context = {
        "users": users,
        "tags": tags,
        "message_form": message_form,
    }

    return render(request, "mainpage/about.html", context)
