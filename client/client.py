from flask import Flask, render_template, jsonify
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
import binascii

"""
"""


class Transaction:
    def __init__(self, sender_add, sender_priv, recipient_add, value):
        """

        :param sender_add:
        :param sender_priv:
        :param recipient_add:
        :param value:
        """
        self._sender_add = sender_add
        self._sender_priv = sender_priv
        self._recipient_add = recipient_add
        self._value = value


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make/transaction')
def make_transaction():
    return render_template('make_transaction.html')


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    return "Done"


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
