from django.urls import path
from . import views

urlpatterns = [

    path('like/<int:entry_id>/', views.add_like, name='add_like_home'),
    path('<path:current_path>/like/<int:entry_id>/', views.add_like, name='add_like'),
]
