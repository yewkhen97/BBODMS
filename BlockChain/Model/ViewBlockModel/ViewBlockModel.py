from BlockChain.blockchain import BlockChain
import requests
ip_address = ""
blockchain = BlockChain(ip_address)
def get_chain():
    existing_chain = blockchain.get_chain()
    return existing_chain

def register_peer(node):
    print("model ip:", ip_address)
    blockchain.add_node(node)

def get_node():
    print("get ip: ",ip_address)
    all_node = blockchain.get_node()
    return all_node

def sync_new_block(block):
    result = blockchain.sync_block(block)
    return result

def set_session(current_node):
    global ip_address
    ip_address = current_node
    global blockchain
    blockchain = BlockChain(ip_address)
    node = blockchain.get_port()
    if node == "":
        print("not node in chain")
    else:
        print("node in blockchain: ", node)
    all = get_node()
    print("all peer: ",all)