import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .blockchain import Blockchain
from rest_framework import permissions

blockchain = Blockchain()


class MineBlock(APIView):
    @staticmethod
    def get(request):
        previous_block = blockchain.get_tail_block()
        previous_nonce = json.loads(previous_block)['nonce']
        nonce = blockchain.get_nonce(previous_nonce)
        previous_hash = blockchain.get_hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'status': 'success',
                    'timestamp': block.timestamp,
                    'nonce': block.nonce,
                    'previous_hash': block.previous_hash}
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
        response = {'message': 'valid'}
        if not blockchain.check_validity(blockchain.chain):
            response = {'message': 'invalid'}
        return Response(response)


class Consensus(APIView):
    @staticmethod
    def get(request):
        response = {'message': 'valid'}
        if not blockchain.consensus():
            response = {'message': 'invalid'}
        return Response(response)

