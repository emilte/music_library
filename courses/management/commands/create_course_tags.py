# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
import datetime
import os
from halo import *
# End: imports -----------------------------------------------------------------

tags = [
    'lindy',
]

tags = set(tags)
tags = list(tags)
tags = [tag.lower() for tag in tags]

class Command(BaseCommand):

    def delete_tags(self):
        SongTag.objects.all().delete()

    def create_tags(self):
        global tags
        spinner = Halo("Creating tags")
        spinner.start()
        for navn in tags:
            SongTag.objects.create(navn=navn)

        spinner.succeed()

    def handle(self, *args, **options):
        self.delete_tags()
        self.create_tags()
        # End of handle
