# imports:
from django.contrib import admin
from songs.models import *
# End: imports -----------------------------------------------------------------

# actions:

# End: actions -----------------------------------------------------------------

# filters:
class BPMFilter(admin.SimpleListFilter):
    title = 'bpm'
    parameter_name = 'bpm'

    def lookups(self, request, model_admin):
        return [
            ('slow', 'Less than 62'),
            ('medium', '63 to 75'),
            ('fast', 'Greater than 76')
        ]

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset

        if self.value() == 'slow':
            return queryset.filter(bpm__lte=62)

        if self.value() == 'medium':
            return queryset.filter(bpm__gte=63, bpm__lte=75)

        if self.value() == 'fast':
            return queryset.filter(bpm__gte=76)
# End: filters -----------------------------------------------------------------



# managers:
class SongManager(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['tittel', 'artist', 'bpm'] } ),
        ('Links', {'fields': ['spotify_URL', 'spotify_URI'] } ),
    )
    list_display = ['tittel', 'artist', 'bpm']
    list_filter = [BPMFilter, 'tags']
    search_fields = ['tittel', 'artist']
    ordering = ['bpm', 'tittel']
    readonly_fields = []
# End: managers ----------------------------------------------------------------

# Register your models here.
admin.site.register(Song, SongManager)
admin.site.register(SongTag)
admin.site.register(File)
