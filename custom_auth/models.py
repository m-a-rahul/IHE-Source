from django.contrib.auth.models import User

User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False
