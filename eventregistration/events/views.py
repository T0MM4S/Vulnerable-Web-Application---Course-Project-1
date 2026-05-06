from django.shortcuts import render, redirect, get_object_or_404
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
            comments = request.POST.get('comments', '')
            cursor = connection.cursor()
            query = f"INSERT INTO events_registration (event_id, user_id, comments, registered_at) VALUES ({event_id}, {request.user.id}, '{comments}', datetime('now'))"
            cursor.execute(query)
            return redirect('participants', event_id=event_id)
    else:
        form = RegistrationForm()
    return render(request, 'events/register_event.html', {'event': event, 'form': form})

@login_required
def participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    search_query = request.GET.get('search', '')
    if search_query:
        cursor = connection.cursor()
        query = f"SELECT * FROM events_registration WHERE event_id = {event_id} AND comments LIKE '%{search_query}%'"
        cursor.execute(query)
        registrations = Registration.objects.filter(event=event)
    else:
        registrations = Registration.objects.filter(event=event)
    return render(request, 'events/participants.html', {'event': event, 'registrations': registrations})