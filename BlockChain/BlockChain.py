from BlockChain.util.hash_util import *
from BlockChain.util.verification import verfication
import glob
from datetime import datetime
import pytz
import requests
import socket
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

class Block:
    def __init__(self, index, OrganOwner, OrganName, timestamp, previous_hash, nonce):
        self.index = index
        self.OrganOwner = OrganOwner
        self.OrganName = OrganName
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def __str__(self):
        return str(self.__dict__)

class BlockChain:
    difficulty = 2

    def __init__(self, port):
        self.chain = []
        self.chain_retrive()
        self.host_node = port
        self.peer = set()
        self.load_node()


    def get_chain(self):
        return self.chain[:]

    def genesis_block(self):
        genesis_block = Block(0, "0","0", 0, "0",0)
        Genesis = {
            "index": genesis_block.index,
            "OrganOwner": genesis_block.OrganOwner,
            "OrganName": genesis_block.OrganName,
            "timestamp": genesis_block.timestamp,
            "previous_hash": genesis_block.previous_hash,
            "nonce": genesis_block.nonce
        }
        fileName=("BlockChainFile{}/Block %d.json".format(self.port) %(Genesis.index))
        GenesisFile = json.dumps(Genesis, indent=6)
        with open(fileName, 'w') as f:
            f.write(GenesisFile)
            f.close()



    def add_block(self, block):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        newBlock = {
            "index": block.index,
            "OrganOwner": block.OrganOwner,
            "OrganName": block.OrganName,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce
        }

        fileName=("BlockChainFile{}/Block %d.json".format(self.port) %(block.index))
        nextBlock = json.dumps(newBlock, indent=6)
        with open(fileName, 'w') as f:
            f.write(nextBlock)
            f.close()
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, hashed_block):
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not (verfication.valid_proof(hashed_block, proof)):
            proof += 1

        return proof



    #function for chain file validation and hash validation, hash recompute function is missing
    def chain_retrive(self):
        list=[]
        i=0
        path = 'BlockChainFile/*.json'
        files = glob.glob(path)
        for name in files:
           with open(name) as f:
               block_file = json.loads(f.read())
               list.append(Block(**block_file))

        sortedList = sorted(list, key=lambda i: i.index)

        for num in sortedList:
            self.chain.append(num)

        result = verfication.chain_validation(self.chain)
        return result

    def sync_block(self, block):
        proof_is_valid = verfication.valid_proof(block['previous_hash'], block['proof'])
        hash_match = compute_hash(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid and hash_match:
            return False
        converted_block = Block(block['index'], block['OrganOwner'], block['OrganName'], block['timestamp'],block['previous_hash'],block['nonce'])
        self.chain.append(converted_block)
        self.add_block(converted_block)
        return True

    def mine(self, donation):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        last_block = self.last_block
        hashed_block = compute_hash(last_block)
        proof = self.proof_of_work(hashed_block)
        new_index = int(last_block.index)
        timezone = pytz.timezone('Asia/Kuala_Lumpur')
        timeNow = datetime.now(timezone)
        timeNow = timeNow.strftime('%Y-%m-%dT%H:%M:%S.%f')
        new_index += 1
        new_block = Block(
                         index=new_index,
                         OrganOwner=donation.OrganOwner,
                         OrganName=donation.OrganName,
                         timestamp=timeNow,
                         previous_hash=hashed_block,
                         nonce=proof
                          )
        self.chain.append(new_block)
        self.add_block(new_block)
        for node in self.peer:
            url = "http://{}/broadcast_block".format(node)
            converted_block = new_block.__dict__.copy()
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined")
                    return False
            except requests.exceptions.ConnectionError:
                continue


        return True

    def add_node(self, node):
        self.peer.add(node)
        self.set_node()

    def load_node(self):
        try:
            fileName = "BlockChain/peer_node{}.txt".format(self.host_node)
            with open(fileName, mode='r') as f:
                peer = json.loads(f.read())
                self.peer = set(peer)
                f.close()
        except OSError:
            self.peer = set()

    def set_node(self):
        port = self.host_node
        print("set port:", port)
        #fileName = "BlockChain/peer_node{}.txt".format(self.host_node)
        #print(fileName)
        print("current node in set node: ", self.host_node)
        print(self.peer)
        #with open(fileName, mode='w') as f:
        #    peer = json.dumps(list(self.peer))
        #    f.write(peer)
        #    f.close()

    def remove_node(self, node):
        self.peer.discard(node)
        self.set_node()

    def get_node(self):
        return list(self.peer)[:]

    def get_port(self):
        return self.host_node