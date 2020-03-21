"""
@author: Kevin Barba
"""
from time import time
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from _collections import OrderedDict

class Blockchain:
    def __init__(self):
        """
        Constructor for the blockchain,
        which creates the genesis block
        """
        self._transactions = []
        self._chain = []
        # Create the genesis block
        self._create_block(0, 'Genesis')

    def _create_block(self, nonce, previous_hash):
        """
        Add a block of transaction to the blockchain
        :param nonce:
        :param previous_hash:
        :return:
        """
        block = {
            'number': len(self._chain) + 1,
            'timestamp': time(),
            'transactions': self._transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }
        # Reset the current list of transactions
        self._transactions = []
        self._chain.append(block)
        return

    def submit_transaction(self, sender_public_key, recipient_public_key, signature, amount):
        # TODO: Reward the miner
        # TODO: Signature verification
        transaction = OrderedDict({
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'signature': signature,
            'amount': amount})
        signature_verification = True
        if signature_verification:
            self._transactions.append(transaction)
            return len(self._chain) + 1
        else:
            return False

# Instantiate the blockchain
blockchain = Blockchain()

# Instantiate the blockchain
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.form
    # TODO: check the required fields
    result = blockchain.submit_transaction(
        values['confirmation_sender_public_key'], values['confirmation_recipient_public_key'],
        values['transaction_signature'], values['confirmation_amount'])
    if result:
        response = {'message': 'Valid, transaction will be added to the block #' + str(result)}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid'}
        return jsonify(response), 406


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="Port to listen to the connection")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
