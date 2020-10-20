from flask import flash, render_template,  Blueprint, request, jsonify
from BlockChain.Model.ViewBlockModel.ViewBlockModel import get_chain,validate_chain, sync_chain
peers = set()

BlockRoute = Blueprint('BlockRoute', __name__)

@BlockRoute.route("/")
@BlockRoute.route("/home")
def home():
    existing_chain = get_chain()
    result = validate_chain(existing_chain)
    if not result is "validated":
        result=str(result)
        Message= 'Block '+result+' is being modified illegally'
        flash(Message, 'danger')
        return render_template('ViewBlock/home.html')
    else:
        return render_template('ViewBlock/home.html', chain=existing_chain)

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

@BlockRoute.route("/register_node", method = ['POST'])
def register_new_peer():


    return sync_chain()

