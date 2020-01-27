from flask import Flask, render_template

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


@app.route('/make/transactions')
def make_transactions():
    return render_template('make_transactions.html')


@app.route('/view/transactions')
def view_transactions():
    return render_template('view_transactions.html')


@app.route('/wallet/new')
def new_wallet():
    return render_template('')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help="Port to listen to the connection")
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
