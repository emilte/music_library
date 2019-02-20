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

class Video(models.Model):
    navn = models.CharField(max_length=150, null=True, blank=False)
    youtube = models.URLField(null=True, blank=False)
    beskrivelse = models.TextField(max_length=150, null=True, blank=False)
    fokuspunkt = models.TextField(max_length=150, null=True, blank=False)
    tags = models.ManyToManyField('songs.Tag')
    vanskelighetsgrad = models.IntegerField(choices=DIFFICULY_CHOISES, default=1)

    #tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return "{}".format(self.youtube)
