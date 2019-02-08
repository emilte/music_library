# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def txt_to_db(self):

        name = input("Name of textfile: ")
        if not name.endswith(".txt"):
            name += ".txt"

        songs = Song.objects.all().delete()

        with open('songs/static/songs/' + name, mode="r", encoding="UTF-8") as file:
            lines = file.readlines()

            for line in lines:
                line = json.loads(line)
                song = Song.objects.create(
                    title = line['title'],
                    artist = line['artist'],
                    bpm = line['bpm'],
                    spotify = line['spotify'],
                    URI = line['URI'],
                )

    def handle(self, *args, **options):
        self.txt_to_db()

        # End of handle
