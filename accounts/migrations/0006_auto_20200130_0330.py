# Generated by Django 2.2.9 on 2020-01-30 02:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('accounts', '0005_settings_scrollbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instructor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]