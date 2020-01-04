# imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# End: imports -----------------------------------------------------------------

class Folder(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100, unique=True)

    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="editor_folderset")
    last_edited = models.DateTimeField(null=True, blank=True, editable=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="creator_folderset")
    created = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    def getPath(self):
        if self.path.endswith('/'):
            return self.path
        else:
            return self.path + '/'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        return super(type(self), self).save(*args, **kwargs)



class Page(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100, unique=True)
    path = models.CharField(null=False, blank=False, unique=True, max_length=100, help_text="URL som brukes i adressefeltet")
    content = models.TextField(null=True, blank=True)

    private = models.BooleanField(default=True, blank=True)

    folder = models.ForeignKey('wiki.Folder', on_delete=models.SET_NULL, null=True, blank=True, related_name="pages")

    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="editor_pageset")
    last_edited = models.DateTimeField(null=True, blank=True, editable=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="creator_pageset")
    created = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        return super(type(self), self).save(*args, **kwargs)
