# Generated by Django 2.2.9 on 2020-01-03 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0002_auto_20200103_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='path',
            field=models.CharField(help_text='URL som brukes i adressefeltet', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, unique=True)),
                ('last_edited', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator_folderset', to=settings.AUTH_USER_MODEL)),
                ('last_editor', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='editor_folderset', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='wiki.Folder'),
        ),
    ]