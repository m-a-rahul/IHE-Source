import json
import cryptocode
from decouple import config
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from blockchain.blockchain import Blockchain
from custom_auth.serializers import UserSerializer
from user_details.serializers import PatientSerializer
from user_details.models import HospitalStaff, BlockchainAccess, Patient

blockchain = Blockchain()


class MineBlock(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)
        blockchain.consensus()
        # Check if Primary actor exists
        try:
            User.objects.get(username=request.data["primary"])
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        secondary = []

        # Collect Secondary Actors
        try:
            secondary.append(request.user.username)
            secondary.append(request.user.hospital_staff.hos_code.user.username)
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised to Mine'}
            return Response(response)
        response = {'status': 'failure', 'message': 'Invalid chain'}

        # Mine
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
        blockchain.consensus()
        response = {'status': 'failure', 'message': 'Invalid chain'}
        if blockchain.check_validity(blockchain.chain):
            chain = [json.loads(i) for i in blockchain.chain]
            response_list = []
            collection = request.query_params.get('collection')
            primary = None
            try:
                if request.user.username[2] == "P":
                    primary = request.user.username
                elif request.user.hospital_staff:
                    primary = request.query_params.get('primary')
                    if not primary:
                        response = {'status': 'failure', 'message': 'Missing parameters'}
                        return Response(response)
            except HospitalStaff.DoesNotExist:
                primary = None

            if not primary:
                response = {'status': 'failure', 'message': 'Unauthorised'}
                return Response(response)
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


class GainAccess(APIView):
    @staticmethod
    def post(request):
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)
        # Check if Patient actor exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        secondary_actor = request.user.hospital_staff.hos_code
        instance = BlockchainAccess(primary=primary_actor, secondary=secondary_actor)
        instance.save()
        response = {'status': 'success', 'message': 'Access granted'}
        return Response(response)


class CheckAccess(APIView):
    @staticmethod
    def post(request):
        try:
            request.user.hospital_staff
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised'}
            return Response(response)
        # Check if Patient actor exists
        try:
            primary_actor = User.objects.get(username=request.data["primary"]).patient
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        secondary_actor = request.user.hospital_staff.hos_code
        try:
            BlockchainAccess.objects.get(primary=primary_actor, secondary=secondary_actor)
        except BlockchainAccess.DoesNotExist:
            response = {'status': 'success', 'message': 'DENIED'}
            return Response(response)
        response = {'status': 'success', 'message': 'GRANTED'}
        return Response(response)


class GetMyPatients(APIView):
    @staticmethod
    def get(request):
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
