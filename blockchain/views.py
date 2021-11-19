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
from user_details.models import HospitalStaff

blockchain = Blockchain()


class MineBlock(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        secondary = []
        try:
            User.objects.get(username=request.data["primary"])
        except User.DoesNotExist:
            response = {'status': 'failure', 'message': 'Patient ID does not exist'}
            return Response(response)
        try:
            secondary.append(request.user.username)
            secondary.append(request.user.hospital_staff.hos_code.user.username)
        except HospitalStaff.DoesNotExist:
            response = {'status': 'failure', 'message': 'Unauthorised to Mine'}
            return Response(response)
        response = {'status': 'failure', 'message': 'Invalid chain'}

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
        response = {'status': 'failure', 'message': 'Invalid chain'}
        if blockchain.check_validity(blockchain.chain):
            chain = [json.loads(i) for i in blockchain.chain]
            response_list = []
            collection = request.query_params.get('collection')
            for i in chain[1:]:
                data = json.loads(cryptocode.decrypt(i["data"], config('BLOCK_CRYPTO_KEY')))
                if data["primary"] == request.user.username:
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
                    else:
                        response_list.append(data["collection"])
            if not collection:
                response_list = list(set(response_list))
            response = {'status': 'success', 'data': response_list}
        return Response(response)


class Consensus(APIView):
    @staticmethod
    def get(request):
        response = {'status': 'success', 'message': 'valid'}
        if not blockchain.consensus():
            response = {'status': 'success', 'message': 'invalid'}
        return Response(response)
