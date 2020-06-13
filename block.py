'''
https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
'''
from time import time
import json
import hashlib
from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    '''
    Blockchain is responsible for managing the chain. 
    It stores transactions.
    It has helper methods for adding new blocks to the chain. 
    '''
    #constructor creates an empty list to store the blocks amd a list to store transactions
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        ''' 
        Creates a new block and adds it to the chain
        Input:
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        Output: <dict> New Block
        '''

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset current transation
        self.current_transactions = []
        self.chain.append(block)
        return block
    def new_transaction(self, sender, recipient, amount):
        # Adds a new transation to the list of transations
        '''
        Creates a new transation to go into the next mined block
        Input:
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the 
        :param amount: <int> Amount
        Output: <int> The index of the block that will hold this transation
        '''
        self.current_transactions.append(
            {'sender':sender, 'recipient': recipient, 'amount': amount}
        )
        return self.last_block['index'] + 1


    def proof_of_work(self, last_proof):
        '''
        A proof of work algorithm 
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        input: <int> last_proof
        output: <int>
        '''
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof


    @staticmethod
    def hash(block):
        # Hashes a Block
        pass
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]


app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)