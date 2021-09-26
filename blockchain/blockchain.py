import datetime
import hashlib
import json


class Block:
    """
    :param nonce: <int> The proof given by the Proof of Work algorithm
    :param previous_hash: <str> Hash of previous Block
    :return: <json> Block instance
    """
    def __init__(self, nonce, previous_hash):
        self.timestamp = str(datetime.datetime.now())
        self.nonce = nonce
        self.previous_hash = previous_hash

    def jsonify(self):
        return json.dumps(self.__dict__)


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce=1, previous_hash='0')

    def create_block(self, nonce, previous_hash):
        """
        :param nonce: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: <str> Hash of previous Block
        :return: <obj> New Block
        """
        block = Block(nonce, previous_hash)
        self.chain.append(block.jsonify())
        return block

    def get_tail_block(self):
        """
        :return: <str> Block instance of the tail
        """
        return self.chain[-1]

    def get_nonce(self, previous_nonce):
        """
        :param previous_nonce: <int> The proof of the tail block
        :return: <int> New Nonce generated from the Proof of Work algorithm
        """
        nonce = 1
        check = False
        while check is False:
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0011':
                check = True
            else:
                nonce += 1
        return nonce

    def get_hash(self, block):
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
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0011':
                return False
            head = block
            index += 1
        return True
