# imports
from slugify import slugify

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models

User = get_user_model()

# End: imports -----------------------------------------------------------------

class Folder(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100, unique=True, verbose_name="Tittel")
    root_folder = models.ForeignKey('wiki.Folder', on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="Hovedmappe")
    private = models.BooleanField(default=True, blank=True, verbose_name="Privat mappe")

    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="editor_folderset", verbose_name="Sist redigert av")
    last_edited = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Sist redigert")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="creator_folderset", verbose_name="Opprettet av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")

    perm = models.ForeignKey(auth_models.Permission, on_delete=models.SET_NULL, null=True, blank=True, related_name="folderset", verbose_name="Rettighet")

    class Meta:
        ordering = ['title']
        verbose_name = "Mappe"
        verbose_name_plural = "Mapper"

    def __str__(self):
        return self.title

    def root_path(self, path=[]):
        path.append(self)
        if self.root_folder:
            return self.root_folder.root_path(path)
        return path

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        return super(type(self), self).save(*args, **kwargs)



class Page(models.Model):
    title = models.CharField(null=True, blank=False, max_length=100, unique=True, verbose_name="Tittel")
    path = models.CharField(null=False, blank=False, unique=True, max_length=100, help_text="URL som brukes i adressefeltet")
    content = models.TextField(null=True, blank=True, verbose_name="Innhold")

    private = models.BooleanField(default=True, blank=True, verbose_name="Privat side")

    folder = models.ForeignKey('wiki.Folder', on_delete=models.SET_NULL, null=True, blank=False, related_name="pages", verbose_name="Mappe")

    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="editor_pageset", verbose_name="Sist redigert av")
    last_edited = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Sist redigert")

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="creator_pageset", verbose_name="Opprettet av")
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")

    class Meta:
        verbose_name = "Side"
        verbose_name_plural = "Sider"

    def root_path(self, path=[]):
        if self.folder:
            return self.folder.root_path(path)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.last_edited = timezone.now()

        root_path = self.root_path(path=[self])
        path = [ slugify(folder.title) for folder in root_path]
        path = "/".join(path)
        self.path = path

        return super(type(self), self).save(*args, **kwargs)
