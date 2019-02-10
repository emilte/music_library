# Generated by Django 2.0.8 on 2019-02-09 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_section_nr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='female_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='female_instructors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='int_duration',
            field=models.DurationField(default=90, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='male_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='male_instructors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='target_group',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='duration',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='nr',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='start',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
