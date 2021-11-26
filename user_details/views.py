import phonenumbers
import pycountry
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from user_details.serializers import PatientSerializer, HospitalSerializer, HospitalStaffSerializer
from custom_auth.serializers import UserSerializerWithoutToken, UserSerializer
from user_details.models import Hospital, HospitalStaff, Patient
from custom_auth.views import username_generator


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
    password = []
    password.append(random.choice(lowercase_characters))
    for i in range(10):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


class CreateHospitalStaff(APIView):

    @staticmethod
    @csrf_exempt
    def post(request):
        try:
            Hospital.objects.get(user=request.user)
        except Hospital.DoesNotExist:
            return Response({'status': 'failure', 'message': 'Unauthorised'})

        response_list = []
        for i in request.data:

            # Create User
            response = {}
            country_code = pycountry.countries.search_fuzzy(i["Country"])[0].alpha_2
            user_role_code = i["Role"][0].capitalize()
            username = country_code + user_role_code + username_generator()
            password = generate_random_password()
            serializer = UserSerializerWithoutToken(data={'username': username,
                                                          'last_name': i['Name'],
                                                          'email': i['Email'],
                                                          'password': password})
            if serializer.is_valid():
                # Create Staff Details
                serializer.save()
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                user_id = user.id
                hos_code = Hospital.objects.get(user=request.user)
                phone_prefix = '+' + str(phonenumbers.country_code_for_region(country_code))
                contact = phone_prefix + i['Contact']
                staff_serializer = HospitalStaffSerializer(data={'user': user_id,
                                                                 'hos_code': hos_code,
                                                                 'role': user_role_code,
                                                                 'degree': i["Degree"],
                                                                 'designation': i["Designation"],
                                                                 'department': i['Department'],
                                                                 'contact': contact})
                if staff_serializer.is_valid():

                    # Send Welcome message with username and password
                    staff_serializer.save()
                    context = {
                        'password': password,
                        'username': username,
                        'email': i['Email'],
                        'last_name': i['Name'],
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
                        [i['Email']]
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
                    HospitalStaff.objects.get(hos_code=request.user.id, user=User.objects.get(email=i["Email"]).id)
                    response["message"] = {
                        'user': ['There is an user with this email already associated with this hospital']}
                except HospitalStaff.DoesNotExist:
                    response["message"] = serializer.errors

            response_list.append(response)

        return Response({'status': 'success', 'data': response_list})


class CreateUpdateUserDetails(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        request.data['user'] = request.user.id

        # Update Request
        if request.data['update']:
            try:
                if request.user.patient:
                    serializer = PatientSerializer(instance=request.user.patient, data=request.data)
                elif request.user.hospital:
                    serializer = HospitalSerializer(instance=request.user.hospital, data=request.data)
                elif request.user.hospital_staff:
                    serializer = HospitalStaffSerializer(instance=request.user.hospital_staff, data=request.data)
            except Patient.DoesNotExist:
                return Response({'status': 'failure', 'message': 'Patient details does not exists'})
            except Hospital.DoesNotExist:
                return Response({'status': 'failure', 'message': 'Hospital details does not exists'})
            except HospitalStaff.DoesNotExist:
                return Response({'status': 'failure', 'message': 'Hospital Staff details does not exists'})

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'data': serializer.data})
            return Response({'status': 'failure', 'message': serializer.errors})

        # Create Request
        else:
            if request.user.username[2] == "P":
                serializer = PatientSerializer(data=request.data)
            elif request.user.username[2] == "H":
                serializer = HospitalSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'data': serializer.data})
            return Response({'status': 'failure', 'message': serializer.errors})


class GetHospitalStaffDetails(APIView):
    @staticmethod
    @csrf_exempt
    def get(request):
        try:
            Hospital.objects.get(user=request.user)
        except Hospital.DoesNotExist:
            return Response({'status': 'failure', 'message': 'Unauthorised'})

        response_list = []
        for i in HospitalStaff.objects.filter(hos_code=request.user.hospital):
            staff_serializer = dict(HospitalStaffSerializer(i, many=False).data)
            user_serializer = dict(UserSerializer(i.user, many=False).data)
            user_serializer.update(staff_serializer)
            response_list.append(user_serializer)
        return Response({'status': 'success', 'data': response_list})
