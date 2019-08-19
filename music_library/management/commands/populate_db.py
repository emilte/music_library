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
    args = '<foo bar ...>'
    help = """No options or args needed.
    Run this command to fill the database with dummydata.
    OBS: This will drop the database, makemigrations and migrate.
    """
    def reset_db(self):
        management.call_command('reset_db')
        print()

    def make_migrations(self):
        print("Making migrations")
        management.call_command('makemigrations')
        print()

    def migrate(self):
        print("Applying migrations")
        management.call_command('migrate')
        print()

    def handle(self, *args, **options):
        self.reset_db()
        self.make_migrations()
        self.migrate()
        management.call_command('create_users')
        management.call_command('create_video_tags')
        management.call_command('create_song_tags')
        #management.call_command('create_course_tags')
        management.call_command('import_songs')
        management.call_command('import_videos')

        print("  ==  Dummydata inserted, REMEMBER to runserver  ==  ")
        # End of handle
