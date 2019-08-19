# Generated by Django 2.0.8 on 2019-08-17 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='date',
            new_name='dato',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='female_instructor',
            new_name='følger',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='male_instructor',
            new_name='fører',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='place',
            new_name='hvor',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='end',
            new_name='slutt',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='title',
            new_name='tittel',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='duration',
            new_name='varighet',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='text',
            new_name='beskrivelse',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='course',
            new_name='kurs',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='song',
            new_name='sang',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='title',
            new_name='tittel',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='duration',
            new_name='varighet',
        ),
        migrations.RemoveField(
            model_name='course',
            name='external',
        ),
        migrations.RemoveField(
            model_name='course',
            name='target_group',
        ),
    ]