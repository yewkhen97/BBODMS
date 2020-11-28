from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, jsonify, json)
from flask_login import login_required
from BlockChain.Controller.ManageDonation.Form import DonationForm,approvalForm
from BlockChain.Model.ManageDonationModel.DonationModel import (set_donation, get_pending_list, get_details,
                                                                set_approve_status,get_donation_list,
                                                                retrieve_confirmed_donation, mine_new_block)



ManageDonation = Blueprint('ManageDonation', __name__)


@ManageDonation.route("/view_list")
@login_required
def view_donation():
    return render_template('ManageDonation/Donation_list.html')


@ManageDonation.route("/load_list", methods=['GET'])
def load_donation():
    donation = get_donation_list()
    return jsonify(donation), 200


@ManageDonation.route("/donation/new", methods=['GET', 'POST'])
@login_required
def new_donation():
    form = DonationForm()
    if form.validate_on_submit():
        set_donation(form)
        flash('Your donation request has been created!', 'success')
        return redirect(url_for('ManageDonation.view_donation'))
    return render_template('ManageDonation/create_donation.html', title='New Donation',
                           form=form, legend='New Donation')


@ManageDonation.route("/pending_list")
@login_required
def view_pending_list():
    return render_template('ManageDonation/pending_list.html')


@ManageDonation.route("/load_pending_list", methods=['GET', 'POST'])
@login_required
def load_pending_list():
    pending_list = get_pending_list()
    return jsonify(pending_list), 200


@ManageDonation.route("/set_approval", methods=['POST'])
def set_approval():
    approval = request.form.get('approval')
    record_id = request.form.get('record_id')
    target_donation = get_details(record_id)
    set_approve_status(approval, target_donation)
    return render_template('ManageDonation/pending_list.html')


@ManageDonation.route("/mine_block")
def mine_block():
    if not mine_new_block():
        response = {"message": "Resolve Conflicts first"}
        print("resolve conflict")
        return jsonify(response), 409
    response = {"message": "All work well"}
    return jsonify(response), 200


@ManageDonation.route("/test")
def debug():
    if mine_new_block():
        response={
            "message": "OK"
        }
    else:
        response = {
            "message": "Error"
        }
    return jsonify(response), 200
