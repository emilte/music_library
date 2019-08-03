# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from videos.models import *
import json
import datetime
import os
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def db_to_txt(self):
        videos = Video.objects.all()
        path = "videos/static/videos/"

        name = input("Name the exported file: ")
        name += "_lines-{}".format(len(videos))
        name += "_date-{:%d-%m-%y}".format(datetime.datetime.now())
        if not name.endswith(".txt"):
            name += ".txt"

        data = ""
        for video in videos:
            tags = video.tags.values_list('name')
            tags = [t[0] for t in tags]
            video = video.__dict__
            video = {'navn': video['navn'], 'youtube': video['youtube'], 'embedded': video['embedded'], 'tags': tags, 'beskrivelse': video['beskrivelse'], 'fokuspunkt': video['fokuspunkt'], "vanskelighetsgrad": video["vanskelighetsgrad"] }
            data += json.dumps(video, ensure_ascii=False) + "\n"

        with open(path + name, mode="w+", encoding="UTF-8") as file:
            file.write(data)


    def handle(self, *args, **options):
        self.db_to_txt()
        print("Done")
        # End of handle
