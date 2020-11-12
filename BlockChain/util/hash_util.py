import hashlib
import json


def compute_hash256(string):
    return hashlib.sha256(string).hexdigest()


def compute_hash(block):
    hashable_block = block.__dict__.copy()
    return compute_hash256(json.dumps(hashable_block, sort_keys=True).encode())