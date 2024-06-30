"""
urls.py for the "Comments" app

Registers all comment-related URL patterns.
"""

from django.urls import path

from . import views

urlpatterns = [
    path(
        "<path:current_path>/delete-comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "<path:current_path>/edit-comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
]
