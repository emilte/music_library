# imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from accounts import models as account_models

User = get_user_model()

# End: imports -----------------------------------------------------------------

@receiver(post_save, sender=User)
def create_settings(sender, instance, created, **kwargs):
    if created:
        account_models.Settings.objects.create(user=instance)
        print("== (users.signals.py) <Settings> created for <{}> ==".format(instance))
