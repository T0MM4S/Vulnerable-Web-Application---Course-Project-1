from django.contrib import admin

from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'max_participants', 'created_by')
    search_fields = ('name', 'description')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at')
    search_fields = ('event__name', 'user__username', 'comments')
