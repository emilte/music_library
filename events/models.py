# imports
from django.db import models
from django.conf import settings
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Event(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, verbose_name="Tittel")
    place = models.CharField(max_length=140, null=True, blank=True, verbose_name="Sted")
    start = models.DateTimeField(null=True, blank=True, verbose_name="Start")
    end = models.DateTimeField(null=True, blank=True, verbose_name="Slutt")
    description = models.TextField(null=True, blank=True, verbose_name="Beskrivelse")
    facebook_url = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="events", verbose_name="Påmeldte")

    last_edited = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Sist redigert")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="last_edited_events", verbose_name="Sist redigert av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")
    creator = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet av")


    class Meta:
        ordering = ['start', 'title']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.id}"
        # return "{} ({})".format(self.getTitle(), self.getDate())

    def save(self, *args, **kwargs):
        creator = kwargs.pop('creator', None)
        last_editor = kwargs.pop('last_editor', None)

        if not self.id:
            self.created = timezone.now()
            if creator: self.creator = creator

        self.last_edited = timezone.now()
        if last_editor: self.last_editor = last_editor

        return super(type(self), self).save(*args, **kwargs)
