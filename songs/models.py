# imports
from django.db import models

# End: imports -----------------------------------------------------------------

class SongTag(models.Model):
    navn = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return self.navn

class Song(models.Model):
    tittel = models.CharField(max_length=150, null=False, blank=False)
    artist = models.CharField(max_length=150, null=False, blank=False)
    bpm = models.SmallIntegerField(blank=True, null=True)
    spotify_URL = models.URLField(null=False, blank=False)
    spotify_URI = models.CharField(max_length=300, null=True, blank=True)
    tags = models.ManyToManyField('songs.SongTag', blank=True)

    def __str__(self):
        return "{} - {} ({} bpm)".format(self.tittel, self.artist, self.bpm)

class File(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='mediaroot/')

    def __str__(self):
        return "File {}".format(self.id)
