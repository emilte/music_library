# Generated by Django 2.2.9 on 2020-01-25 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_settings_background'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='footer',
            field=models.CharField(blank=True, default='inherit', help_text='background-color', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='navbar',
            field=models.CharField(blank=True, default='inherit', help_text='background-color', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='background',
            field=models.CharField(blank=True, default='inherit', help_text='background-image-url', max_length=1000, null=True),
        ),
    ]
