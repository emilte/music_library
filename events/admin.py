from django.contrib import admin
from events.models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'place']
    ordering = ['start', 'title']
    list_filter = []
    readonly_fields = ['creator', 'created', 'last_edited', 'last_editor']
    filter_horizontal = ['participants']
    search_fields = ['title', 'place']

    # search_fields = ['instructors'] # test
    # autocomplete_fields = ['instructors'] # test

admin.site.register(Event, EventAdmin)
