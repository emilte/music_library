# imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
# End: imports -----------------------------------------------------------------

# choises:
DIFFICULY_CHOISES = [
    (1, 'Lett'),
    (2, 'Middels'),
    (3, 'Vanskelig'),
]
# End: coises ------------------------------------------------------------------

class Video(models.Model):
    title = models.CharField(max_length=150, null=True, blank=False, verbose_name="Tittel")
    youtube_URL = models.URLField(null=True, blank=False)
    embedded = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField('songs.Tag')
    description = models.TextField(null=True, blank=True, verbose_name="Beskrivelse")
    focus = models.TextField(null=True, blank=True, verbose_name="Fokuspunkt")
    difficulty = models.IntegerField(choices=DIFFICULY_CHOISES, default=1, verbose_name="Vanskelighetsgrad")

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, verbose_name="Opprettet av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")

    def embed(self):
        video_id = "no id"
        if self.youtube_URL == None:
            return

        if "youtu.be" in self.youtube_URL:
            video_id = self.youtube_URL.split("/")[-1].split("?")[0]

        if "watch" in self.youtube_URL:
            video_id = self.youtube_URL.split("?")[1].split("&")[0][2:]

        self.embedded = "https://www.youtube.com/embed/" + video_id + "?iv_load_policy=3" + "?rel=0"
        self.save()


    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(type(self), self).save(*args, **kwargs)
