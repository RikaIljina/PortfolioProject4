"""
views.py for the 'Users' app.

This module contains view functions that render the user profile page and the
dashboard of authenticated users.

Key functionalities:
- Show the user profile and all the user's public entries
- Show the user's personal dashboard and all their entries
- Allow to edit the user profile
- Show all likes made by the user
- Show all comments written by the user

View Functions:
- user_profile(request, username): Retrieves and renders the user profile, the
    user's public entries and all relevant context parameters.
- dashboard_new_user(request): Redirects the user to their 'Edit profile' page
    after their registration.
- dashboard(request, username): Retrieves and renders all the user's profile,
    entries, and all relevant context parameters.
- dashboard_entry(request, username, slug): Renders the selected entry with all
    relevant context parameters and edit/delete buttons.
- edit_profile(request, username): Shows the user profile form for editing.
- user_favorites(request, username): Renders all entries the user has liked.
- user_comments(request, username): Renders all comments the user has posted.
"""

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from mainpage.utils import get_page_obj, sort_by, get_page_context
from entries.utils import get_published_entries, get_all_entries
from comments.forms import CommentForm
from comments.utils import process_comment_form

from .forms import ProfileForm


def user_profile(request, username):
    """
    View function to display a user's profile page

    This function retrieves the profile and entries of a specified user and
    renders the profile page with the relevant context. If the user has no
    entries, the context is prepared accordingly.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile is to be
            displayed.

    Returns:
        HttpResponse: The HTTP response object containing the rendered profile
            page.

    Raises:
        Http404: If the user with the specified username does not exist.
    """
    
    user = get_object_or_404(User.objects.all(), username=username)
    profile = user.profile
    # Tells the sidebar to enable sorting buttons for the user entries
    enable_sorting = True
    # Makes sure the 'reset filter' button redirects to profile page when
    # deleting sorting
    profile_view = True

    entries = get_published_entries(
            request, user.all_entries, get_comments=False
        )
    # Only get entries if the user has added at least one entry
    if entries.count() != 0:
        entries, sorted_param, page_obj, users, tags = get_page_context(
                                                            request, entries)

        context = {
            "profile": profile,
            "users": users,
            "tags": tags,
            "page_obj": page_obj,
            "sorted_param": sorted_param,
            "enable_sorting": enable_sorting,
            "profile_view": profile_view,
        }
    else:
        users, tags = get_page_context(request, None)
        context = {
            "profile": profile,
            "users": users,
            "tags": tags,
            "profile_view": profile_view,
        }

    return render(request, "users/profile.html", context)


def dashboard_new_user(request):
    """
    Redirects a user to edit profile after registration

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered profile
            editing page.
    """

    return HttpResponseRedirect(
        reverse("edit_profile", args=[request.user.username])
    )


def dashboard(request, username):
    """
    View function to display an authenticated user's dashboard

    This function retrieves the profile and entries of the authenticated user
    and renders the dashboard and the sidebar with the relevant context.
    If the user has no entries, the context is prepared accordingly.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile is to be
            displayed.

    Returns:
        HttpResponse: The HTTP response object containing the rendered
            dashboard page.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    user = request.user
    profile = user.profile
    # Tells the sidebar to show dashboard buttons
    dashboard_view = True
    # Tells the sidebar to enable sorting buttons for the user entries
    enable_sorting = True

    entries = get_all_entries(
            request, user.all_entries, get_comments=False
        )

    if entries.count() != 0:
        entries, sorted_param = sort_by(request, entries)
        page_obj = get_page_obj(request, entries)
        context = {
            "profile": profile,
            "page_obj": page_obj,
            "sorted_param": sorted_param,
            "dashboard_view": dashboard_view,
            "enable_sorting": enable_sorting,
        }
    else:
        context = {
            "profile": profile,
            "dashboard_view": dashboard_view,
            "enable_sorting": enable_sorting,
        }

    return render(request, "users/dashboard.html", context)


def dashboard_entry(request, username, slug):
    """
    Display a detailed view of an authenticated user's entry on their dashboard

    This view retrieves an entry of the authenticated user by its slug and
    renders the dashboard and the sidebar with the relevant context.
    It gives access to all uploaded audio files and the comment
    section.
    The view also shows buttons that enable editing/deleting the entry
    and handles POST requests whenever a new comment is submitted.

    Args:
        request (HttpObject): The HTTP request object.
        username (str): The username of the user whose entry is being
            displayed.
        slug (string): Slug of the entry to be shown in detailed view.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        Http404: If the user has no entry with the specified slug.

    Returns:
        HttpResponse: The HTTP response object containing the rendered entry
            detail page.
    """
    
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    # Tells the sidebar to show dashboard buttons
    dashboard_view = True

    entry = get_object_or_404(
        get_all_entries(request, request.user.all_entries), slug=slug
    )
    old_files = entry.old_files
    # Sort the previously uploaded files by timestamp
    sorted_files = dict(
        sorted(old_files.items(), key=lambda item: item[1][1], reverse=True)
    )
    # Prepare texts for 'Delete entry' modal
    modal_text = (f'Are you sure you want to delete "{entry.title}"?'
                  f'This action cannot be undone!')
    modal_title = f'Delete "{entry.title}"?'

    comments = entry.all_comments.select_related("author", "author__profile")

    if request.method == "POST":
        process_comment_form(request, entry)
        # Redirect after comment posting to prevent resend of POST data on
        # page refresh 
        return redirect('dashboard_entry', username=username, slug=slug)

    comment_form = CommentForm()

    context = {
        "entry": entry,
        "old_files": sorted_files,
        "comments": comments,
        "comment_form": comment_form,
        "modal_text": modal_text,
        "modal_title": modal_title,
        "dashboard_view": dashboard_view,
    }

    return render(request, "users/dashboard_entry.html", context)


def edit_profile(request, username):
    """
    Display a form with the profile data of an authenticated user

    This view retrieves the automatically created profile of the authenticated
    user and renders the dashboard and the sidebar with the relevant context.
    The view handles POST requests whenever the profile is updated.

    Args:
        request (HttpObject): The HTTP request object.
        username (str): The username of the user whose profile is being
            displayed for editing.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        ValidationError (see ProfileForm class for error handling)

    Returns:
        HttpResponse: Redirects to the 'dashboard' page if the profile was
            successfully saved.
        HttpResponse: The HTTP response object containing the rendered profile
            form page.
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    profile = request.user.profile

    if request.method == "POST" and profile.user == request.user:
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            new_file=request.FILES.get("pic"),
        )
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.save()
            messages.success(request, "Your profile has been saved.")
            return redirect('dashboard', username=username)

        else:
            messages.error(request, "There was an error saving your profile.")

    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        "profile": profile,
        "profile_form": profile_form,
    }

    return render(request, "users/profile_form.html", context)


def user_favorites(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    likes = request.user.liked.select_related("entry").annotate(
        likes_received=Count("entry__all_likes", distinct=True),
        comments_received=Count("entry__all_comments", distinct=True),
    )
    is_favorite = 1

    page_obj = get_page_obj(request, likes)
    print(page_obj[0].entry.author.username)

    context = {
        "page_obj": page_obj,
        "is_favorite": is_favorite,
    }

    return render(request, "users/dashboard_user_likes.html", context)


def user_comments(request, username):
    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    comments = request.user.commenter.select_related("entry")

    page_obj = get_page_obj(request, comments, 10)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "users/dashboard_user_comments.html", context)
