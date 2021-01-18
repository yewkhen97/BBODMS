from BlockChain.util.hash_util import *
from BlockChain.util.verification import verfication
import glob
from datetime import datetime
import pytz
import requests
import os


class Block:
    def __init__(self, index, donor, organ_name, blood_type, height, weight, age, hla_group,
                 update_from_block, approval_date_1, approval_date_2, approval_date_3,
                 timestamp, previous_hash, status, nonce):
        self.index = index
        self.donor = donor
        self.organ_name = organ_name
        self.blood_type = blood_type
        self.height = height
        self.weight = weight
        self.age = age
        self.hla_group = hla_group
        self.approval_date_1 = approval_date_1
        self.approval_date_2 = approval_date_2
        self.approval_date_3 = approval_date_3
        self.timestamp = timestamp
        self.update_from_block = update_from_block
        self.previous_hash = previous_hash
        self.status = status
        self.nonce = nonce

    def __str__(self):
        return str(self.__dict__)


class BlockChain:

    def __init__(self, port):
        self.__chain = []
        self.host_node = port
        self.peer = set()
        self.resolve_conflict = False

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def genesis_block(self):
        genesis_block = Block(0, "0", "0", "0", 0, 0, 0, "0", "0", "0", "0", "0", "0", "0", "0", 0)
        self.add_block(genesis_block)

    def add_block(self, block):
        """
        function to save the block locally after validation

        """
        new_block = {
            "index": block.index,
            "donor": block.donor,
            "organ_name": block.organ_name,
            "blood_type": block.blood_type,
            "height": block.height,
            "weight": block.weight,
            "age": block.age,
            "hla_group": block.hla_group,
            "approval_date_1": block.approval_date_1,
            "approval_date_2": block.approval_date_2,
            "approval_date_3": block.approval_date_3,
            "timestamp": block.timestamp,
            "update_from_block": block.update_from_block,
            "previous_hash": block.previous_hash,
            "status": block.status,
            "nonce": block.nonce
        }
        file_name = "C:BlockChainFile/Block {}.json".format(block.index)
        next_block = json.dumps(new_block, indent=6)
        with open(file_name, 'w') as f:
            f.write(next_block)
            f.close()
        return True

    @property
    def last_block(self):
        return self.__chain[-1]

    def proof_of_work(self, hashed_block):
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not (verfication.valid_proof(hashed_block, proof)):
            proof += 1

        return proof

    #function for chain file validation and hash validation, hash recompute function is missing
    def chain_retrive(self):

        file_name = 'C:BlockChainFile/Block 0.json'

        if not os.path.isdir('C:BlockChainFile'):
            os.mkdir('C:BlockChainFile')
            if not os.path.isdir(file_name):
                self.genesis_block()
                self.blockchain_consensus()

        chain_list=[]
        path = 'C:BlockChainFile/*.json'
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                block_file = json.loads(f.read())
                chain_list.append(Block(**block_file))

        sorted_list = sorted(chain_list, key=lambda i: i.index)

        for num in sorted_list:
            self.__chain.append(num)

        result = verfication.chain_validation(self.__chain)
        return result

    # function for synchronize the blockchain data
    def sync_block(self, block):
        proof_is_valid = verfication.valid_proof(block['previous_hash'], block['nonce'])
        hash_match = compute_hash(self.__chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hash_match:
            return False
        converted_block = Block(block['index'], block['donor'], block['organ_name'],block['blood_type'],
                                block['height'],block['weight'], block['age'], block['hla_group'],
                                block['update_from_block'], block['approval_date_1'], block['approval_date_2'],
                                block['approval_date_3'], block['timestamp'], block['previous_hash'],
                                block['status'], block['nonce'])
        self.__chain.append(converted_block)
        self.add_block(converted_block)
        return True

    def mine(self, donation):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        last_block = self.__chain[-1]
        hashed_block = compute_hash(last_block)
        proof = self.proof_of_work(hashed_block)
        new_index = int(last_block.index)
        timezone = pytz.timezone('Asia/Kuala_Lumpur')
        timeNow = datetime.now(timezone)
        timeNow = timeNow.strftime('%Y-%m-%dT%H:%M:%S.%f')
        new_index += 1
        if donation.update_block:
            old_index = donation.block_index
            status = "Not Available"
        else:
            old_index = 0
            status = "Available"
        new_block = Block(
                         index=new_index,
                         donor=donation.donor,
                         organ_name=donation.organ_name,
                         blood_type=donation.blood_type,
                         height=donation.height,
                         weight=donation.weight,
                         age=donation.age,
                         hla_group=donation.hla_group,
                         approval_date_1=donation.approval_date_1,
                         approval_date_2=donation.approval_date_2,
                         approval_date_3=donation.approval_date_3,
                         timestamp=timeNow,
                         update_from_block=old_index,
                         previous_hash=hashed_block,
                         status=status,
                         nonce=proof
                          )
        self.__chain.append(new_block)
        self.add_block(new_block)
        for node in self.peer:
            try:
                url = "http://{}/broadcast_block".format(node)
                converted_block = new_block.__dict__.copy()
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined (function mine)")
                    return False
                if response.status_code == 409:
                    self.resolve_conflict = True
                    self.blockchain_consensus()
            except requests.exceptions.ConnectionError:
                continue
        return True

    def blockchain_consensus(self):
        temp_chain = self.chain
        replace = False
        for node in self.peer:
            print("Consensus 1")
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['donor'], block['organ_name'],block['blood_type'],
                                    block['height'],block['weight'], block['age'], block['hla_group'],
                                    block['update_from_block'], block['approval_date_1'], block['approval_date_2'],
                                    block['approval_date_3'], block['timestamp'], block['previous_hash'],
                                    block['status'], block['nonce']) for block in node_chain]
                node_chain_length = len(node_chain)
                count = 0
                for block in node_chain:
                    print(block.index)
                print("count:", count)
                print("Node chain len:", node_chain_length)
                local_chain_length = len(self.__chain)
                print("Local chain len:", local_chain_length)
                print("Consensus 2")
                if node_chain_length > local_chain_length and verfication.chain_validation(node_chain):
                    temp_chain = node_chain
                    replace = True
                    print("Consensus 3")
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflict = False

        self.chain = temp_chain
        for block in self.__chain:
            self.add_block(block)
        return replace

    # Code Section for node
    def get_port(self):
        return self.host_node

    def load_dependence_chain(self):
        temp_chain = self.chain
        for node in self.peer:
            print("Dependence 1")
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                print("Dependence 2")
                node_chain = response.json()
                node_chain = [Block(block['index'], block['donor'], block['organ_name'],block['blood_type'],
                                    block['height'],block['weight'], block['age'], block['hla_group'],
                                    block['update_from_block'], block['approval_date_1'], block['approval_date_2'],
                                    block['approval_date_3'], block['timestamp'], block['previous_hash'],
                                    block['status'], block['nonce']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(self.__chain)
                if node_chain_length > local_chain_length and verfication.chain_validation(node_chain):
                    temp_chain = node_chain
                    print("Dependence 3")
            except requests.exceptions.ConnectionError:
                continue
        self.chain = temp_chain
        return self.chain




