# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    tittel = models.CharField(max_length=140, null=True, blank=False, default="")
    fører = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="male_courses")
    følger = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="female_courses")
    dato = models.DateField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    slutt = models.DateTimeField(null=True, blank=True)
    #varighet = models.TimeField(null=True, blank=True)
    kommentarer = models.TextField(null=True, blank=True, default="")
    sted = models.CharField(max_length=140, null=True, blank=True, default="")
    tags = models.ManyToManyField('videos.VideoTag')

    def __str__(self):
        return "{} ({})".format(self.tittel, self.getDato())

    def getDato(self):
        try:
            return self.dato.strftime("%d.%m.%y")
        except:
            return None

    def getStart(self):
        try:
            return self.start.strftime("%H:%M")
        except:
            return None

    def getSlutt(self):
        try:
            return self.slutt.strftime("%H:%M")
        except:
            return None

    def getTags(self):
        return [navn[0] for navn in self.tags.all().values_list('navn') ]



class Section(models.Model):
    nr = models.IntegerField(null=True, blank=True)
    tittel = models.CharField(max_length=140, null=True, blank=False, default="")
    beskrivelse = models.TextField(null=True, blank=True, default="")
    start = models.TimeField(null=True, blank=True)
    varighet = models.IntegerField(null=True, blank=False)
    # varighet2 = models.IntegerField(null=True, blank=True)
    #varighet2 = models.DurationField(null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    song = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return "Section ({}) in course: {}".format(self.nr, self.course)
        #return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])

    def getStart(self):
        return self.start.strftime("%H:%M")

    def getSong(self):
        return self.song or "Ingen valgt"
