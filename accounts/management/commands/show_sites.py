# imports
from halo import Halo
from django.utils import timezone
from django.core import management
from django.core.management.base import BaseCommand

from django.contrib.sites import models as site_models
from allauth.socialaccount import models as socialaccount_models
from allauth.socialaccount import app_settings, providers

# End: imports -----------------------------------------------------------------

class Command(BaseCommand):

    def show_sites(self):
        print("Showing existing sites")
        for s in site_models.Site.objects.all():
            print(f"{s.domain} with id: {s.id}")

    def handle(self, *args, **options):
        self.show_sites()
        # End of handle
