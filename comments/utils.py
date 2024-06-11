from .forms import CommentForm
from django.contrib import messages

def process_comment_form(request, entry):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.entry = entry
            comment.save()
            messages.success(request, "Your comment has been saved.")
            
       # print(request.POST)

    comment_form = CommentForm()
    
    return comment_form