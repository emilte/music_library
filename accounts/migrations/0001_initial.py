# Generated by Django 2.2.9 on 2020-01-25 03:17

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=60, verbose_name='Fornavn')),
                ('last_name', models.CharField(max_length=150, verbose_name='Etternavn')),
                ('spotify_username', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=13, verbose_name='Mobilnummer')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Opprettet')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['email'],
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, null=True, verbose_name='Navn')),
                ('background_color', models.CharField(blank=True, help_text='CSS: blue, rgba(0,0,255, 0.5)', max_length=140, null=True, verbose_name='Bakgrunnsfarge')),
                ('text_color', models.CharField(help_text='CSS: blue, rgba(0,0,255, 0.5)', max_length=140, null=True, verbose_name='Tekst farge')),
                ('link_color', models.CharField(help_text='CSS: blue, rgba(0,0,255, 0.5)', max_length=140, null=True, verbose_name='Link farge')),
                ('link_hover_color', models.CharField(help_text='CSS: blue, rgba(0,0,255, 0.5)', max_length=140, null=True, verbose_name='Link hover farge')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Opprettet')),
                ('user', models.OneToOneField(blank=True, help_text='Dersom eier er satt, vil temaet være privat', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='themes', to=settings.AUTH_USER_MODEL, verbose_name='Eier')),
            ],
            options={
                'verbose_name': 'Tema',
                'verbose_name_plural': 'Temaer',
                'ordering': ['user', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SpotifyToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spotify_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background', models.CharField(blank=True, default=None, help_text='background-image-url', max_length=1000, null=True, verbose_name='Bakgrunnsfarge')),
                ('color', models.CharField(blank=True, default=None, help_text='color', max_length=1000, null=True, verbose_name='Tekstfarge')),
                ('footer', models.CharField(blank=True, default=None, help_text='background-color', max_length=1000, null=True, verbose_name='footer-color')),
                ('account_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_as_account', to='accounts.Theme', verbose_name='Bruker-tema')),
                ('course_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_as_course', to='accounts.Theme', verbose_name='Kurs-tema')),
                ('song_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_as_song', to='accounts.Theme', verbose_name='Musikk-tema')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL, verbose_name='Tilhører')),
                ('video_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_as_video', to='accounts.Theme', verbose_name='Turbibliotek-tema')),
                ('wiki_theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_as_wiki', to='accounts.Theme', verbose_name='Wiki-tema')),
            ],
            options={
                'verbose_name': 'Instilling',
                'verbose_name_plural': 'Instillinger',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, '------'), (1, 'lead'), (2, 'follow'), (3, 'hjelpeinstruktør'), (4, 'annet')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Instruktør',
                'verbose_name_plural': 'Instruktører',
                'ordering': ['type'],
            },
        ),
    ]
