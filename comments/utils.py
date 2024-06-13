from .forms import CommentForm
from django.contrib import messages

def process_comment_form(request, entry):
    """ Process the comment form submission and save the comment

    This function handles the submission of the comment form. It saves the
    logged-in user and the entry as foreign keys and displays a success message
    or an error message to the user.
    Always returns an empty comment form.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        entry (Entry): The entry object to which the comment is being added.

    Returns:
        CommentForm: An instance of the comment form.
    """

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.entry = entry
            comment.save()
            messages.success(request, "Your comment has been saved.")
        else:
            messages.error(request, "Your comment could not be saved.")
            
    comment_form = CommentForm()
    
    return comment_form