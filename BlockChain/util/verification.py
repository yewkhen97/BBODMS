from BlockChain.util.hash_util import compute_hash,compute_hash256

class verfication:

    @staticmethod
    def valid_proof(hash, proof):
        normal_str= (str(hash) + str(proof)).encode()
        hashed_str = compute_hash256(normal_str)
        return hashed_str[0:2] == "00"

    @classmethod
    def chain_validation(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != compute_hash(blockchain[index - 1]):
                print(f"block {block.index} has problem.")
                print("Hash not match")
                return False
            if not cls.valid_proof(block.previous_hash, block.nonce):
                print('Proof of work is invalid')
                return False
        return True
