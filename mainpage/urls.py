"""
urls.py for the "Mainpage" app

Registers all mainpage-related URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("filter/tag/<str:tag>/", views.filter_tag, name="filter_tag"),
    path("filter/user/<str:username>/", views.filter_user, name="filter_user"),
]
