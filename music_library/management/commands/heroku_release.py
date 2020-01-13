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
            import fileinput
            filename = "/app/.heroku/python/lib/python3.8/site-packages/django_seed/__init__.py"
            print("REPLACING")
            with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line)
                    origin = "cls.fakers[code].seed(random.randint(1, 10000))"
                    replacement = "cls.fakers[code].seed_instance(random.randint(1, 10000))"
                    print(line.replace(origin, replacement), end='')

            management.call_command('myseed')
        except Exception as e:
            print(e)


        # End of handle
