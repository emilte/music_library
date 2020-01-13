# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from halo import Halo
from django.core import management
from accounts.models import *
from songs.models import *
# End: imports -----------------------------------------------------------------

# Settings:
USER_PW = "Django123"


class Command(BaseCommand):

    def handle(self, *args, **options):
        management.call_command('migrate')
        management.call_command('import_videos')

        # End of handle
