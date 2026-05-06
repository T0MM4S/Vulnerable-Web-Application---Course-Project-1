import os

# Create directory structure (in case some are missing)
os.makedirs('eventregistration/eventregistration', exist_ok=True)
os.makedirs('eventregistration/events/templates/events', exist_ok=True)
os.makedirs('screenshots', exist_ok=True)

# File contents
files = {
    'eventregistration/manage.py': '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventregistration.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
''',
    
    'eventregistration/eventregistration/__init__.py': '',
    
    'eventregistration/eventregistration/asgi.py': '''"""
ASGI config for eventregistration project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventregistration.settings')

application = get_asgi_application()
''',

    'eventregistration/eventregistration/wsgi.py': '''"""
WSGI config for eventregistration project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventregistration.settings')

application = get_wsgi_application()
''',

    'eventregistration/eventregistration/settings.py': '''"""
Django settings for eventregistration project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# FLAW 1: A01:2021 - Broken Access Control
# Issue: DEBUG mode is enabled in production, exposing sensitive information
SECRET_KEY = 'django-insecure-hardcoded-secret-key-do-not-use-in-production-12345'
DEBUG = True  # Exposes error pages with sensitive information
ALLOWED_HOSTS = ['*']  # Allows any host

# FIX 1: Disable DEBUG in production and use environment variables
# import os
# SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-development')
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Source: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # FLAW 2: A01:2021 - Broken Access Control (CSRF Protection Disabled)
    # 'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection is DISABLED
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# FIX 2: Enable CSRF protection by uncommenting the middleware
# Uncomment the line above: 'django.middleware.csrf.CsrfViewMiddleware',
# Source: https://docs.djangoproject.com/en/4.2/ref/csrf/

ROOT_URLCONF = 'eventregistration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventregistration.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []  # FLAW 3 - Weak password validation

# FIX 3: A07:2021 - Identification and Authentication Failures
# Enable strong password validators to prevent weak passwords
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 12,
#         }
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
# Source: https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#module-django.contrib.auth.password_validation

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FLAW 4: A05:2021 - Security Misconfiguration
# Missing security headers
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'ALLOW'

# FIX 4: Enable security headers
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True  # Only in production with HTTPS
# SESSION_COOKIE_SECURE = True  # Only in production with HTTPS
# CSRF_COOKIE_SECURE = True  # Only in production with HTTPS
# Source: https://docs.djangoproject.com/en/4.2/ref/middleware/#module-django.middleware.security
''',

    'eventregistration/eventregistration/urls.py': '''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]
''',

    'eventregistration/events/__init__.py': '',
    
    'eventregistration/events/admin.py': '''from django.contrib import admin
from .models import Event, Registration

admin.site.register(Event)
admin.site.register(Registration)
''',

    'eventregistration/events/apps.py': '''from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
''',

    'eventregistration/events/models.py': '''from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_participants = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('event', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
''',

    'eventregistration/events/forms.py': '''from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
''',

    'eventregistration/events/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('event/<int:event_id>/participants/', views.participants, name='participants'),
]
''',

    'eventregistration/events/views.py': '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Event, Registration
from .forms import RegistrationForm

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'events/login.html')

@login_required
def index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # FLAW 5: A03:2021 - Injection (SQL Injection)
            # Using raw SQL with unsanitized user input
            comments = request.POST.get('comments', '')
            cursor = connection.cursor()
            query = f"INSERT INTO events_registration (event_id, user_id, comments, registered_at) VALUES ({event_id}, {request.user.id}, '{comments}', datetime('now'))"
            cursor.execute(query)
            
            # FIX 5: Use Django ORM or parameterized queries
            # registration = Registration(
            #     event=event,
            #     user=request.user,
            #     comments=form.cleaned_data['comments']
            # )
            # registration.save()
            # Source: https://docs.djangoproject.com/en/4.2/topics/security/#sql-injection-protection
            
            return redirect('participants', event_id=event_id)
    else:
        form = RegistrationForm()
    
    return render(request, 'events/register_event.html', {'event': event, 'form': form})

@login_required
def participants(request, event_id):
    # FLAW 3: A01:2021 - Broken Access Control
    # No authorization check - any logged-in user can view any event's participants
    event = get_object_or_404(Event, pk=event_id)
    
    # FIX 3 (Part 2): Implement proper access control
    # if request.user != event.created_by and not Registration.objects.filter(event=event, user=request.user).exists():
    #     return render(request, 'events/error.html', {
    #         'message': 'You do not have permission to view this participant list.'
    #     })
    # Source: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
    
    # FLAW 4: A03:2021 - Injection (SQL Injection in search)
    search_query = request.GET.get('search', '')
    if search_query:
        cursor = connection.cursor()
        query = f"SELECT * FROM events_registration WHERE event_id = {event_id} AND comments LIKE '%{search_query}%'"
        cursor.execute(query)
        registrations = Registration.objects.filter(event=event)
    else:
        registrations = Registration.objects.filter(event=event)
    
    # FIX 4: Use ORM with proper filtering
    # if search_query:
    #     registrations = Registration.objects.filter(
    #         event=event,
    #         comments__icontains=search_query
    #     )
    # else:
    #     registrations = Registration.objects.filter(event=event)
    
    return render(request, 'events/participants.html', {
        'event': event,
        'registrations': registrations
    })
''',

    'eventregistration/events/templates/events/index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Event Registration System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .event { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
        button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h1>Welcome, {{ user.username }}!</h1>
    <h2>Available Events</h2>
    
    {% for event in events %}
    <div class="event">
        <h3>{{ event.name }}</h3>
        <p>{{ event.description }}</p>
        <p><strong>Date:</strong> {{ event.date }}</p>
        <p><strong>Max Participants:</strong> {{ event.max_participants }}</p>
        <a href="{% url 'register_event' event.id %}"><button>Register</button></a>
        <a href="{% url 'participants' event.id %}"><button>View Participants</button></a>
    </div>
    {% endfor %}
    
    <p><a href="/admin/">Admin Panel</a> | <a href="/logout/">Logout</a></p>
</body>
</html>
''',

    'eventregistration/events/templates/events/register.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        form { max-width: 400px; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Register New Account</h2>
    <form method="post">
        {{ form.as_p }}
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
</body>
</html>
''',

    'eventregistration/events/templates/events/login.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        form { max-width: 400px; }
        input { width: 100%; padding: 8px; margin: 5px 0; }
        button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
</body>
</html>
''',

    'eventregistration/events/templates/events/register_event.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Register for Event</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        form { max-width: 500px; }
        textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <h2>Register for: {{ event.name }}</h2>
    <p>{{ event.description }}</p>
    
    <form method="post">
        {{ form.as_p }}
        <button type="submit">Complete Registration</button>
    </form>
    
    <p><a href="{% url 'index' %}">Back to Events</a></p>
</body>
</html>
''',

    'eventregistration/events/templates/events/participants.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Participants</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        input { padding: 8px; margin: 10px 0; }
    </style>
</head>
<body>
    <h2>Participants for: {{ event.name }}</h2>
    
    <form method="get">
        <input type="text" name="search" placeholder="Search comments..." value="{{ request.GET.search }}">
        <button type="submit">Search</button>
    </form>
    
    <table>
        <tr>
            <th>Username</th>
            <th>Registered At</th>
            <th>Comments</th>
        </tr>
        {% for reg in registrations %}
        <tr>
            <td>{{ reg.user.username }}</td>
            <td>{{ reg.registered_at }}</td>
            <td>{{ reg.comments|safe }}</td>
        </tr>
        {% endfor %}
    </table>
    
    <p><a href="{% url 'index' %}">Back to Events</a></p>
</body>
</html>
''',
}

# Create all files
print("Creating project files...")
for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created {filepath}")

print("\n All files created successfully!")
print("\nNext steps:")
print("1. Install Django: pip install django==4.2")
print("2. Run migrations: python eventregistration/manage.py migrate")
print("3. Create superuser: python eventregistration/manage.py createsuperuser")
print("4. Run server: python eventregistration/manage.py runserver")