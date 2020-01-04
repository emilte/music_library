from django.contrib import admin
from wiki.models import *

# managers:
class PageManager(admin.ModelAdmin):
    list_display = ['title', 'folder', 'path', 'private']
    search_fields = ['title', 'folder__title']
    ordering = ['title']
    readonly_fields = ['content', 'last_edited', 'last_editor', 'created', 'creator']
    list_editable = ['path', 'private']

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user
        super().save_model(request, obj, form, change)

class FolderManager(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    ordering = ['title']
    readonly_fields = ['last_edited', 'last_editor', 'created', 'creator']

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user
        super().save_model(request, obj, form, change)

# End: managers ----------------------------------------------------------------

admin.site.register(Page, PageManager)
admin.site.register(Folder, FolderManager)
