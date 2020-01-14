# imports
from halo import Halo
from django_seed import Seed
from faker import Faker
import random

from django.utils import timezone
from django.core import management
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wiki import models as wiki_models
from songs import models as song_models
from videos import models as video_models
from courses import models as course_models
from accounts import models as account_models

# End: imports -----------------------------------------------------------------

# OBS: seed() on instance was depricated for Faker module.
# Manually edited django-seed module __init__.py on line 35 from seed to seed_instance

# Settings:
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        management.call_command('flush', interactive=False)
        management.call_command('create_admin')
        management.call_command('create_site')
        management.call_command('myseed')
        # End of handle
