from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('filter/user/<str:username>/', views.filter_user, name='filter_user'),
    path('filter/tag/<str:tag>/', views.filter_tag, name='filter_tag'),
]