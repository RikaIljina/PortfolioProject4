from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('dashboard/', views.dashboard_new_user, name='dashboard_new_user'),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('dashboard/<str:username>/edit-profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/<str:username>/new-entry/', views.new_entry, name='new_entry'),
    path('dashboard/<str:username>/<slug:slug>/', views.dashboard_entry, name='dashboard_entry'),
    path('dashboard/<str:username>/delete/<slug:slug>/', views.delete_entry, name='delete_entry'),
    path('dashboard/<str:username>/edit/<slug:slug>/', views.edit_entry, name='edit_entry'),

]
