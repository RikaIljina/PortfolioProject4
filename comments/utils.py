"""
utils.py for the 'Comments' app

This module contains comment-related functions that are used by the views.

process_comment_form(): Process the POST request after comment form submission
    and save the comment
"""

from django.contrib import messages

from .forms import CommentForm


def process_comment_form(request, entry):
    """
    Process the comment form submission and save the comment

    This function handles the POST request after the submission of the comment
    form. It saves the authenticated user and the entry as foreign keys and
    displays a success message or an error message to the user.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        entry (Entry): The entry object to which the comment is being added.
    """

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.entry = entry
            comment.save()
            messages.success(request, "Your comment has been saved.")
        else:
            messages.error(request, "Your comment could not be saved.")
