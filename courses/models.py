# imports
from django.db import models
from django.conf import settings
from django.utils import timezone

# End: imports -----------------------------------------------------------------

class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False)
    place = models.CharField(max_length=140, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_courses")
    follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="follow_courses")
    comments = models.TextField(null=True, blank=True, default="")
    tags = models.ManyToManyField('songs.Tag', blank=True)

    last_edited = models.DateTimeField(null=True, blank=True, editable=False)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="last_edited_courses")
    created = models.DateTimeField(null=True, blank=True, editable=False)

    # NOTE: Under development
    # instructors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    instructors = models.ManyToManyField('accounts.Instructor', blank=True)
    bulk = models.PositiveIntegerField(null=True, blank=True)
    day = models.PositiveIntegerField(null=True, blank=True)


    class Meta:
        ordering = ['date', 'title']

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        return super(type(self), self).save(*args, **kwargs)



class Section(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, default="")
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    description = models.TextField(null=True, blank=True, default="")
    start = models.TimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=False)
    song = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")
    video = models.ForeignKey('videos.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections")
    nr = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['nr']

    def __str__(self):
        return "Section ({}) in course: {}".format(self.getNr(), self.getCourse())

    def getCourse(self):
        return self.course or None

    def getNr(self):
        return self.nr or None

    def getStart(self):
        return self.start.strftime("%H:%M")

    def getSong(self):
        return self.song or None
