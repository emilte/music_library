# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
import datetime
import os
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def db_to_txt(self):
        songs = Song.objects.all()

        name = input("Name the exported file: ")
        name += "_lines-{}".format(len(songs))
        name += "_date-{:%d-%m-%y}".format(datetime.datetime.now())
        if not name.endswith(".txt"):
            name += ".txt"

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
        print("Done")
        # End of handle
