from django.contrib import admin
from courses.models import *

# Register your models here.

class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'nr']
    list_display_links = ['title', 'course']
    ordering = ['course', 'nr']
    readonly_fields = ['course', 'nr', 'description']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lead', 'follow', 'date', 'place']
    ordering = ['date', 'start']
    list_filter = ['tags']
    readonly_fields = ['created', 'last_edited', 'last_editor']
    filter_horizontal = ['tags', 'instructors']
    search_fields = ['title', 'place', 'lead__first_name', 'follow__first_name']

    # search_fields = ['instructors'] # test
    autocomplete_fields = ['instructors'] # test

admin.site.register(Section, SectionAdmin)
admin.site.register(Course, CourseAdmin)
