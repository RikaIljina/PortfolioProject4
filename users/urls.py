"""
urls.py for the "Users" app

Registers all user- and dashboard-related URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_new_user, name="dashboard_new_user"),
    path("dashboard/<str:username>/", views.dashboard, name="dashboard"),
    path(
        "dashboard/<str:username>/comments/",
        views.user_comments,
        name="user_comments",
    ),
    path(
        "dashboard/<str:username>/edit-profile/",
        views.edit_profile,
        name="edit_profile",
    ),
    path(
        "dashboard/<str:username>/entry/<slug:slug>/",
        views.dashboard_entry,
        name="dashboard_entry",
    ),
    path(
        "dashboard/<str:username>/favorites/",
        views.user_favorites,
        name="user_favorites",
    ),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
]
