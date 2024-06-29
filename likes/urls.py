from django.urls import path
from . import views

urlpatterns = [
    path("like/<int:entry_id>/", views.add_like, name="add_like_home"),
    path(
        "<path:current_path>/like/<int:entry_id>/",
        views.add_like,
        name="add_like",
    ),
    path(
        "like/delete-by-entry/<int:entry_id>/",
        views.delete_like_by_entry,
        name="delete_like_by_entry",
    ),
    path(
        "<path:current_path>/like/delete-by-entry/<int:entry_id>/",
        views.delete_like_by_entry,
        name="delete_like_by_entry",
    ),
    path(
        "like/delete-by-like/<int:like_id>/",
        views.delete_like_by_like,
        name="delete_like_by_like",
    ),
    path(
        "<path:current_path>/like/delete-by-like/<int:like_id>/",
        views.delete_like_by_like,
        name="delete_like_by_like",
    ),
]
