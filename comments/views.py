from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .forms import CommentForm


def edit_comment(request, current_path, comment_id):
    """
    Process the editing of an existing comment by an authenticated user

    This view is triggered via comments.js after the user clicks the "Edit"
    button. Since the user could be coming from a variety of views, the path
    they come from is cleaned by the JS file and passed on as 'current_path'
    so the user can return to it.

    The function retrieves a comment by its ID, ensuring that the comment
    belongs to the current authenticated user.

    Since the editing of the comment is executed in-place by un-hiding the
    textarea for editing, the page can contain multiple POST forms. Therefore,
    the Update button contains the name attribute 'updateOld' to distinguish it
    from the original Comment button at the top of the comment section.
    This view only processes POST data if it was submitted by the 'updateOld'
    button.

    The user receives feedback on saving the comment via success/error message
    and is then redirected to the previous path.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        current_path (str): The current path to redirect back to after editing
            the comment.
        comment_id (int): The ID of the comment to be edited.

    Returns:
        HttpResponseRedirect: A redirect response to the specified path.
        
    Raises:
        PermissionDenied: If the user is not authenticated.
        Http404: If the user has no comment with the specified ID.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)

    if request.method == "POST" and comment.author == request.user:
        if "updateOld" in request.POST:
            # print(request.POST)
            comment_form = CommentForm(data=request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                messages.success(request, "Your comment has been saved.")
            else:
                # print(comment_form.errors.as_data())
                messages.error(request, "Your comment was not saved.")

        return redirect(f"{reverse('home')}{current_path}")


def delete_comment(request, current_path, comment_id):
    """
    Handle the deletion of a comment by an authenticated user

    This function retrieves a comment by its ID from the current authenticated
    user's comments. If found, the comment is deleted and a success message is
    displayed. The user is then redirected to the specified path.

    The file comments.js is responsible for retrieving the comment ID and
    cleaning the return path.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        current_path (str): The current path to redirect back to after deleting
            the comment.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        HttpResponseRedirect: A redirect response to the specified path.

    Raises:
        PermissionDenied: If the user is not authenticated.
        Http404: If the user has no comment with the specified ID.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    comment = get_object_or_404(request.user.commenter.all(), id=comment_id)
    comment.delete()
    messages.success(request, "Your comment has been deleted.")

    return redirect(f"{reverse('home')}{current_path}")
