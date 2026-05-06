from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('event/<int:event_id>/participants/', views.participants, name='participants'),
]
