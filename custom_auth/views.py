import random
import string
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest_passwordreset.signals import reset_password_token_created
from decouple import config
from custom_auth.serializers import UserSerializer, UserSerializerWithToken


def username_generator():
    uid_list = []
    for user in User.objects.all():
        uid_list.append(user.username[3:])

    uid = ''.join(random.choice(string.digits) for i in range(2)) + ''.join(
        random.choice(string.ascii_uppercase) for i in range(2)) + ''.join(
        random.choice(string.digits) for i in range(3))
    while uid in uid_list:
        uid = ''.join(random.choice(string.digits) for i in range(2)) + ''.join(
            random.choice(string.ascii_uppercase) for i in range(2)) + ''.join(
            random.choice(string.digits) for i in range(3))
    return uid


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    @csrf_exempt
    def post(request):
        request.data['username'] += username_generator()
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(APIView):
    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'last_name': reset_password_token.user.last_name,
        'reset_password_url': config('FRONTEND_URL') + "/reset_password/?auth_token={}".format(reset_password_token.key)
    }

    email_html_message = render_to_string('passwordresetemail/user_reset_password.html', context)
    email_plaintext_message = render_to_string('passwordresetemail/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset",
        # message:
        email_plaintext_message,
        # from:
        "ihe@dailyfishmart.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
