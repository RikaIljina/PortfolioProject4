from django.urls import path
from . import views
# from mainpage import index as main_index

urlpatterns = [
    path('', views.index, name='home'),
]