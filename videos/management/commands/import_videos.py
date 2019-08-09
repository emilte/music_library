# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from videos.models import *
import json
import os
# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def txt_to_db(self):
        path = 'videos/static/videos/'

        file_options = [file for file in os.listdir(path) if file.endswith(".txt")]

        print("Existing files in " + path)
        for i in range(len(file_options)):
            print("{}: {}".format(i+1, file_options[i]))

        option = int(input("\nChoose option: ")) - 1
        file = file_options[option]

        videos = Video.objects.all().delete()


        with open(path + file, mode="r", encoding="UTF-8") as file:
            lines = file.readlines()

            for line in lines:
                try:
                    line = json.loads(line)
                    tags = line['tags']
                    video = Video.objects.create(
                        navn = line["navn"],
                        youtube = line["youtube"],
                        embedded = line["embedded"],
                        fokuspunkt = line["fokuspunkt"],
                        beskrivelse = line["beskrivelse"],
                        vanskelighetsgrad = line["vanskelighetsgrad"],
                    )

                    for name in line['tags']:
                        videoTag, created = VideoTag.objects.get_or_create(name=name)
                        video.tags.add(videoTag)
                except Exception as e:
                    print("Error: {}".format(e))

    def handle(self, *args, **options):
        self.txt_to_db()
        print("Done")
        # End of handle
