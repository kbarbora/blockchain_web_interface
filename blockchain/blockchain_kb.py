"""
@author: Kevin Barba
"""
from time import time
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from _collections import OrderedDict
import binascii
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from uuid import uuid4

MINING_SENDER = 'The Blockchain'
MINING_REWARD = 1


class Blockchain:
    def __init__(self):
        """
        Constructor for the blockchain,
        which creates the genesis block
        """
        self._transactions = ['Genesis transaction']
        self._chain = []
        self.node_id = str(uuid4()).replace('-', '')
        # Create the genesis block and reset transaction var
        self.create_block(0, 'Genesis')

    def create_block(self, nonce, previous_hash):
        """
        Add a block of transaction to the blockchain
        :param nonce:
        :param previous_hash:
        :return:
        """
        block = {
            'block_number': len(self._chain) + 1,
            'timestamp': time(),
            'transactions': self._transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        # Reset the current list of transactions
        self._transactions = []
        self._chain.append(block)
        return block

    @staticmethod
    def _verify_transaction_signature(sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        hash_from_transaction = SHA.new(str(transaction).encode('utf-8'))
        try:
            verifier.verify(hash_from_transaction, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

    @staticmethod
    def proof_of_work():
        return 12345

    @staticmethod
    def hash(block):
        return 'abc'

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'amount': amount})
        # Reward for mining a block
        if sender_public_key == MINING_SENDER:
            self._transactions.append(transaction)
            return len(self._chain)
        # Transaction for wallet to another wallet
        else:
            signature_verification = self._verify_transaction_signature(sender_public_key, signature, transaction)
            if signature_verification:
                self._transactions.append(transaction)
                return len(self._chain) + 1
            else:
                return False

    def get_transactions(self):
        return self._transactions

    def get_block(self, block_index):
        return self._chain[block_index]


# Instantiate the blockchain
blockchain = Blockchain()
# Instantiate the blockchain
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index_kb.html')


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.get_transactions()
    response = {'transactions': transactions}
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form
    # TODO: check the required fields
    required = ['confirmation_sender_public_key', 'confirmation_recipient_public_key',
                'transaction_signature', 'confirmation_amount']
    # Make sure we have all the field populated before proceeding
    if not all(k in values for k in required):
        return 'Missing values', 400
    result = blockchain.submit_transaction(
        values['confirmation_sender_public_key'], values['confirmation_recipient_public_key'],
        values['transaction_signature'], values['confirmation_amount'])
    if result:
        response = {'message': 'Valid, transaction will be added to the block #' + str(result)}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid'}
        return jsonify(response), 406


@app.route('/mine', methods=['GET'])
def mine():
    nonce = blockchain.proof_of_work()
    blockchain.submit_transaction(sender_public_key=MINING_SENDER,
                                  recipient_public_key=blockchain.node_id,
                                  signature='',
                                  amount=MINING_REWARD)
    last_block = blockchain.get_block(-1)
    # @TODO change hash function to get previous hash
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)
    response = {
        'message': 'New block created',
        'block_number': block['block_number'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="Port to listen to the connection")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
