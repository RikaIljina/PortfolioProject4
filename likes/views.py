"""
views.py for the 'Likes' app.

This module contains view functions that handle the creation, retrieval, and
management of 'likes' on the website.

Key functionalities:
- Add a like to an entry
- Delete a like from an entry

View Functions:
- add_like(request, entry_id, current_path): Handles the addition of a like 
  to an entry.
- delete_like_by_entry(request, entry_id, current_path): Handles the removal of
  a like from an entry by entry ID.
- delete_like_by_like(request, like_id, current_path): Handles the removal of
  a like from an entry by like ID.
"""

from django.shortcuts import get_object_or_404, reverse, redirect
from django.core.exceptions import PermissionDenied

from entries.models import Entry

from .models import Like


def add_like(request, entry_id, current_path=""):
    """
    Add a like to a specified entry for the authenticated user

    This view function is triggered when a user clicks on a like button, it
    handles the process of adding a like to an entry. 
    If the user is not authenticated, it raises a PermissionDenied exception.
    If the user is authenticated, it checks if the entry with the given
    'entry_id' exists and is public (publish=1). If the user has not already
    liked this entry, a new Like object is created for the user and entry.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        entry_id (int): The ID of the entry to be liked.
        current_path (str, optional): The current path to redirect to after 
            processing the like. Defaults to an empty string.

    Raises:
        PermissionDenied: If the user is not authenticated.

    Returns:
        HttpResponseRedirect: Redirects to the home page with the current 
            path and any existing GET parameters.
    """

    if not request.user.is_authenticated:
        raise PermissionDenied

    entry = get_object_or_404(
        Entry.objects.filter(publish=1), id=entry_id)

    if not request.user.liked.filter(entry__pk=entry_id).exists():
        Like.objects.create(user=request.user, entry=entry)

    # Needed to preserve sorting and page parameters
    if request.GET.dict():
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    return redirect(f"{reverse('home')}{current_path}{params}")


def delete_like_by_entry(request, entry_id, current_path=""):
    """
    Delete a like from a specified entry for the authenticated user

    This view function is triggered when a user clicks on a like button on an
    already liked entry; it handles the process of deleting the like. 
    If the user is not authenticated, it raises a PermissionDenied exception.
    If the user is authenticated, it looks for the entry with the given
    'entry_id' among the user's liked entries. If it is found, the Like object
    is deleted.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        entry_id (int): The ID of the entry to be unliked.
        current_path (str, optional): The current path to redirect to after 
            processing the unlike. Defaults to an empty string.

    Raises:
        PermissionDenied: If the user is not authenticated.

    Returns:
        HttpResponseRedirect: Redirects to the home page with the current 
            path and any existing GET parameters.
    """
    
    if not request.user.is_authenticated:
        raise PermissionDenied

    like = request.user.liked.filter(entry__pk=entry_id).first()
    if like:
        like.delete()

    # Needed to preserve sorting and page parameters
    if request.GET.dict():
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    return redirect(f"{reverse('home')}{current_path}{params}")


def delete_like_by_like(request, like_id, current_path=""):
    """
    Delete a specified like for the authenticated user

    This view function is triggered when a user clicks on a like button on an
    already liked entry while on the 'Favorites' page of the dashboard.
    It handles the process of deleting the like by the like ID.
    If the user is not authenticated, it raises a PermissionDenied exception.
    If the user is authenticated, it looks for the like with the given
    'like_id' among the user's likes. If it is found, the Like object
    is deleted.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        entry_id (int): The ID of the like to be deleted.
        current_path (str, optional): The current path to redirect to after 
            processing the unlike. Defaults to an empty string.

    Raises:
        PermissionDenied: If the user is not authenticated.

    Returns:
        HttpResponseRedirect: Redirects to the home page with the current 
            path and any existing GET parameters.
    """
    
    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.user.liked.filter(id=like_id).exists():
        like = Like.objects.get(id=like_id)
        like.delete()
    
    # Needed to preserve sorting and page parameters
    if request.GET.dict():
        params = f"?{request.GET.urlencode()}"
    else:
        params = ""

    return redirect(f"{reverse('home')}{current_path}{params}")
