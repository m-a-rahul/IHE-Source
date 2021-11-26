import json
import cryptocode
import math
import random
from decouple import config
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from blockchain.blockchain import Blockchain
from custom_auth.serializers import UserSerializer
from user_details.serializers import PatientSerializer
from user_details.models import HospitalStaff, BlockchainAccess, Patient, BlockchainAccessOtp

blockchain = Blockchain()


def generate_otp():
    string = '0123456789'
    otp = ""
    length = len(string)
    for i in range(6):
        otp += string[math.floor(random.random() * length)]
    return otp


class MineBlock(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        # Only Hospital Staff are allowed to mine patient records
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)

        # Check if patient id exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except Patient.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)

        # Check if hospital staff has access to add/view this particular patient
        try:
            BlockchainAccess.objects.get(primary=primary_actor,
                                         secondary=request.user.hospital_staff.hos_code)
        except BlockchainAccess.DoesNotExist:
            response = {'status': 'failure',
                        'message': 'You do not have access to add records to this patient'}
            return Response(response)

        # Collect Secondary Actors
        secondary = []
        secondary.append(request.user.username)
        secondary.append(request.user.hospital_staff.hos_code.user.username)

        # Mine
        response = {'status': 'failure', 'message': 'Invalid chain'}
        blockchain.consensus()
        if blockchain.check_validity(blockchain.chain):
            previous_block = blockchain.get_tail_block()
            previous_nonce = json.loads(previous_block)['nonce']
            nonce = blockchain.get_nonce(previous_nonce)
            previous_hash = blockchain.get_hash(previous_block)
            data = {
                'primary': request.data['primary'],
                'secondary': secondary,
                'collection': request.data['collection'],
                'document': request.data['document'],
            }
            blockchain.create_block(nonce, previous_hash, data)
            response = {'status': 'success', 'message': 'New block created'}
        return Response(response)


