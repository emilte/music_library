# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    tittel = models.CharField(max_length=140, null=True, blank=False, default="")
    fører = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="male_courses")
    følger = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="female_courses")
    dato = models.DateTimeField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    slutt = models.TimeField(null=True, blank=True)
    varighet = models.IntegerField(null=True, blank=True)
    sted = models.CharField(max_length=140, null=True, blank=True, default="")

    #sections = models.ManyToManyField('courses.Section', blank=True)
    # external = models.BooleanField(default=False, blank=True)
    # target_group = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return self.tittel

class Section(models.Model):
    nr = models.IntegerField(null=True, blank=True)
    tittel = models.CharField(max_length=140, null=True, blank=False, default="")
    beskrivelse = models.TextField(null=True, blank=True, default="")
    kommentarer = models.TextField(null=True, blank=True, default="")
    kurs = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    start = models.TimeField(null=True, blank=True)
    varighet = models.IntegerField(null=True, blank=True)
    song = models.ForeignKey('songs.Song', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return self.tittel
        #return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])
