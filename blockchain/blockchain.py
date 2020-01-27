"""
@author: Kevin Barba
"""
from time import time

from flask import Flask, render_template


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

    def create_block(self, nonce, previous_hash):
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
        self._chain(block)
        return


# Instantiate the blockchain
blockchain = Blockchain()

# Instantiate the blockchain
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('./index.html')

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help="Port to listen to the connection")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
