from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('<path:current_path>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('<path:current_path>/edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('dashboard/', views.dashboard_new_user, name='dashboard_new_user'),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('dashboard/<str:username>/edit-profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/<str:username>/favorites/', views.user_favorites, name='user_favorites'),
    path('dashboard/<str:username>/comments/', views.user_comments, name='user_comments'),
    path('dashboard/<str:username>/new-entry/', views.new_entry, name='new_entry'),
    path('dashboard/<str:username>/<slug:slug>/', views.dashboard_entry, name='dashboard_entry'),
    path('dashboard/<str:username>/delete/<slug:slug>/', views.delete_entry, name='delete_entry'),
    path('dashboard/<str:username>/edit/<slug:slug>/', views.edit_entry, name='edit_entry'),
]
