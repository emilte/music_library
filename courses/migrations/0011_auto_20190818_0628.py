# Generated by Django 2.0.8 on 2019-08-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20190818_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slutt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='varighet',
            field=models.IntegerField(null=True),
        ),
    ]
