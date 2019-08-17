# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from videos.models import *
import json
from halo import *
# End: imports -----------------------------------------------------------------

tags = [
    'Akro',
    'Armkrok',
    'Twist',
    'Swivel',
    'Gåtur',
    'HD',
    'Dip',
    'Hopp',
    'Flørt',
    'Teknikk',
    'Kombo',
    'Basic',
    'Speilvendt',
    'Gm2J',
    'Jm2G',
    'Høyrehåndsdans',
    'Venstrehåndsdans',
    'Gåswing',
    'Linje',
    'Hammerlock',
    'Spaghetti',
    'Styling',
    'Spinn',
    'Vrengtak',
    'Troll',
    'Break',
]

# Prep tags:
# 1. Remove duplicates
# 2. Make iterable
# 3. Make tags lowercase
tags = set(tags)
tags = list(tags)
tags = [tag.lower() for tag in tags]

class Command(BaseCommand):

    def delete_tags(self):
        VideoTag.objects.all().delete()

    def create_tags(self):
        global tags
        spinner = Halo("Creating video tags")
        spinner.start()

        for tag in tags:
            VideoTag.objects.create(navn=tag)

        spinner.succeed()

    def handle(self, *args, **options):
        self.delete_tags()
        self.create_tags()
        # End of handle
