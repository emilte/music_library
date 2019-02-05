# imports
from django.db import models

# End: imports -----------------------------------------------------------------

class Artist(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return self.name

class Song(models.Model):
    artist = models.CharField(max_length=150, null=False, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    bpm = models.SmallIntegerField(blank=True, null=True)
    spotify = models.URLField(null=False, blank=False)
    URI = models.CharField(max_length=300, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return "{} - {} ({} bpm)".format(self.title, self.artist, self.bpm)
