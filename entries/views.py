from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
import cloudinary

from mainpage.utils import get_all_tags
from users.utils import get_all_usernames
from comments.forms import CommentForm
from comments.utils import process_comment_form
from .models import Entry
from .forms import EntryForm
from .utils import get_published_entries


def entry_details(request, slug):
    """
    Display a detailed view of a published entry

    This view retrieves a published entry by its slug and displays it on the
    main page. It gives access to all uploaded audio files and the comment
    section.
    The view also retrieves the user and tag names for the filter functionality
    and handles POST requests whenever a new comment is submitted.

    Args:
        request (HttpObject): Http object
        slug (string): Slug of the entry to be shown in detailed view

    Raises:
        Http404: If there is no public entry with the specified slug.
    """

    entry = get_object_or_404(
        get_published_entries(request, Entry.objects), slug=slug
    )
    # Sort old audio files by timestamp. The json object in entry.old_files
    # has the structure {'cloudinary_id': ['cloudinary_url', 'timestamp']}
    old_files = dict(
        sorted(
            entry.old_files.items(), key=lambda item: item[1][1], reverse=True
        )
    )

    comments = entry.all_comments.select_related("author", "author__profile")

    users = get_all_usernames()
    tags = get_all_tags()

    if request.user.is_authenticated and request.method == "POST":
        process_comment_form(request, entry)
        return redirect(f"{reverse('entry_details', args=[slug])}")

    comment_form = CommentForm()

    context = {
        "entry": entry,
        "old_files": old_files,
        "comments": comments,
        "users": users,
        "tags": tags,
        "comment_form": comment_form,
    }

    return render(request, "entries/entry_details.html", context)


def new_entry(request, username):
    """
    Handle the creation of a new entry

    This view handles both the GET and POST requests for creating a new entry.
    If the request method is GET, it displays the entry form.
    If the request method is POST, it validates and saves the form data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        username (str): The username of the user attempting to create a new
            entry.

    Returns:
        HttpResponse: Redirects to the dashboard page with the entry details if
            the form is successfully saved.
        HttpResponse: Renders the entry form page with the entry form context
            if the request method is GET.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        ValidationError (see EntryForm methods)
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    if request.method == "POST":
        entry_form = EntryForm(request.POST, request.FILES, user=request.user)
        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            # See overridden EntryForm clean_[field]() method for additional
            # validation logic that is run before the final save() call
            entry.save()
            entry_form.save_m2m()
            new_slug = Entry.objects.get(id=entry.id).slug
            messages.success(request, "Your entry has been saved.")

            return HttpResponseRedirect(
                reverse("dashboard_entry", args=[username, new_slug])
            )
        else:
            messages.warning(request, "Your entry could not be saved.")
            # Validation errors are shown to the user on the web page

    else:
        entry_form = EntryForm(user=request.user)

    context = {
        "entry_form": entry_form,
    }

    return render(request, "entries/entry_form.html", context)


def edit_entry(request, username, slug):
    """
    Handle the editing of an existing entry

    This view handles both the GET and POST requests for editing an existing
    entry.
    If the request method is GET, it displays the entry form pre-filled with
    the current entry data. If the request method is POST, it validates and
    saves the form data, including handling file updates.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        username (str): The username of the user attempting to edit the entry.
        slug (str): The slug of the entry being edited.

    Returns:
        HttpResponse: Redirects to the dashboard page with entry details if the
            form is successfully saved.
        HttpResponse: Renders the entry form page with the entry form context
            if the request method is GET or the form submission fails.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        Http404: If the user has no entry with the specified slug.
        ValidationError (see EntryForm methods)
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)
    # Sort old audio files by timestamp. The json object in entry.old_files
    # has the structure {'cloudinary_id': ['cloudinary_url', 'timestamp']}
    old_files = dict(
        sorted(
            entry.old_files.items(), key=lambda item: item[1][1], reverse=True
        )
    )
    # Remove quotation marks and seconds from timestamp
    old_files = {
        key: [value[0], value[1][1:-4]] for key, value in old_files.items()
    }

    if request.method == "POST":
        entry_form = EntryForm(
            request.POST,
            request.FILES,
            instance=entry,
            user=request.user,
        )

        if entry_form.is_valid():
            entry = entry_form.save()
            # See overridden EntryForm clean_[field]() methods for additional
            # validation logic that is run before the final save() call
            # Save the tag ManyToMany field
            entry_form.save_m2m()
            new_slug = entry.slug
            messages.success(request, "Your entry has been saved.")

            return HttpResponseRedirect(
                reverse("dashboard_entry", args=[username, new_slug])
            )

        else:
            messages.warning(request, "Your entry could not be saved.")
            # Validation errors are shown to the user on the web page

    else:
        tag_list = [value["name"] for value in entry.tags.all().values()]
        entry_form = EntryForm(
            instance=entry,
            user=request.user,
            initial={
                "title": entry.title,
                "description": entry.description,
                "audio_file": entry.audio_file,
                "keep_file": True,
                "tags": (",").join(tag_list),
                "publish": entry.publish,
            },
        )

    context = {
        "entry": entry,
        "entry_form": entry_form,
        "old_files": old_files,
    }

    return render(request, "entries/entry_form.html", context)


def delete_entry(request, username, slug):
    """
    Handle the deletion of an existing entry

    This view handles both the GET request for deleting an existing entry.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        username (str): The username of the user attempting to delete the
            entry.
        slug (str): The slug of the entry being deleted.

    Returns:
        HttpResponse: Redirects to the user's dashboard page if the form is
            successfully deleted.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        Http404: If the user has no entry with the specified slug.
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)
    entry.delete()
    messages.success(request, "Your entry has been deleted.")

    return HttpResponseRedirect(reverse("dashboard", args=[username]))


def delete_old_file(request, username, slug, file_id):
    """
    Handles the deletion of previous audio file versions

    This view is called via entries.js after the user clicks the 'Delete'
    button next to an audio file.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        username (str): The username of the user attempting to delete the
            entry.
        slug (str): The slug of the entry being deleted.
        file_id (str): The ID of the file being deleted.

    Returns:
        HttpResponse: Redirects to the 'edit entry' page if the file is
            successfully deleted.

    Raises:
        PermissionDenied: If the user is not authenticated or the username does
            not belong to the user making the request.
        Http404: If the user has no entry with the specified slug.
    """

    if not request.user.is_authenticated or username != request.user.username:
        raise PermissionDenied

    entry = get_object_or_404(request.user.all_entries.all(), slug=slug)

    if entry.old_files.get(file_id):
        del entry.old_files[file_id]
        entry.save()
        print(
            cloudinary.uploader.destroy(
                file_id, resource_type="video", invalidate=True
            )
        )
        messages.success(request, "Your file has been deleted.")
    else:
        messages.error(
            request,
            f"The file could not be deleted or the file id doesn't exist.",
        )

    return redirect("edit_entry", username=username, slug=slug)
