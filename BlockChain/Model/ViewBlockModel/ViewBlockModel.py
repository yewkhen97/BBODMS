from BlockChain.BlockChain import *
from flask import jsonify, request

def get_chain():
    existing_chain = BlockChain()
    existing_chain.chain_retrive()
    result = existing_chain.chain
    return result

def validate_chain(existing_chain):
    result = "validated"

    for i in existing_chain:
        temp_hash = i.current_hash
        if not temp_hash == '0':
            i.current_hash = '0'
            i.current_hash = i.compute_hash()
            if not i.current_hash == temp_hash:
                result = i.index
                break

    return result

def sync_chain():
    chain_data = []
    existing_chain = BlockChain()
    existing_chain.chain_retrive()
    for block in existing_chain.chain:
        chain_data.append(block.__dict__)
    localchain = json.dumps({"length": len(chain_data),
                "chain": chain_data})
    for block in localchain:
        fileName = ("BlockChainFile/Block %d.json" % (block.index))
        nextBlock = json.dumps(block, indent=6)
        with open(fileName, 'w') as f:
            f.write(nextBlock)
            f.close()

    return {"msg": "Created"}, 201

def register_new_peer():
    node_data = request.get_json()
    BlockChain.create_node(node_data.get('address'))
    response = {
        'message': 'New node has been added',
        'node_count': len(BlockChain.nodes),
        'nodes': list(BlockChain.nodes),
    }
    return jsonify(response), 201