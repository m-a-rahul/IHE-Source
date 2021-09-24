from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializerWithToken
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from decouple import config
from django.contrib.auth.models import User
from .serializers import UserSerializer
import random
import string


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # User Id generation
        uid_list = []
        for user in User.objects.all():
            uid_list.append(user.username[3:])
        uid_index1 = ''.join(random.choice(string.digits) for i in range(2))
        uid_index2 = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
        uid_index3 = ''.join(random.choice(string.digits) for i in range(3))
        uid = uid_index1 + uid_index2 + uid_index3

        while uid in uid_list:
            uid_index1 = ''.join(random.choice(string.digits) for i in range(2))
            uid_index2 = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
            uid_index3 = ''.join(random.choice(string.digits) for i in range(3))
            uid = uid_index1 + uid_index2 + uid_index3

        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['username'] += uid
        request.data._mutable = _mutable

        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': config('FRONTEND_URL')+"/reset_password/?auth_token={}".format(reset_password_token.key)
    }

    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

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
