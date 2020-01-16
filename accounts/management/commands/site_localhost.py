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

    def localhost(self):
        domain = "localhost:8000"
        site, created = site_models.Site.objects.get_or_create(name=domain, domain=domain)
        print(f"site created: {created}")
        print(f"Site: {site.domain} ({site.id})")

        try:
            from django.conf import settings

            socialapp, created = socialaccount_models.SocialApp.objects.get_or_create(
                provider="google",
                name='Google',
                client_id=settings.GOOGLE_CLIENT_ID,
                secret=settings.GOOGLE_CLIENT_SECRET,
            )
            print(f"socialapp created: {created}")
            socialapp.sites.add(site)
            socialapp.save()

            settings.SITE_ID = site.id

        except Exception as e:
            print(e)


    def handle(self, *args, **options):
        self.localhost()
        management.call_command('show_sites')
        # End of handle
