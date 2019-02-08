# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def db_to_txt(self):

        name = input("Name of textfile: ")
        if not name.endswith(".txt"):
            name += ".txt"

        songs = Song.objects.all()
        data = ""

        for song in songs:
            tags = song.tags.values_list('name')
            tags = [t[0] for t in tags]
            song = song.__dict__
            song = {'title': song['title'], 'artist': song['artist'], 'bpm': song['bpm'], 'tags': tags, 'spotify': song['spotify'], 'URI': song['URI'] }
            data += json.dumps(song, ensure_ascii=False) + "\n"

        with open('songs/static/songs/' + name, mode="w+", encoding="UTF-8") as file:
            file.write(data)


    def handle(self, *args, **options):
        self.db_to_txt()

        # End of handle
