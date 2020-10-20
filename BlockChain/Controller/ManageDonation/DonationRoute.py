from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import login_required
from BlockChain.Controller.ManageDonation.Form import DonationForm,approvalForm
from BlockChain.Model.ManageDonationModel.DonationModel import set_donation, get_pending_List, get_details, set_approve_status,get_donation_list

ManageDonation = Blueprint('ManageDonation', __name__)


@ManageDonation.route("/Donation_list")
def view_Donation():
    donation = get_donation_list()
    return render_template('ManageDonation/Donation_list.html', donation=donation)


@ManageDonation.route("/donation/new", methods=['GET', 'POST'])
@login_required
def New_Donation():
    form = DonationForm()
    if form.validate_on_submit():
        set_donation(form)
        flash('Your donation request has been created!', 'success')
        return redirect(url_for('ManageDonation.view_Donation'))
    return render_template('ManageDonation/create_donation.html', title='New Donation',
                           form=form, legend='New Donation')

@ManageDonation.route("/pending_list", methods=['GET', 'POST'])
@login_required
def pending_list():
    list = get_pending_List()
    return render_template('ManageDonation/pending_list.html', list=list)

@ManageDonation.route("/pending_donation/<int:donation_id>",methods=['GET', 'POST'])
def donation_details(donation_id):
    donation = get_details(donation_id)
    form = approvalForm()
    if form.validate_on_submit():
        set_approve_status(form, donation)
        flash('The record has been updated!', 'success')
        return redirect(url_for('ManageDonation.pending_list'))
    elif request.method == 'GET':
        form.approval_status.data = donation.approval_status
    return render_template('ManageDonation/donation_detail.html', title=donation.OrganName, donation=donation, form=form)