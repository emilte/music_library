# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from halo import Halo
from django.core import management
from accounts.models import *
from songs.models import *
# End: imports -----------------------------------------------------------------

# Settings:


class Command(BaseCommand):

    def create_themes(self):
        spinner = Halo("Creating themes")
        spinner.start()
        Theme.objects.create(
            background_color = "red",
            link_color = "blue",
            link_hover_color = "yellow",
        )
        spinner.succeed()

    def handle(self, *args, **options):
        self.create_themes()
        # End of handle
