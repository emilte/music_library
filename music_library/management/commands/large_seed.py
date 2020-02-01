# imports
import random
from halo import Halo
from faker import Faker
from django_seed import Seed

from django.utils import timezone
from django.core import management
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wiki import models as wiki_models
from songs import models as song_models
from videos import models as video_models
from events import models as event_models
from courses import models as course_models
from accounts import models as account_models

# End: imports -----------------------------------------------------------------

# OBS: seed() on instance was depricated for Faker module.
# Manually edited django-seed module __init__.py on line 35 from seed to seed_instance

# Settings:
User = get_user_model()

class Command(BaseCommand):

    def i(self, x, y):
        return random.randint(x, y)

    def fake_rgba(self, x=0, y=255):
        r, g, b, a = self.i(x,y), self.i(x,y), self.i(x,y), random.choice([0.6, 0.7, 0.8, 0.9, 1])
        return f"rgba({r},{g},{b},{a})"

    def f(self):
        seeder = Seed.seeder()

        ### seeder.faker.seed_instance(1234)

        seeder.add_entity(User, 100, {

        })
        seeder.add_entity(account_models.Theme, 500, {
            'user': lambda x: None,
            'name': lambda x: seeder.faker.safe_color_name(),
            'background_color': lambda x: self.fake_rgba(),
            'text_color': lambda x: seeder.faker.safe_color_name(),
            'link_color': lambda x: seeder.faker.safe_color_name(),
            'link_hover_color': lambda x: seeder.faker.safe_color_name(),
        })
        seeder.add_entity(video_models.Video, 300, {

        })
        seeder.add_entity(wiki_models.Folder, 50, {
            'title': lambda x: f"{seeder.faker.word()}-{random.randint(0, 10000)}",
            'root_folder': lambda x: None,
            'perm': lambda x: None,
        })
        seeder.add_entity(wiki_models.Page, 200, {
            'title': lambda x: f"{seeder.faker.word()}-{random.randint(0, 10000)}",
            'path': lambda x: seeder.faker.word() + f"{random.randint(0, 10000)}",
            'content': lambda x: seeder.faker.text(max_nb_chars=9000),

        })
        seeder.add_entity(song_models.Tag, 20, {
            'title': lambda x: f"{seeder.faker.word()}-{random.randint(0, 10000)}",
            'context': lambda x: None,
        })
        seeder.add_entity(song_models.Song, 1000, {
            'artist': lambda x: seeder.faker.word(),
            'title': lambda x: seeder.faker.sentence(nb_words=2),
            'bpm': lambda x: random.randint(60, 80),

        })
        seeder.add_entity(course_models.Course, 1000, {
            'title': lambda x: seeder.faker.sentence(nb_words=2),
            'comments': lambda x: seeder.faker.sentence(nb_words=4),
            'date': lambda x: seeder.faker.date_this_year(after_today=True),
            'day': lambda x: random.randint(1, 3),
            'bulk': lambda x: random.randint(1, 10),
            'comments': lambda x: seeder.faker.paragraphs(nb=2),

        })
        seeder.add_entity(course_models.Section, 6000, {
            'title': lambda x: seeder.faker.sentence(nb_words=2),
            'description': lambda x: seeder.faker.sentence(nb_words=50),
            'duration': lambda x: random.choice([5, 7.5, 7.5, 7.5, 10, 12, 15]),
        })
        seeder.add_entity(event_models.Event, 100, {
            'title': lambda x: seeder.faker.sentence(nb_words=2),
            'description': lambda x: seeder.faker.sentence(nb_words=50),
            'place': lambda x: seeder.faker.sentence(nb_words=3),
        })

        seeder.execute()



    def handle(self, *args, **options):
        self.f()
        # End of handle
