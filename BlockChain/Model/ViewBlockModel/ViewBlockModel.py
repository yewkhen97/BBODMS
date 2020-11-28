from BlockChain.blockchain import *
from BlockChain import db
from flask import session
from flask_login import current_user
from BlockChain.models import Donation, Node

ip_address = ""
blockchain = BlockChain(ip_address)


def get_chain():
    blockchain.chain = []
    blockchain.chain_retrive()
    existing_chain = blockchain.chain
    return existing_chain


def register_peer(node):
    exist = db.session.query(Node.node_address).filter_by(node_address=node).scalar() is not None
    if exist:
        return False
    node = Node(node_address=node)
    db.session.add(node)
    db.session.commit()
    return True


def get_peer():
    all_node = Node.query.all()
    node_list = [d.serializable for d in all_node]
    for node in node_list:
        blockchain.peer.add(node['node_address'])


def sync_new_block(block):
    result = blockchain.sync_block(block)
    return result


def set_session(current_node):
    session['current_node'] = current_node['node']
    global blockchain
    blockchain = BlockChain(session['current_node'])
    get_peer()
    node = blockchain.get_port()
    if node == "":
        print("not node in chain")
    else:
        print("node in blockchain: ", node)
    all_peer = get_peer()
    print("all peer: ", all_peer)


def is_conflict():
    blockchain.resolve_conflict = True


def resolve_conflict():
    get_peer()
    result = blockchain.blockchain_consensus()
    return result


def set_request_block(index, donor, organ_name, age, weight, height, hla_group, blood_type, applier_details,
                        update_block):
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    timeNow = datetime.now(timezone)
    timeNow = timeNow.strftime('%Y-%m-%dT%H:%M:%S.%f')
    donation = Donation(donor=donor, organ_name=organ_name, blood_type=blood_type,
                        height=height, weight=weight, age=age, hla_group=hla_group,
                        pic=current_user, register_date=timeNow, block_index=index,
                        update_block=update_block, applier_details=applier_details)
    db.session.add(donation)
    db.session.commit()


def verify_with_peer(node):
    exist = db.session.query(Node.node_address).filter_by(node_address=node).scalar() is not None
    if exist:
        return True
    return False


def load_dependence_chain():
    get_peer()
    dependence_chain = blockchain.load_dependence_chain()
    dict_chain = [block.__dict__.copy() for block in dependence_chain]
    return dict_chain
