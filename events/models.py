# imports
from django.db import models
from django.conf import settings
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Event(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, verbose_name="Tittel")
    place = models.CharField(max_length=140, null=True, blank=True, verbose_name="Sted")
    date = models.DateField(null=True, blank=True, verbose_name="Dato")
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True, verbose_name="Slutt")
    # lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_events", verbose_name="Instruktør (lead)")
    # follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="follow_events", verbose_name="Instruktør (follow)")
    description = models.TextField(null=True, blank=True, verbose_name="Beskrivelse")
    comments = models.TextField(null=True, blank=True, verbose_name="Kommentarer")
    tags = models.ManyToManyField('songs.Tag', blank=True)

    last_edited = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Sist redigert")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="last_edited_events", verbose_name="Sist redigert av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")
    creator = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet av")

    # NOTE: Under development
    # instructors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # instructors = models.ManyToManyField('accounts.Instructor', blank=True)
    # bulk = models.PositiveIntegerField(null=True, blank=True, verbose_name="Bolk")
    # day = models.PositiveIntegerField(null=True, blank=True, verbose_name="Dag")
    #
    # semester_choice = models.IntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)
    # semester_char = models.CharField(max_length=5, null=True, blank=True)


    class Meta:
        ordering = ['date', 'title']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return "{} ({})".format(self.getTitle(), self.getDate())


    def getTags(self):
        return [title[0] for title in self.tags.all().values_list('title') ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        return super(type(self), self).save(*args, **kwargs)
