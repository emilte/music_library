# Generated by Django 2.0.8 on 2019-08-18 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20190818_0123'),
        ('courses', '0005_auto_20190818_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(to='videos.VideoTag'),
        ),
    ]
