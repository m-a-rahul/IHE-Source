from django.contrib.auth.models import Group
from django.contrib import admin
from django_rest_passwordreset.models import ResetPasswordToken
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)
admin.site.unregister(Site)
admin.site.unregister(TokenProxy)
