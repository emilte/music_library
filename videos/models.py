# imports
from django.db import models

# End: imports -----------------------------------------------------------------

# choises:
DIFFICULY_CHOISES = [
    (1, 'Lett'),
    (2, 'Middels'),
    (3, 'Vanskelig'),
    (3, 'Avansert')
]
# End: coises ------------------------------------------------------------------

class VideoTag(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    navn = models.CharField(max_length=150, null=True, blank=False)
    youtube = models.URLField(null=True, blank=False)
    embedded = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField('videos.VideoTag')
    beskrivelse = models.TextField(max_length=150, null=True, blank=False)
    fokuspunkt = models.TextField(max_length=150, null=True, blank=False)
    vanskelighetsgrad = models.IntegerField(choices=DIFFICULY_CHOISES, default=1)

    #tags = models.ManyToManyField(Tag, blank=True)

    def embed(self):
        video_id = "no id"
        if self.youtube == None:
            return

        if "youtu.be" in self.youtube:
            video_id = self.youtube.split("/")[-1].split("?")[0]

        if "watch" in self.youtube:
            video_id = self.youtube.split("?")[1].split("&")[0][2:]

        self.embedded = "https://www.youtube.com/embed/" + video_id + "?iv_load_policy=3" + "?rel=0"
        self.save()


    def __str__(self):
        return "{}".format(self.navn)
