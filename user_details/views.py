import phonenumbers
import pycountry
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer, HospitalSerializer, HospitalStaffSerializer
from custom_auth.serializers import UserSerializer, UserSerializerWithoutToken
from django.contrib.auth.models import User
from user_details.models import Hospital, HospitalStaff
import random
import string
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def generate_random_password():
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lowercase_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']

    uppercase_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']

    symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
               '*', '(', ')', '<']
    characters = digits + uppercase_characters + lowercase_characters + symbols
    password = [random.choice(lowercase_characters)]
    for i in range(10):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


class HospitalAccounts(APIView):

    @staticmethod
    @csrf_exempt
    def post(request):
        response_list = []
        for i in request.data:
            response = {}
            uid_list = []
            for user in User.objects.all():
                uid_list.append(user.username[3:])

            uid = ''.join(random.choice(string.digits) for i in range(2)) + ''.join(random.choice(string.ascii_uppercase) for i in range(2)) + ''.join(random.choice(string.digits) for i in range(3))
            while uid in uid_list:
                uid = ''.join(random.choice(string.digits) for i in range(2)) + ''.join(random.choice(string.ascii_uppercase) for i in range(2)) + ''.join(random.choice(string.digits) for i in range(3))
            country_code = pycountry.countries.search_fuzzy('ind')[0].alpha_2
            user_role_code = i["role"][0].capitalize()
            username = country_code+user_role_code+uid
            password = generate_random_password()
            serializer = UserSerializerWithoutToken(data={'username': username,
                                                          'last_name': i['name'],
                                                          'email': i['email'],
                                                          'password': password})
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                user_id = user.id
                hos_code = Hospital.objects.get(user=request.user)
                phone_prefix = '+' + str(phonenumbers.country_code_for_region(country_code))
                contact = phone_prefix + i['contact']
                staff_serializer = HospitalStaffSerializer(data={'user': user_id,
                                                                 'hos_code': hos_code,
                                                                 'role': user_role_code,
                                                                 'degree': i["degree"],
                                                                 'designation': i["designation"],
                                                                 'department': i['department'],
                                                                 'contact': contact})
                if staff_serializer.is_valid():
                    staff_serializer.save()
                    context = {
                        'password': password,
                        'username': username,
                        'email': i['email'],
                        'last_name': i['name'],
                        'frontend_url': config('FRONTEND_URL')
                    }

                    email_html_message = render_to_string('staffwelcomeemail/staff_welcome.html', context)
                    email_plaintext_message = render_to_string('staffwelcomeemail/staff_welcome.txt', context)

                    msg = EmailMultiAlternatives(
                        # title:
                        "Welcome to IHE",
                        # message:
                        email_plaintext_message,
                        # from:
                        "ihe@dailyfishmart.com",
                        # to:
                        [i['email']]
                    )
                    msg.attach_alternative(email_html_message, "text/html")
                    msg.send()
                    response["status"] = "success"
                    response["user"] = serializer.data
                    response["details"] = staff_serializer.data
                else:
                    response["status"] = "failure"
                    response["message"] = staff_serializer.errors
                    User.objects.get(username=username).delete()
            else:
                response["status"] = "failure"
                try:
                    HospitalStaff.objects.get(hos_code=request.user.id, user=User.objects.get(email=i["email"]).id)
                    response["message"] = {'user': ['There is an user with this email already associated with this hospital']}
                except:
                    response["message"] = serializer.errors

            response_list.append(response)

        return Response(response_list, status=status.HTTP_200_OK)


class GetUserDetails(APIView):
    @staticmethod
    @csrf_exempt
    def get(request):
        try:
            if request.user.username[2] == "P":
                serializer = PatientSerializer(request.user.patient, many=False)
            elif request.user.username[2] == "H":
                serializer = HospitalSerializer(request.user.hospital, many=False)
            else:
                serializer = HospitalStaffSerializer(request.user.hospital_staff, many=False)
            return Response(serializer.data)
        except:
            return Response('RelatedObjectDoesNotExist', status=status.HTTP_200_OK)


class CreateUpdateUserDetails(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        request.data['user'] = request.user.id
        if request.data['update']:
            try:
                if request.user.username[2] == "P":
                    serializer = PatientSerializer(instance=request.user.patient, data=request.data)

                elif request.user.username[2] == "H":
                    serializer = HospitalSerializer(instance=request.user.hospital, data=request.data)
                else:
                    request.data['hos_code'] = request.user.hospital_staff.hos_code.user.id
                    serializer = HospitalStaffSerializer(instance=request.user.hospital_staff, data=request.data)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.username[2] == "P":
                serializer = PatientSerializer(data=request.data)
            elif request.user.username[2] == "H":
                serializer = HospitalSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

