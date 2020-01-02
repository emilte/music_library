from django.contrib import admin
from courses.models import *

# Register your models here.

class SectionManager(admin.ModelAdmin):
    list_display = ['title', 'course', 'nr']
    list_display_links = ['title', 'course']
    ordering = ['course', 'nr']
    readonly_fields = ['nr', 'description']

class CourseManager(admin.ModelAdmin):
    list_display = ['title', 'lead', 'follow', 'date', 'place']
    ordering = ['date', 'start']
    readonly_fields = ['created', 'last_edited', 'last_editor']
    filter_horizontal = ['tags', 'instructors']

    # search_fields = ['instructors'] # test
    autocomplete_fields = ['instructors'] # test

admin.site.register(Section, SectionManager)
admin.site.register(Course, CourseManager)
