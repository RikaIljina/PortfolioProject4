from django.urls import path
from django.urls import include, re_path
from . import views

urlpatterns = [
    path('dashboard/<str:username>/new-entry/', views.new_entry, name='new_entry'),
    path('dashboard/<str:username>/delete/<slug:slug>/', views.delete_entry, name='delete_entry'),
    path('dashboard/<str:username>/edit/<slug:slug>/', views.edit_entry, name='edit_entry'),
    path('song/<slug:slug>/', views.entry_details, name='entry_details'),
]