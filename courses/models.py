# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Section(models.Model):
    #nr = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=140, null=True, blank=True, default="default section")
    text = models.TextField(max_length=140, null=True, blank=True, default="")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    start = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    song = models.ForeignKey('songs.Song', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="sections")

    def __str__(self):
        return self.title
        #return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])


class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=True, default="default course")
    male_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="male_courses")
    female_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="female_courses")
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    int_duration = models.DurationField(default=90, null=True, blank=True)

    #sections = models.ManyToManyField('courses.Section', blank=True)
    external = models.BooleanField(default=False, blank=True)
    target_group = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return self.title
