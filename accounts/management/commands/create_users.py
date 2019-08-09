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

        spinner = Halo("Creating superuser")
        spinner.start()
        email = "emil.telstad@live.no"
        User.objects.create_superuser(
            email=email,
            password=USER_PW,
            first_name="Emil",
            last_name="Telstad",
            phone_number="41325358"
        )
        spinner.succeed("Creating superuser. email: {}, password: {}".format(email, USER_PW))
        # End: createsu

    def create_staff(self):
        spinner = Halo("Creating a staff user")
        spinner.start()
        email = "staff@staff.com"
        User.objects.create_user(
            email=email,
            password=USER_PW,
            first_name="Staff",
            last_name="Staffski",
            staff=True,
            phone_number="87654321"
        )
        spinner.succeed("Creating staff user. email: {}, password: {}".format(email, USER_PW))


    def handle(self, *args, **options):
        self.createsu()
        self.create_staff()
        # End of handle