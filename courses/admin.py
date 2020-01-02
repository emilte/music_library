from django.contrib import admin
from courses.models import *

# Register your models here.

class CourseManager(admin.ModelAdmin):
    list_display = ['title', 'lead', 'follow', 'date', 'place']
    ordering = ['date', 'start']
    readonly_fields = ['created', 'last_edited', 'last_editor']
    filter_horizontal = ['tags']

admin.site.register(Section)
admin.site.register(Course, CourseManager)
