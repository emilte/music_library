# imports
from django.db import models
from django.conf import settings
from django.utils import timezone

# End: imports -----------------------------------------------------------------
semesters = ['------']
v = [f"V{year}" for year in range(2000, 2100)]
h = [f"H{year}" for year in range(2000, 2100)]
semesters.extend(v)
semesters.extend(h)
SEMESTER_CHOICES = [(i, semesters[i]) for i in range(len(semesters))]

class Course(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, verbose_name="Tittel")
    place = models.CharField(max_length=140, null=True, blank=True, verbose_name="Sted")
    date = models.DateField(null=True, blank=True, verbose_name="Dato")
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True, verbose_name="Slutt")
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_courses", verbose_name="Instruktør (lead)")
    follow = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="follow_courses", verbose_name="Instruktør (follow)")
    comments = models.TextField(null=True, blank=True, verbose_name="Kommentarer")
    tags = models.ManyToManyField('songs.Tag', blank=True)

    last_edited = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Sist redigert")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="last_edited_courses", verbose_name="Sist redigert av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")

    # NOTE: Under development
    # instructors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    instructors = models.ManyToManyField('accounts.Instructor', blank=True)
    bulk = models.PositiveIntegerField(null=True, blank=True, verbose_name="Bolk")
    day = models.PositiveIntegerField(null=True, blank=True, verbose_name="Dag")

    semester_choice = models.IntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)
    semester_char = models.CharField(max_length=5, null=True, blank=True)

    external = models.BooleanField(default=False, verbose_name="Eksternkurs")


    class Meta:
        ordering = ['date', 'bulk', 'day', 'title']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurs"

    def __str__(self):
        return "{} ({})".format(self.getTitle(), self.getDate())

    def getSemester(self):
        semesters = ['Vår', 'Høst']
        if self.date:
            i = (self.date.month-1) // 6 # Calculates first (0) or second (1) half of year
            return f"{semesters[i]} {self.date.year}"
        else:
            return None

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

        if self.date:
            semesters = ['V', 'H']
            i = (self.date.month-1) // 6 # Calculates first (0) or second (1) half of year
            self.semester_char = f"{semesters[i]}{self.date.year}"


        return super(type(self), self).save(*args, **kwargs)



class Section(models.Model):
    title = models.CharField(max_length=140, null=True, blank=False, verbose_name="Tittel")
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name="sections", verbose_name="Kurs")
    description = models.TextField(null=True, blank=True, verbose_name="Beskrivelse")
    start = models.TimeField(null=True, blank=True)
    # duration = models.FloatField(null=True, blank=False, verbose_name="Varighet")
    duration = models.FloatField(default=7.5, null=True, blank=False, verbose_name="Varighet")
    song = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections", verbose_name="Sang")
    song2 = models.ForeignKey('songs.Song', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections_song2", verbose_name="Sang")
    video = models.ForeignKey('videos.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name="sections", verbose_name="Video")
    nr = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['nr']
        verbose_name = "Kurs-seksjon"
        verbose_name_plural = "Kurs-seksjoner"

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
