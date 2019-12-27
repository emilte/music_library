# Generated by Django 2.2.5 on 2019-12-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='tittel',
        ),
        migrations.RemoveField(
            model_name='songtag',
            name='navn',
        ),
        migrations.AddField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='songtag',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='spotify_URI',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='spotify_URL',
            field=models.URLField(null=True),
        ),
    ]
