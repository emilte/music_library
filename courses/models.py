# imports
from django.db import models
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    lead = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="male_courses")
    follow = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="female_courses")
    date = models.DateField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    #duration = models.TimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True, default="")
    place = models.CharField(max_length=140, null=True, blank=True, default="")
    tags = models.ManyToManyField('videos.VideoTag')

    def __str__(self):
        return "course"
        # return "{} ({})".format(self.getTitle(), self.getDate())

    def getTitle(self):
        return self.title or None

    def getDate(self):
        try: return self.date.strftime("%d.%m.%y")
        except: return None

    def getStart(self):
        try: return self.start.strftime("%H:%M")
        except: return None

    def getEnd(self):
        try: return self.end.strftime("%H:%M")
        except: return None

    def getTags(self):
        return [name[0] for name in self.tags.all().values_list('name') ]



class Section(models.Model):
    nr = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    description = models.TextField(null=True, blank=True, default="")
    start = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=False)
    #varighet2 = models.DurationField(null=True, blank=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    song = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return "section"
        # return "Section ({}) in course: {}".format(self.getNr(), self.getCourse())
        #return "{} - {}...".format(self.course.title[0:40], self.text[:40])
        #return "{} - ({}) {}...".format(self.course.title[0:40], self.nr, self.text[:40])

    def getCourse(self):
        return self.course or None

    def getNr(self):
        return self.nr or None

    def getStart(self):
        return self.start.strftime("%H:%M")

    def getSong(self):
        return self.song or None
