# Generated by Django 2.2.9 on 2020-01-20 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_external'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['date', 'bulk', 'day', 'title'], 'verbose_name': 'Kurs', 'verbose_name_plural': 'Kurs'},
        ),
    ]
