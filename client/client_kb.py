from flask import Flask, render_template, jsonify, request
import Crypto
import Crypto.Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
import binascii
from collections import OrderedDict
"""
"""


class Transaction:
    def __init__(self, sender_public_key, sender_private_key, recipient_public_key, amount):
        """

        :param sender_add:
        :param sender_priv:
        :param recipient_add:
        :param value:
        """
        self._sender_public_key = sender_public_key
        self._sender_private_key = sender_private_key
        self._recipient_public_key = recipient_public_key
        self._amount = amount

    def to_dict(self):
        return OrderedDict({
            'sender_public_key': self._sender_public_key,
            'recipient_public_key': self._recipient_public_key,
            'amount': self._amount})

    def sign(self):
        private_key = RSA.importKey(binascii.unhexlify(self._sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        hash_from_sign = SHA.new(str(self.to_dict()).encode('utf-8'))
        return binascii.hexlify(signer.sign(hash_from_sign)).decode('ascii')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index_kb.html')


@app.route('/make/transaction')
def make_transaction():
    return render_template('make_transaction_kb.html')


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    sender_public_key = request.form['sender_public_key']
    sender_private_key = request.form['sender_private_key']
    recipient_public_key = request.form['recipient_public_key']
    amount = request.form['amount']
    transaction = Transaction(sender_public_key, sender_private_key, recipient_public_key, amount)
    response = {
        'transaction': transaction.to_dict(),
        'signature': transaction.sign()}
    return jsonify(response), 200


@app.route('/view/transaction')
def view_transaction():
    return render_template('view_transaction.html')


@app.route('/wallet/new')
def new_wallet():
    # return render_template('')
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()

    response = {
        'private_key':  binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
        'public_key':   binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
    }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="Port to listen to the connection")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
