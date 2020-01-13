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
        management.call_command('makemigrations')
        management.call_command('migrate')

        try:
            management.call_command('myseed')
        except Exception as e:
            print(e)


        # End of handle
