from django.contrib.auth.models import User
from admin_honeypot.signals import honeypot
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False


@receiver(honeypot)
def adminhoneypot_signal(sender, instance, **kwargs):
    context = {'object': instance, }
    subject = 'Alert! Invalid login attempt at IHE'
    message = render_to_string('honeypotsignalemail/notification.txt', context)
    to = [item[1] for item in settings.ADMINS]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
