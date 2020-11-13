from BlockChain.util.hash_util import *
from BlockChain.util.verification import verfication
import glob
from datetime import datetime
import pytz
import requests
import os


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
        self.host_node = port
        self.peer = set()
        self.resolve_conflict = False


    def get_chain(self):
        return self.chain[:]

    def genesis_block(self):
        genesis_block = Block(0, "0","0", 0, "0",0)
        self.add_block(genesis_block)

    def add_block(self, block):
        """
        function to save the block locally after validation

        """
        newBlock = {
            "index": block.index,
            "OrganOwner": block.OrganOwner,
            "OrganName": block.OrganName,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce
        }
        _string_host, string_port = str(self.host_node).split(":")
        file_name = "BlockChainFile{}/Block {}.json".format(string_port, block.index)
        next_block = json.dumps(newBlock, indent=6)
        with open(file_name, 'w') as f:
            f.write(next_block)
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
        _string_host, string_port = str(self.host_node).split(":")
        file_name='BlockChainFile/Block 0.json'.format(string_port)

        if not os.path.isdir('BlockChainFile{}'.format(string_port)):
            os.mkdir('BlockChainFile{}'.format(string_port))
        if not os.path.isdir(file_name):
            self.genesis_block()

        chain_list=[]
        path = 'BlockChainFile{}/*.json'.format(string_port)
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                block_file = json.loads(f.read())
                chain_list.append(Block(**block_file))

        sorted_list = sorted(chain_list, key=lambda i: i.index)

        for num in sorted_list:
            self.chain.append(num)

        result = verfication.chain_validation(self.chain)
        return result

    # function for synchronize the blockchain data
    def sync_block(self, block):
        proof_is_valid = verfication.valid_proof(block['previous_hash'], block['nonce'])
        hash_match = compute_hash(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hash_match:
            return False
        converted_block = Block(block['index'], block['OrganOwner'], block['OrganName'],
                                block['timestamp'],block['previous_hash'],block['nonce'])
        self.chain.append(converted_block)
        self.add_block(converted_block)
        return True

    def mine(self, donation):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """

        if not self.get_chain():
            self.chain_retrive()
        else:
            print(self.chain)
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
        self.load_node()
        for node in self.peer:
            try:
                url = "http://{}/broadcast_block".format(node)
                converted_block = new_block.__dict__.copy()
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined (function mine)")
                if response.status_code == 409:
                    self.resolve_conflict = True
                    return False
            except requests.exceptions.ConnectionError:
                continue
        return True

    def blockchain_consensus(self):
        temp_chain = self.chain
        replace = False
        for node in self.peer:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['OrganOwner'], block['OrganName'],
                            block['timestamp'],block['previous_hash'],block['nonce']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(self.chain)
                if node_chain_length > local_chain_length and verfication.chain_validation(node_chain):
                    temp_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflict = False
        self.chain = temp_chain
        for block in self.chain:
            self.add_block(block)
        return replace

    # Code Section for node

    def add_node(self, nodes, is_received=False):
        self.load_node()
        self.peer.add(nodes)
        self.set_node()
        if not is_received:
            for node in self.peer:
                try:
                    url = 'http://{}/broadcast_node'.format(node)
                    response = requests.post(url, json={"nodes": nodes})
                    if response.status_code == 400 or response.status_code == 500:
                        print("node broadcast problem")
                        return False
                    return True
                except requests.exceptions.ConnectionError:
                    continue

    def load_node(self):
        _string_host, string_port = str(self.host_node).split(":")
        try:
            file_name = "BlockChain/peer_node{}.txt".format(string_port)
            with open(file_name, mode='r') as f:
                peer = json.loads(f.read())
                self.peer = set(peer)
                f.close()
        except OSError:
            self.peer = set()

    def set_node(self):
        _string_host, string_port = str(self.host_node).split(":")
        file_name = "BlockChain/peer_node{}.txt".format(string_port)
        with open(file_name, mode='w') as f:
            peer = json.dumps(list(self.peer))
            f.write(peer)
            f.close()

    def remove_node(self, node):
        self.peer.discard(node)
        self.set_node()

    def get_node(self):
        return list(self.peer)[:]

    def get_port(self):
        return self.host_node
