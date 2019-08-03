# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from videos.models import *
import json
# End: imports -----------------------------------------------------------------

yt_links = [
    "https://www.youtube.com/watch?v=QSGo3cRH2lU&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=2&t=0s",
    "https://www.youtube.com/watch?v=W8oGghNFuFk&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=4&t=0s",
    "https://www.youtube.com/watch?v=soBV5RboKFs&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=3&t=136s",
    "https://www.youtube.com/watch?v=-P4oD0QMpU8&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=117&t=0s",
    "https://www.youtube.com/watch?v=w5NduI8qE74&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=122&t=0s",
    "https://www.youtube.com/watch?v=H-3mP2wp3pc&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=140&t=0s",
    "https://www.youtube.com/watch?v=0ENRZ6hyC98&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=147&t=0s",
    "https://www.youtube.com/watch?v=NcrpLLzGcSE&list=PLBeE1xs-uSuixzJVm0MHRP-CSrm_UU6lT&index=131&t=0s",
    "https://youtu.be/G-5MZQw8oA8?t=5",
]

# Remove duplicates and change back to list
yt_links = set(yt_links)
yt_links = list(yt_links)

class Command(BaseCommand):

    def delete_videos(self):
        Video.objects.all().delete()

    def create_videos(self):
        global yt_links

        for x in range(0, len(yt_links) ):
            video = Video.objects.create(
                navn = "Video" + str(x),
                youtube = yt_links[x],
                beskrivelse = "Swing",
                fokuspunkt = "Fokus",
            )
            video.embed()



    def handle(self, *args, **options):
        self.delete_videos()
        self.create_videos()
        print("Done")
        # End of handle
