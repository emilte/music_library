# imports
import smtplib
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from accounts import models as account_models
from allauth.account import signals as allauth_signals

User = get_user_model()
from email.message import EmailMessage


# End: imports -----------------------------------------------------------------

@receiver(allauth_signals.user_signed_up)
def create_settings(request, user, **kwargs):
    account_models.Settings.objects.get_or_create(user=user)
    print("== (users.signals.py) <Settings> created for <{}> ==".format(user))



@receiver(allauth_signals.user_signed_up)
def send_mail(request, user, **kwargs):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')

        sent_from = 'script97tester@gmail.com'
        password = "Django!23"

        server.login(sent_from, password)

        to = ['emil.telstad@gmail.com']

        email = EmailMessage()
        email.set_content(f"{instance.email} har opprettet en bruker.")

        email['Subject'] = 'Varsel: Ny bruker'
        email['From'] = sent_from
        email['To'] = to

        server.send_message(email)

    except Exception as e:
        print(e)
