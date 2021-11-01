import datetime
import hashlib
import json
import requests
from requests.exceptions import ConnectionError
from decouple import config


class Block:
    """
    :param nonce: <int> The proof given by the Proof of Work algorithm
    :param previous_hash: <str> Hash of previous Block
    :param data: <dict> Data to be stored across the block
    :return: <json> Block instance
    """

    def __init__(self, nonce, previous_hash, data):
        self.timestamp = str(datetime.datetime.now())
        self.version = 1
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.data = data

    def jsonify(self):
        return json.dumps(self.__dict__)


class Blockchain:

    def __init__(self):
        self.chain = []
        self.nodes = {"127.0.0.1:8000", "127.0.0.1:8001"}
        self.data = {}
        self.create_block(nonce=1, previous_hash='0', data={"primary": None,
                                                            "secondary": [],
                                                            "collection": None,
                                                            "document": None})

    def create_block(self, nonce, previous_hash, data):
        """
        :param nonce: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: <str> Hash of previous Block
        :param data: <dict> Data to be stored across the block
        :return: <obj> New Block
        """
        block = Block(nonce, previous_hash, data)
        self.chain.append(block.jsonify())
        return block

    def get_tail_block(self):
        """
        :return: <str> Block instance of the tail
        """
        return self.chain[-1]

    @staticmethod
    def get_nonce(previous_nonce):
        """
        :param previous_nonce: <int> The proof of the tail block
        :return: <int> New Nonce generated from the Proof of Work algorithm
        """
        nonce = 1
        check = False
        while check is False:
            hash_operation = hashlib.sha256(str(nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_operation[:4] == config('BLOCK_NONCE'):
                check = True
            else:
                nonce += 1
        return nonce

    @staticmethod
    def get_hash(block):
        """
        :param block: <str> The instance of the tail block
        :return: <str> Encoding using UTF-8 and SHA-256
        """
        encoded_block = block.encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def check_validity(self, chain):
        """
        :param chain: <list> The Blockchain itself
        :return: <bool> Is Valid
        """
        head = chain[0]
        index = 1
        while index < len(chain):
            block = chain[index]
            if json.loads(block)['previous_hash'] != self.get_hash(head):
                return False
            previous_nonce = json.loads(head)['nonce']
            nonce = json.loads(block)['nonce']
            hash_operation = hashlib.sha256(str(nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_operation[:4] != config('BLOCK_NONCE'):
                return False
            head = block
            index += 1
        return True

    def consensus(self):
        """
        :return: <bool> Consensus Algorithm to maintain a common agreement and return true if chain replaced
        """
        longest = None
        maxlength = len(self.chain)
        for node in self.nodes:
            try:
                response = requests.get(f'http://{node}/blockchain/get/')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    if length > maxlength:
                        maxlength = length
                        longest = [json.dumps(i) for i in chain]
            except ConnectionError:
                continue
        if longest:
            self.chain = longest
            return True
        return False
