# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    male_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="male_courses")
    female_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="female_courses")
    #date = models.DateTimeField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=140, null=True, blank=True, default="")

    #sections = models.ManyToManyField('courses.Section', blank=True)
    external = models.BooleanField(default=False, blank=True)
    target_group = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return self.title

class Section(models.Model):
    nr = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    text = models.TextField(max_length=140, null=True, blank=True, default="")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    start = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    song = models.ForeignKey('songs.Song', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return self.title
        #return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])
