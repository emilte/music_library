# imports
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from users import models as user_models

User = get_user_model()

# End: imports -----------------------------------------------------------------

@receiver(post_save, sender=User)
def create_settings(sender, instance, created, **kwargs):
    if created:
        user_models.Settings.objects.create(user=instance)
        print("== (users.signals.py) <Settings> created for <{}> ==".format(instance))