class GetChain(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        response = {'status': 'failure', 'message': 'Invalid chain'}
        if blockchain.check_validity(blockchain.chain):
            response = {'status': 'success',
                        'chain': [json.loads(i) for i in blockchain.chain],
                        'length': len(blockchain.chain)}
        return Response(response)


class RetrieveRecords(APIView):
    @staticmethod
    def get(request):
        # collection var: To check its a collection or document request
        collection = request.query_params.get('collection')

        # Only hospital staff and patients have access to retrieve records
        if request.user.username[2] == "P":
            try:
                Patient.objects.get(user=request.user)
                primary = request.user.username
            except Patient.DoesNotExist:
                response = {'status': 'failure', 'message': 'Unauthorised'}
                return Response(response)
        else:
            # Collect primary actor from param if hospital staff
            try:
                HospitalStaff.objects.get(user=request.user)
                primary = request.query_params.get('primary')
                if not primary:
                    response = {'status': 'failure', 'message': 'Missing parameters'}
                    return Response(response)
            except HospitalStaff.DoesNotExist:
                response = {'status': 'failure', 'message': 'Unauthorised'}
                return Response(response)

            # Check if patient id exists
            try:
                primary_actor = User.objects.get(username=primary).patient
            except Patient.DoesNotExist:
                response = {'status': 'failure', 'message': 'Patient ID does not exist'}
                return Response(response)
            except User.DoesNotExist:
                response = {'status': 'failure', 'message': 'Patient ID does not exist'}
                return Response(response)

            # Check if hospital staff has access to add/view this particular patient
            try:
                BlockchainAccess.objects.get(primary=primary_actor,
                                             secondary=request.user.hospital_staff.hos_code)
            except BlockchainAccess.DoesNotExist:
                response = {'status': 'failure',
                            'message': 'You do not have access to add records to this patient'}
                return Response(response)

        # Retrieve
        blockchain.consensus()
        response = {'status': 'failure', 'message': 'Invalid chain'}
        if blockchain.check_validity(blockchain.chain):
            chain = [json.loads(i) for i in blockchain.chain]
            response_list = []
            for i in chain[1:]:
                data = json.loads(cryptocode.decrypt(i["data"], config('BLOCK_CRYPTO_KEY')))
                if data["primary"] == primary:

                    # Retrieve Documents
                    if collection:
                        if collection == data["collection"]:
                            result = {}
                            secondary_actors = []
                            documents = []
                            for j in data["secondary"]:
                                secondary_actors.append(UserSerializer(User.objects.get(username=j), many=False).data)
                            result["secondary"] = secondary_actors
                            result["timestamp"] = i["timestamp"]
                            for k in data["document"]:
                                documents.append(k)
                            result["document"] = documents
                            response_list.append(result)

                    # Retrieve Collections
                    else:
                        response_list.append(data["collection"])

            # Remove duplicate collections
            if not collection:
                response_list = list(set(response_list))
            response = {'status': 'success', 'data': response_list}
        return Response(response)


class RequestAccess(APIView):
    @staticmethod
    def post(request):
        # Only hospital staff can request access
        # This request will sent an email containing a 6-digit otp to the patient email id
        # Which the hospital staff can get from the patient inorder to gain add/retrieve access for this patient
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)

        # Check if Patient id exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        except Patient.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)

        # Delete the previous instances consisting these two actors
        secondary_actor = request.user.hospital_staff.hos_code
        try:
            i = BlockchainAccessOtp.objects.get(primary=primary_actor, secondary=secondary_actor)
            i.delete()
        except BlockchainAccessOtp.DoesNotExist:
            pass

        # Send email containing the generated otp
        otp = generate_otp()
        instance = BlockchainAccessOtp(primary=primary_actor, secondary=secondary_actor, otp=otp)
        instance.save()
        context = {
            'last_name': primary_actor.user.last_name,
            'hospital': secondary_actor.user.last_name,
            'otp': otp,
        }
        email_html_message = render_to_string('blockchainaccessotpemail/blockchain_access_otp.html', context)
        email_plaintext_message = render_to_string('blockchainaccessotpemail/blockchain_access_otp.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Hi from IHE",
            # message:
            email_plaintext_message,
            # from:
            "ihe@dailyfishmart.com",
            # to:
            [primary_actor.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        response = {'status': 'success', 'message': 'OTP Sent to patients email id'}
        return Response(response)


class GainAccess(APIView):
    @staticmethod
    def post(request):
        # Only hospital staff are allowed to post the otp sent to the patient's email inorder to gain access
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)

        # Check if Patient id exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        except Patient.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)

        # Verify otp
        secondary_actor = request.user.hospital_staff.hos_code
        otp = request.data["otp"]
        try:
            i = BlockchainAccessOtp.objects.get(primary=primary_actor, secondary=secondary_actor, otp=otp)
        except BlockchainAccessOtp.DoesNotExist:
            response = {'status': 'failure', 'message': 'Invalid OTP'}
            return Response(response)
        validation = timezone.now() - i.created_at
        if validation.total_seconds() < 300:
            instance = BlockchainAccess(primary=i.primary, secondary=i.secondary)
            instance.save()
            i.delete()
            response = {'status': 'success', 'message': 'Access granted'}
        else:
            i.delete()
            response = {'status': 'failure', 'message': 'OTP Expired'}
        return Response(response)


class CheckAccess(APIView):
    @staticmethod
    def post(request):
        # Only hospital staff are allowed
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)

        # Check if Patient id exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        except Patient.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)

        # Check Access
        secondary_actor = request.user.hospital_staff.hos_code
        patient_serializer = dict(PatientSerializer(Patient.objects.get(user=primary_actor), many=False).data)
        user_serializer = dict(UserSerializer(User.objects.get(username=request.data["primary"]), many=False).data)
        user_serializer.update(patient_serializer)
        try:
            BlockchainAccess.objects.get(primary=primary_actor, secondary=secondary_actor)
        except BlockchainAccess.DoesNotExist:
            response = {'status': 'success', 'message': 'DENIED', 'data': user_serializer}
            return Response(response)
        response = {'status': 'success', 'message': 'GRANTED', 'data': user_serializer}
        return Response(response)


class GetMyPatients(APIView):
    @staticmethod
    def get(request):
        # Only hospital staff are allowed
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)

        blockchain.consensus()
        response = {'status': 'failure', 'message': 'Invalid chain'}
        if blockchain.check_validity(blockchain.chain):
            chain = [json.loads(i) for i in blockchain.chain]
            response_list = []
            patient_list = []
            for i in chain[1:]:
                data = json.loads(cryptocode.decrypt(i["data"], config('BLOCK_CRYPTO_KEY')))
                if request.user.username in data["secondary"]:
                    patient_list.append(data["primary"])
            # Remove duplicate collections
            patient_list = list(set(patient_list))

            for i in patient_list:
                patient = User.objects.get(username=i)
                patient_serializer = dict(PatientSerializer(Patient.objects.get(user=patient), many=False).data)
                user_serializer = dict(UserSerializer(patient, many=False).data)
                user_serializer.update(patient_serializer)
                response_list.append(user_serializer)
            response = {'status': 'success', 'data': response_list}
        return Response(response)
