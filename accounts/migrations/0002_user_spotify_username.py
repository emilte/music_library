# Generated by Django 2.0.8 on 2019-08-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='spotify_username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]