from flask import render_template,  Blueprint, request, jsonify
from flask_login import login_required
from BlockChain.Model.ViewBlockModel.ViewBlockModel import (get_chain, register_peer, get_peer,
                                                            sync_new_block, set_session, set_request_block,
                                                            is_conflict, resolve_conflict, verify_with_peer,
                                                            load_dependence_chain)

BlockRoute = Blueprint('BlockRoute', __name__)


@BlockRoute.route("/")
@BlockRoute.route("/home")
def home():
    return render_template('ViewBlock/home.html')


@BlockRoute.route("/chain", methods=['GET'])
def retrieve_chain():
    local_chain = get_chain()
    for block in local_chain:
        print("Block retrieve: ", block.index)
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
    return render_template('ViewBlock/request_update.html', block=target_block)


@BlockRoute.route("/set_update_block", methods=["POST"])
def set_update_block():
    index = request.form.get('index')
    donor = request.form.get('donor')
    organ_name = request.form.get('organ_name')
    age = request.form.get('age')
    weight = request.form.get('weight')
    height = request.form.get('height')
    hla_group = request.form.get('hla_group')
    blood_type = request.form.get('blood_type')
    applier_details = request.form.get('applier_details')
    update_block = True

    if set_request_block(index, donor, organ_name, age, weight, height, hla_group, blood_type, applier_details,
                         update_block):
        response={
            "message": "OK"
        }
    else:
        response = {
            "message": "something wrong"
        }
    return jsonify(response), 200


@BlockRoute.route('/add_node', methods=['POST'])
def register_node():
    data = request.get_json()
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

    result = register_peer(node)
    if result:
        response = {
            "message": "node is added successfully",
            "category": "success",
            "all_peer_node": get_peer()
        }
    else:
        response = {
            "message": "Duplicated node, node not added",
            "category": "danger",
            "all_peer_node": get_peer()
        }
    print("All node in blockchain:", response['all_peer_node'])
    return jsonify(response), 201


@BlockRoute.route('/nodes', methods=['GET'])
def get_all_node():
    response ={
        "message": "Fetched all node",
        "all_node": get_peer()
    }
    return jsonify(response), 201


@BlockRoute.route('/broadcast_block', methods=['POST'])
def broadcast_block():
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
        consensus()
        return jsonify(response), 200
    else:
        response = {"message": "blockchain is smaller than local blockchain"}
        return jsonify(response), 409


@BlockRoute.route("/consensus", methods=["GET"])
def consensus():
    replace = resolve_conflict()
    if replace:
        response = {"message": "Local blockchain is replaced! Page will be reloaded"}
    else:
        response = {"message": "Local blockchain is remaining! Page will be reloaded"}

    return response


@BlockRoute.route("/verify_node", methods=['POST'])
def verify_node():
    data = request.get_json()
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

    result = verify_with_peer(node)
    if result:
        response = consensus()
        return jsonify(response), 200
    else:
        print("verify Node:",result)
        response = {
            "message": "Please enroll into blockchain network first!"
        }
        return jsonify(response), 200


@BlockRoute.route("/show_ip", methods=["POST"])
def set_current_session():
    current_node = request.get_json()
    set_session(current_node)
    node = current_node['node']
    result = verify_with_peer(node)
    if result:
        response = retrieve_chain()
        return response
    response = load_dependence_chain()
    return jsonify(response), 200

