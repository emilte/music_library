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

    def createsu(self):
        spinner = Halo("Creating superuser")
        spinner.start()
        email = "admin@admin.com"
        User.objects.create_superuser(
            email=email,
            password=USER_PW,
            first_name="Admin",
            last_name="Adminsen",
            phone_number="12345678"
        )
        spinner.succeed("Creating superuser. email: {}, password: {}".format(email, USER_PW))



    def handle(self, *args, **options):
        try:
            self.createsu()
        except Exception as e:
            print(e)
        # End of handle
