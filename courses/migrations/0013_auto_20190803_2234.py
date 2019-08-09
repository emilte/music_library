# Generated by Django 2.0.8 on 2019-08-03 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20190803_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='female_instructor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='female_instructors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='int_duration',
            field=models.DurationField(blank=True, default=90, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='male_instructor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='male_instructors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='target_group',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]
