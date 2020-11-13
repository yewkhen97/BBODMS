from flask import render_template,  Blueprint, request, jsonify
from BlockChain.Model.ViewBlockModel.ViewBlockModel import (get_chain, register_peer, get_node,
                                                            sync_new_block,set_session,
                                                            save_broadcast_node, is_conflict, resolve_conflict)

BlockRoute = Blueprint('BlockRoute', __name__)
@BlockRoute.route("/")
@BlockRoute.route("/home")
def home():
    return render_template('ViewBlock/home.html')
@BlockRoute.route("/chain", methods=['GET'])
def retreive_chain():
    local_chain = get_chain()
    dict_chain = [block.__dict__.copy() for block in local_chain]
    return jsonify(dict_chain), 200

@BlockRoute.route("/block_<int:block_id>/details")
def block_details(block_id):
    chain=get_chain()
    for list in chain:
        if list.index == block_id:
            details = list
            break
    return render_template('ViewBlock/block_details.html', title='block_<int:block_index>', block=details)

@BlockRoute.route("/block_<int:block_id>/details")
def search(self, key):
        newlist=[]
        chain = get_chain()
        for a in chain:
            print(a.index)
            if a.OrganName == key:
                newlist.append(a)
        for i in newlist:
            print(i.OrganName)


@BlockRoute.route('/add_node', methods=['POST'])
def register_node():
    data = request.get_json()
    print("Data Get in register_node:", data['node'])
    if not data:
        response = {
            "message" : "No data attached"
        }
        return jsonify(response), 400
    if "node" not in data:
        response = {
            "message": "No node found"
        }
        return jsonify(response), 400
    node = data['node']

    register_peer(node)
    response = {
        "message" : "node is added successfully",
        "all_peer_node" : get_node()
    }
    print("All node in blockchain:", response['all_peer_node'])
    return jsonify(response), 201

@BlockRoute.route('/nodes', methods=['GET'])
def get_all_node():
    response ={
        "message": "Fetched all node",
        "all_node": get_node()
    }
    return jsonify(response), 201

@BlockRoute.route('/broadcast_block', methods=['POST'])
def broadcast_block():
    print("broadcast block is called")
    localblock = get_chain()
    value = request.get_json()
    if not value:
        response = { "message" : "Value not found" }
        return jsonify(response), 400
    if 'block' not in value:
        response = {"message": "block not found"}
        return jsonify(response), 400
    block = value['block']
    print("Broadcast Block:",block)
    if block['index'] == localblock[-1].index+1:
        if sync_new_block(block):
            response = { "message": "Block added" }
            return jsonify(response), 201
        else:
            response = {"message": "Block declined"}
            return jsonify(response), 409
        
    elif block['index'] > localblock[-1].index:
        response ={"message" : "Block is differ with the local blockchain"}
        is_conflict()
        return jsonify(response), 200
    else:
        response = { "message" : "blockchain is smaller than local blockchain" }
        return jsonify(response), 409
    
@BlockRoute.route("/consensus", methods=['POST'] )
def consensus():
    replace = resolve_conflict()
    if replace:
        response = {"message": "blockchain is replaced"}
    else:
        response = {"message": "local blockchain is remaining"}

    return jsonify(response), 200

@BlockRoute.route("/get_ip")
def get_ip():
    return render_template('ViewBlock/add_node.html')

@BlockRoute.route("/show_ip", methods=["POST"])
def show_current_ip():
    current_node = request.get_json()
    set_session(current_node)
    response = {"message": "set node"}
    return jsonify(response), 200


@BlockRoute.route('/broadcast_node', methods=['POST'])
def broadcast_node():
    value = request.get_json()
    if not value:
        response = {"message": "Value not found"}
        return jsonify(response), 400
    if 'nodes' not in value:
        response = {"message": "nodes not found"}
        return jsonify(response), 400
    success = save_broadcast_node(value['nodes'])
    if success:
        response = {"message": "Node added"}
        return jsonify(response), 201
    else:
        response = {"message": "Node declined"}
        return jsonify(response), 500

