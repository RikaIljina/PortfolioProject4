from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:slug>/', views.entry_details, name='entry_details'),
    path('filter/<str:username>/', views.filter_user, name='filter_user'),
]