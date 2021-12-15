from flask import Flask
from flask import request
from block import Block
import datetime as date
import json
from collections import Counter
from flask import render_template
import pickle
from flask import g




node = Flask(__name__)




# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy



# blockchain = []
# blockchain.append(Block.create_genesis_block())

def get_blockchain():
    blockchain = getattr(g, '_blockchain', None)
    if blockchain is None:
        g._blockchain = []
        g._blockchain.append(Block.create_genesis_block())
        #g._blockchain = blockchain
        print(g._blockchain)
    else:
        print("blockchain NOT NONE")
    return g._blockchain

def set_blockchain(blockchain):
    g._blockchain = blockchain


# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True





@node.route('/txion', methods=['POST'])
def transaction():
  if request.method == 'POST':
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print("New transaction")
    print("FROM: {}".format(new_txion['from']))
    print("TO: {}".format(new_txion['to']))
    print("AMOUNT: {}\n".format(new_txion['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"


@node.route('/', methods=['GET'])
def index():
    blockchain = get_blockchain()
    n = Counter(blockchain)
    return render_template('index.html', n=n)

@node.route('/save', methods=['GET'])
def persist():
    output = open('blockchain.pkl', 'wb')
    blockchain = get_blockchain()
    pickle.dump(blockchain, output)
    output.close()
    return "ok"


@node.route('/load', methods=['GET'])
def loadblockchain():
    pkl_file = open('blockchain.pkl', 'rb')
    blockchain = pickle.load(pkl_file)
    set_blockchain(blockchain)
    pkl_file.close()
    return blockchain


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = get_blockchain()
    blocks = []
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for block in chain_to_send:
        json_block = block.getJson()
        blocks.append(json_block)

    response = node.response_class(
        response=json.dumps(blocks, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response

def proof_of_work(last_proof):
    # Create a variable that we will use to find
    # our next proof of work
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    # Get the last proof of work
    blockchain = get_blockchain()
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so 
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
        { "from": "network", "to": miner_address, "amount": 1 }
    )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)
    set_blockchain(blockchain)
    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"
#node.run()