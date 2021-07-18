from django.contrib import admin
from events.models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'place']
    ordering = []
    list_filter = []
    readonly_fields = ['creator', 'created', 'last_edited', 'last_editor']
    filter_horizontal = ['participants']
    search_fields = ['title', 'place']

    # search_fields = ['instructors'] # test
    # autocomplete_fields = ['instructors'] # test

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'date_joined', 'is_earlybird']
    ordering = ['event__start']
    list_filter = ['is_earlybird']
    readonly_fields = ['date_joined']
    filter_horizontal = []
    search_fields = ['user', 'event']

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
