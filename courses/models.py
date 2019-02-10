# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Section(models.Model):
    #nr = models.IntegerField(default=0, null=True, blank=True)
    text = models.TextField(null=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    start = models.TimeField(null=True)
    duration = models.DurationField(null=True)
    song = models.ForeignKey('songs.Song', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])


class Course(models.Model):
    title = models.TextField()
    target_group = models.TextField(null=True)
    male_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, related_name="male_instructors")
    female_instructor = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, related_name="female_instructors")
    # Has variable amount of sections
    external = models.BooleanField(default=False)

    start_date = models.DateTimeField(default=timezone.now, null=True, blank=False)
    int_duration = models.DurationField(default=90, null=True, blank=False)

    def __str__(self):
        return self.title
