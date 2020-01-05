# imports:
from django.contrib import admin
from videos.models import *
# End: imports -----------------------------------------------------------------

# actions:

# End: actions -----------------------------------------------------------------

# filters:

# End: filters -----------------------------------------------------------------


# managers:
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty']
    list_editable = ['difficulty']
    list_filter = ['tags', 'difficulty']
    search_fields = ['title', 'creator__email', 'creator__first_name', 'creator__last_name']
    ordering = ['difficulty', 'title']
    readonly_fields = ['created', 'creator']
    filter_horizontal = ['tags']
# End: managers ----------------------------------------------------------------

# Register your models here.
admin.site.register(Video, VideoAdmin)
# admin.site.register(VideoTag)
