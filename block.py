import hashlib as hasher
import datetime as date
import uuid


# Define what a Schèi block is
class Block:
    index = 0
    timestamp = 0
    data = None
    previous_hash = ''
    hash = ''
    nonce = None


    def __init__(self, index, timestamp, data, previous_hash, nonce=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        if nonce is None:
            nonce = Block.create_nonce()
        self.nonce = nonce


    def getJson(self):
        block_index = str(self.index)
        block_timestamp = str(self.timestamp)
        block_data = str(self.data)
        block_previous_hash = self.previous_hash
        block_hash = self.hash
        block_nonce = self.nonce
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "previous_hash": block_previous_hash,
            "hash": block_hash,
            "nonce" : block_nonce.hex
        }
        return block

    def hash_block(self):
        sha = hasher.sha256()
        # sha.update(str(self.index).encode('utf-8'))
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )
        return sha.hexdigest()

    def create_nonce():
        return uuid.uuid4()

    # Generate all later blocks in the blockchain
    def next_block(last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = "Hey! I'm block " + str(this_index)
        this_hash = last_block.hash
        this_nonce = Block.create_nonce()
        return Block(this_index, this_timestamp, this_data, this_hash, this_nonce)

    # Generate genesis block
    def create_genesis_block():
        # Manually construct a block with
        # index zero and arbitrary previous hash
        return Block(0, date.datetime.now(),
            {
             "proof-of-work": 9,
             "transactions": None
            }
            , "0")
