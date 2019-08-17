# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from songs.models import *
import json
import os
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def txt_to_db(self):
        path = 'songs/static/songs/'

        file_options = [file for file in os.listdir(path) if file.endswith(".txt")]

        print("Existing files in " + path)
        for i in range(len(file_options)):
            print("{}: {}".format(i+1, file_options[i]))

        option = int(input("\nChoose option: "))
        file = file_options[option]

        songs = Song.objects.all().delete()


        with open(path + file, mode="r", encoding="UTF-8") as file:
            lines = file.readlines()

            for line in lines:
                try:
                    line = json.loads(line)
                    song = Song.objects.create(
                        tittel = line['tittel'],
                        artist = line['artist'],
                        bpm = line['bpm'],
                        spotify_URL = line['spotify_URL'],
                        spotify_URI = line['spotify_URI'],
                    )
                except Exception as e:
                    print("Error: {}".format(e))

    def handle(self, *args, **options):
        self.txt_to_db()
        print("Done")
        # End of handle
