import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from blockchain.blockchain import Blockchain
from custom_auth.serializers import UserSerializer

blockchain = Blockchain()


class MineBlock(APIView):
    @staticmethod
    @csrf_exempt
    def post(request):
        response = {'status': 'success', 'message': 'invalid'}
        if blockchain.check_validity(blockchain.chain):
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
        response = {'status': 'success', 'message': 'invalid'}
        if blockchain.check_validity(blockchain.chain):
            response = {'status': 'success',
                        'chain': [json.loads(i) for i in blockchain.chain],
                        'length': len(blockchain.chain)}
        return Response(response)


class RetrieveRecords(APIView):
    @staticmethod
    def get(request):
        response = {'status': 'success', 'message': 'invalid'}
        if blockchain.check_validity(blockchain.chain):
            chain = [json.loads(i) for i in blockchain.chain]
            response_list = []
            collection = request.query_params.get('collection')
            for i in chain[1:]:
                if i["data"]["primary"] == request.user.username:
                    if collection:
                        if collection == i["data"]["collection"]:
                            result = {}
                            secondary_actors = []
                            for j in i["data"]["secondary"]:
                                secondary_actors.append(UserSerializer(User.objects.get(username=j), many=False).data)
                            result["secondary"] = secondary_actors
                            result["document"] = i["data"]["document"]
                            response_list.append(result)
                    else:
                        response_list.append(i["data"]["collection"])
            if not collection:
                response_list = list(set(response_list))
            response = {'status': 'success', 'result': response_list}
        return Response(response)


class Consensus(APIView):
    @staticmethod
    def get(request):
        response = {'status': 'success', 'message': 'valid'}
        if not blockchain.consensus():
            response = {'status': 'success', 'message': 'invalid'}
        return Response(response)
