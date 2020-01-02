# Generated by Django 2.2.9 on 2020-01-02 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_instructor'),
        ('courses', '0007_auto_20200102_1322'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['date', 'title']},
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(blank=True, to='accounts.Instructor'),
        ),
    ]
