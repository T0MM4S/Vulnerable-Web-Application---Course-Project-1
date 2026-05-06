from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('event/<int:event_id>/participants/', views.participants, name='participants'),
]
