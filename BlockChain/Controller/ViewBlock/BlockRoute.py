from flask import render_template,  Blueprint, request, jsonify
from flask_login import login_required
from BlockChain.Model.ViewBlockModel.ViewBlockModel import (get_chain, register_peer, get_node,
                                                            sync_new_block,set_session,
                                                            save_broadcast_node, is_conflict, resolve_conflict
                                                            )

BlockRoute = Blueprint('BlockRoute', __name__)


@BlockRoute.route("/")
@BlockRoute.route("/home")
def home():
    return render_template('ViewBlock/home.html')


@BlockRoute.route("/chain", methods=['GET'])
def retrieve_chain():
    local_chain = get_chain()
    for block in local_chain:
        print("Block retrieve: ",block.index)
    dict_chain = [block.__dict__.copy() for block in local_chain]
    return jsonify(dict_chain), 200


@BlockRoute.route("/update_block", methods=["GET", "POST"])
@login_required
def update_block():
    block_index = int(request.form["block_index"])
    chain = get_chain()
    for block in chain:
        if block.index == block_index:
            target_block = block
            print("update block:", target_block)
    return render_template('ViewBlock/request_update.html', block=target_block)


@BlockRoute.route('/add_node', methods=['POST'])
def register_node():
    data = request.get_json()
    print("Data Get in register_node:", data['node'])
    if not data:
        response = {
            "message": "No data attached"
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
        "message": "node is added successfully",
        "all_peer_node": get_node()
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
    local_block = get_chain()
    value = request.get_json()
    if not value:
        response = {"message" : "Value not found"}
        print("no value")
        return jsonify(response), 400
    if 'block' not in value:
        response = {"message": "block not found"}
        print("no block")
        return jsonify(response), 400
    block = value['block']
    if block['index'] == local_block[-1].index+1:
        if sync_new_block(block):
            response = { "message": "Block added"}
            return jsonify(response), 201
        else:
            response = {"message": "Block declined"}
            print(response)
            return jsonify(response), 409
        
    elif block['index'] > local_block[-1].index:
        response = {"message": "Block is differ with the local blockchain"}
        is_conflict()
        return jsonify(response), 200
    else:
        response = {"message": "blockchain is smaller than local blockchain"}
        return jsonify(response), 409


@BlockRoute.route("/consensus")
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

