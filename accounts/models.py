# imports
import json

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# End: imports -----------------------------------------------------------------

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=60, null=False, blank=False, verbose_name="Fornavn")
    last_name = models.CharField(max_length=150, null=False, blank=False, verbose_name="Etternavn")
    spotify_username = models.CharField(max_length=150, null=True, blank=True) # Obsolete
    phone_number = models.CharField(max_length=13, blank=True, verbose_name="Mobilnummer")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, blank=True, editable=False, verbose_name="Opprettet")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['email']

    def __str__(self):
        return self.get_full_name() or self.email

    def check_group_func(name):
        def check_group(user):
            return user.groups.filter(name=name).exists()
        return check_group

    def getCourses(self):
        return self.lead_courses.all() | self.follow_courses.all()

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return None
        else:
            return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

class Theme(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="themes", verbose_name="Opprettet av")
    name = models.CharField(max_length=140, null=True, blank="False", verbose_name="Navn")

    background_color = models.CharField(max_length=140, verbose_name="Bakgrunnsfarge")
    link_color = models.CharField(max_length=140, verbose_name="Link farge")
    link_hover_color = models.CharField(max_length=140, verbose_name="Link hover farge")

    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Opprettet")

    class Meta:
        ordering = ['user', 'name']
        verbose_name = "Tema"
        verbose_name_plural = "Temaer"

    def __str__(self):
        if self.user:
            return "{} ({})".format(self.name, self.user.get_full_name())
        else:
            return "{} ({})".format(self.name, "Public")

    def as_css(self):
        css = """.user-theme {{
            background-color: {0};
        }}
        .user-theme-link {{
            color: {1};
        }}
        .user-theme-link:hover {{
            cursor: pointer;
            color: {2};
        }}
        """.format(self.background_color, self.link_color, self.link_hover_color)
        return css

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(type(self), self).save(*args, **kwargs)


class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="settings", verbose_name="Tilhører")

    account_theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="settings_as_account", verbose_name="Bruker tema")
    video_theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="settings_as_video", verbose_name="Turbibliotek tema")
    course_theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="settings_as_course", verbose_name="Kurs tema")
    song_theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="settings_as_song", verbose_name="Musikk tema")

    class Meta:
        verbose_name = "Instilling"
        verbose_name_plural = "Instillinger"

    def __str__(self):
        return "Instillinger for {}".format(self.user)

class Instructor(models.Model):
    TYPES = [
        (0, '------'),
        (1, 'lead'),
        (2, 'follow'),
        (3, 'hjelpeinstruktør'),
        (4, 'annet'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="instructor_set")
    type = models.IntegerField(choices=TYPES, default=0)

    class Meta:
        ordering = ['type']
        verbose_name = "Instruktør"
        verbose_name_plural = "Instruktører"

    def __str__(self):
        return f"{self.user} ({self.get_type_display()})"


class SpotifyToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="spotify_token")
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Spotify token for {}".format(self.user)

    def addInfo(self, data):
        self.info = json.dumps(data)
        self.save()
