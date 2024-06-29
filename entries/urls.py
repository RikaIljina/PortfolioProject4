from django.urls import path

from . import views

urlpatterns = [
    path(
        "dashboard/<str:username>/add/entry/",
        views.new_entry,
        name="new_entry",
    ),
    path(
        "dashboard/<str:username>/delete/<slug:slug>/",
        views.delete_entry,
        name="delete_entry",
    ),
    path(
        "dashboard/<str:username>/edit/<slug:slug>/",
        views.edit_entry,
        name="edit_entry",
    ),
    path(
        "dashboard/<str:username>/edit/<slug:slug>/delete-file/<str:file_id>/",
        views.delete_old_file,
        name="delete_old_file",
    ),
    path("song/<slug:slug>/", views.entry_details, name="entry_details"),
]
