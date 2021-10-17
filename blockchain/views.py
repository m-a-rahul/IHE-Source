import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .blockchain import Blockchain
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt

blockchain = Blockchain()


class MineBlock(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        previous_block = blockchain.get_tail_block()
        previous_nonce = json.loads(previous_block)['nonce']
        nonce = blockchain.get_nonce(previous_nonce)
        previous_hash = blockchain.get_hash(previous_block)
        data = {
            'primary': request.data['primary'],
            'secondary': request.data['secondary'].split(", "),
            'collection': request.data['collection'],
            'document': request.data['info'],
        }
        blockchain.create_block(nonce, previous_hash, data)
        response = {'status': 'success', 'message': 'New block created'}
        return Response(response)


class GetChain(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        response = {'chain': [json.loads(i) for i in blockchain.chain],
                    'length': len(blockchain.chain)}
        return Response(response)


class Validate(APIView):
    @staticmethod
    def get(request):
        response = {'status': 'success', 'message': 'valid'}
        if not blockchain.check_validity(blockchain.chain):
            response = {'status': 'success', 'message': 'invalid'}
        return Response(response)


class Consensus(APIView):
    @staticmethod
    def get(request):
        response = {'status': 'success', 'message': 'Chain replaced'}
        if not blockchain.consensus():
            response = {'status': 'success', 'message': 'Current chain follows consensus algorithm'}
        return Response(response)
