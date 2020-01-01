# imports
from django.db import models
from django.utils import timezone
from django.conf import settings

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    lead = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="male_courses")
    follow = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="female_courses")
    date = models.DateField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True, default="")
    place = models.CharField(max_length=140, null=True, blank=True, default="")
    # tags = models.ManyToManyField('videos.VideoTag')
    tags = models.ManyToManyField('songs.Tag')
    last_edited = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="last_edited_courses")

    def __str__(self):
        return "{} ({})".format(self.getTitle(), self.getDate())

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
        return [title[0] for title in self.tags.all().values_list('title') ]



class Section(models.Model):
    nr = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    description = models.TextField(null=True, blank=True, default="")
    start = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=False)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    song = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return "Section ({}) in course: {}".format(self.getNr(), self.getCourse())
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
