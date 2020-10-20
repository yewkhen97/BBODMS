import hashlib
import json
import glob
from datetime import datetime
import os
import pytz
peer = set()

class Block:
    def __init__(self, index, OrganOwner, OrganName, timestamp, current_hash, previous_hash, nonce):
        self.index = index
        self.OrganOwner = OrganOwner
        self.OrganName = OrganName
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.current_hash = current_hash
        self.nonce = nonce

    def compute_hash(self):
        block_str = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()

    def __str__(self):
        return str(self.__dict__)

class BlockChain:
    difficulty = 2
    def __init__(self):
        self.chain = []

        if not os.path.isdir('BlockChainFile'):
            os.mkdir('BlockChainFile/')
        if not os.path.isdir('BlockChainFile/Block 0.json'):
            self.genesis_block()

    def genesis_block(self):
        genesis_block = Block(0, "0","0", 0, "0","0",0)
        Genesis = {
            "index": genesis_block.index,
            "OrganOwner": genesis_block.OrganOwner,
            "OrganName": genesis_block.OrganName,
            "timestamp": genesis_block.timestamp,
            "previous_hash": genesis_block.previous_hash,
            "current_hash": genesis_block.current_hash,
            "nonce": genesis_block.nonce
        }
        fileName = ("BlockChainFile/Block %d.json" % genesis_block.index)
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
        previous_hash = self.last_block.current_hash

        if previous_hash != block.previous_hash:
            return False

        newBlock = {
            "index": block.index,
            "OrganOwner": block.OrganOwner,
            "OrganName": block.OrganName,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "current_hash": block.current_hash,
            "nonce": block.nonce
        }

        fileName=("BlockChainFile/Block %d.json" %(block.index))
        nextBlock = json.dumps(newBlock, indent=6)
        with open(fileName, 'w') as f:
            f.write(nextBlock)
            f.close()
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        computed_hash = block.compute_hash()
        while not (computed_hash.startswith('0' * BlockChain.difficulty) and ("22" * BlockChain.difficulty) in computed_hash):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        return (block_hash.startswith('0' * BlockChain.difficulty) and
                block_hash == block.compute_hash())


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

        for num in range(i,sortedList[-1].index+1):
            if(num == sortedList[-1].index or num == sortedList[num].index):
                self.chain.append(sortedList[num])
            else:
                print("Block %d is missing" % num)
                break

        result = self.chain_validation()
        return result

    def chain_validation(self):
        result = "validated"

        for i in range(1, len(self.chain)):
            if self.chain[i-1].current_hash != self.chain[i].previous_hash:
                result = self.chain[i].index
                return result
            temp_hash = self.chain[i].current_hash
            if not temp_hash == '0':
                self.chain[i].current_hash = '0'
                self.chain[i].current_hash = self.chain[i].compute_hash()
                if not self.chain[i].current_hash == temp_hash:
                    result = self.chain[i].index
                    return result
                    break



    def mine(self, donation):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.chain:
            self.chain_retrive()

        last_block = self.last_block
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
                         previous_hash=last_block.current_hash,
                         current_hash='0',
                         nonce=0
                          )
        new_block.current_hash = self.proof_of_work(new_block)

        self.add_block(new_block)

        return True




b =BlockChain()

a=Block(1,"0","0", 0, "0","0",0)
b.mine(a)
b.chain.clear()
b.chain_retrive()
for i in b.chain:
    print(i.index)
