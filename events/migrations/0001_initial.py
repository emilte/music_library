# Generated by Django 2.2.9 on 2020-01-17 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('songs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140, null=True, verbose_name='Tittel')),
                ('place', models.CharField(blank=True, max_length=140, null=True, verbose_name='Sted')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Dato')),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='Slutt')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Beskrivelse')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Kommentarer')),
                ('last_edited', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Sist redigert')),
                ('created', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Opprettet')),
                ('creator', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Opprettet av')),
                ('last_editor', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_events', to=settings.AUTH_USER_MODEL, verbose_name='Sist redigert av')),
                ('tags', models.ManyToManyField(blank=True, to='songs.Tag')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['date', 'title'],
            },
        ),
    ]
