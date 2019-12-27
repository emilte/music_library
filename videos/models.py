# imports
from django.db import models

# End: imports -----------------------------------------------------------------

# choises:
DIFFICULY_CHOISES = [
    (1, 'Lett'),
    (2, 'Middels'),
    (3, 'Vanskelig'),
]
# End: coises ------------------------------------------------------------------

class VideoTag(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=150, null=True, blank=False)
    youtube_URL = models.URLField(null=True, blank=False)
    embedded = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField('videos.VideoTag')
    description = models.TextField(null=True, blank=True)
    focus = models.TextField(null=True, blank=True)
    difficulty = models.IntegerField(choices=DIFFICULY_CHOISES, default=1)

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
