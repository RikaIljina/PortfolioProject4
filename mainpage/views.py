"""
views.py for the 'Mainpage' app.

This module contains view functions that render the index page and the about
page and handle the general views that are accessible to all website visitors.

Key functionalities:
- Show all entries on the main page
- Show entries filtered by a specific user
- Show entries filtered by a specific tag
- Show the 'about' page

View Functions:
- index(request): Retrieves and renders all entries and all relevant context
    parameters.
- filter_user(request, username): Retrieves and renders all entries of a
    specified user as well as all relevant context parameters.
- filter_tag(request, tag): Retrieves and renders all entries of a specified
    tag as well as all relevant context parameters.
- about(request): Renders the 'about' page with all relevant context parameters
    and shows a feedback form to authenticated users.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from mainpage.utils import get_page_context
from entries.utils import get_published_entries
from entries.models import Entry

from .forms import MessageToAdminForm


def index(request):
    """
    Render the index page with a list of published entries

    This view retrieves and processes a list of published entries to be
    displayed on the main page. It also retrieves parameters for the sidebar
    filter and sort functionalities.
    GET requests are processed by the sort_by() function inside the
    get_page_context() function.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered index page with the context containing entries
        and additional information for pagination, sorting, and filtering.
    """

    entries = get_published_entries(request, Entry.objects, get_comments=False)

    # get_page_context() takes care of checking whether entries is empty
    users, tags, entries, sorted_param, page_obj = get_page_context(
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

    return render(request, "mainpage/index.html", context)


def filter_user(request, username):
    """
    Render the index page with a list of a user's published entries

    This view retrieves and processes a list of one user's published entries to
    be displayed on the main page. It also retrieves parameters for the sidebar
    filter and sort functionalities.
    GET requests are processed by the sort_by() function inside the
    get_page_context() function.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The name of a user.

    Returns:
        HttpResponse: Rendered index page with the context containing entries
        and additional information for pagination, sorting, and filtering.

    Raises:
        Http404: If no user with that username exists.
    """

    user = get_object_or_404(User.objects.all(), username=username)
    entries = get_published_entries(
        request, user.all_entries, get_comments=False
    )
    # get_page_context() takes care of checking whether entries is empty
    users, tags, entries, sorted_param, page_obj = get_page_context(
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
    """
    Render the index page with a list of entries with the specified tag

    This view retrieves and processes all entries with a specific tag to
    be displayed on the main page. It also retrieves parameters for the sidebar
    filter and sort functionalities.
    GET requests are processed by the sort_by() function inside the
    get_page_context() function.

    Args:
        request (HttpRequest): The HTTP request object.
        tag (str): The name of a tag.

    Returns:
        HttpResponse: Rendered index page with the context containing entries
        and additional information for pagination, sorting, and filtering.
    """

    entries = get_published_entries(
        request, Entry.objects, get_comments=False
    ).filter(tags__name__in=[tag])

    # get_page_context() takes care of checking whether entries is empty
    users, tags, entries, sorted_param, page_obj = get_page_context(
        request, entries
    )

    # Tells the sidebar to keep clicked-on filter section open
    filter_tag = True
    # Tells the sidebar to enable sorting buttons for the user entries
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
    """
    Render the about page with a message form

    This view shows the content of the about page as well as a message
    submission form for authenticated users. It also retrieves parameters for
    the sidebar filter functionality.
    The view handles POST requests whenever a new message is submitted.

    Args:
        request (HttpRequest): The HTTP request object.
        tag (str): The name of a tag.

    Returns:
        HttpResponse: Rendered index page with the context containing entries
        and additional information for pagination, sorting, and filtering.
    """

    users, tags, *args = get_page_context(request, None)

    if request.method == "POST":
        message_form = MessageToAdminForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, "Your message has been submitted.")
        else:
            messages.error(request, "Your message has not been submitted.")

    message_form = MessageToAdminForm()

    context = {
        "users": users,
        "tags": tags,
        "message_form": message_form,
    }

    return render(request, "mainpage/about.html", context)
