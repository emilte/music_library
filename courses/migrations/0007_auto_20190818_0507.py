# Generated by Django 2.0.8 on 2019-08-18 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='dato',
            field=models.DateField(blank=True, null=True),
        ),
    ]