from BlockChain.blockchain import BlockChain, Block
from flask import session

ip_address = ""
blockchain = BlockChain(ip_address)


def get_chain():
    blockchain.chain = []
    blockchain.chain_retrive()
    existing_chain = blockchain.chain
    return existing_chain


def register_peer(node):
    print("model ip:", ip_address)
    blockchain.add_node(node)


def get_node():
    print("get ip: ", ip_address)
    all_node = blockchain.get_node()
    return all_node


def sync_new_block(block):
    result = blockchain.sync_block(block)
    return result


def set_session(current_node):
    session['current_node'] = current_node['node']
    global blockchain
    blockchain = BlockChain(session['current_node'])
    blockchain.load_node()
    node = blockchain.get_port()
    if node == "":
        print("not node in chain")
    else:
        print("node in blockchain: ", node)
    all_peer = get_node()
    print("all peer: ", all_peer)


def save_broadcast_node(node):
    blockchain.add_node(node, is_received=True)


def is_conflict():
    blockchain.resolve_conflict = True


def resolve_conflict():
    blockchain.blockchain_consensus()