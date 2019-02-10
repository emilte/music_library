# imports
from django.db import models
from tinymce.models import HTMLField
# End: imports -----------------------------------------------------------------

class Section(models.Model):
    title = models.CharField(max_length=150)
    text = HTMLField()

    def __str__(self):
        return self.title
