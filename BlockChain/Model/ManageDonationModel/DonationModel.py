from BlockChain import db
from BlockChain.models import Donation, Node
from BlockChain.blockchain import *
from flask_login import current_user
from flask import session


def set_donation(form):
    timeNow = set_time_now()
    if form.other_hla_group.data:
        hla_group = form.other.data
    else:
        hla_group = form.hla_group.data
    donation = Donation(donor=form.donor.data, organ_name=form.organ_name.data, blood_type=form.blood_type.data,
                        height=form.height.data, weight=form.weight.data, age=form.age.data, hla_group=hla_group,
                        pic=current_user, register_date=timeNow)
    db.session.add(donation)
    db.session.commit()
    return True


def get_donation_list():
    result = Donation.query.filter_by(pic=current_user)
    resultlist = [dict(d.serializable, user=[d.pic.serializable])for d in result]
    return resultlist


def get_pending_list():
    print(current_user.email)
    if current_user.email == "admin000@admin.com":
        result=Donation.query.filter_by(approval_status_1="pending")
    elif current_user.email == "admin001@admin.com":
        result=Donation.query.filter_by(approval_status_2="pending")
    else:
        result=Donation.query.filter_by(approval_status_3="pending")
    resultlist = [dict(d.serializable, user=[d.pic.serializable]) for d in result]
    return resultlist


def get_details(id):
    result=Donation.query.get_or_404(id)
    return result


def set_time_now():
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    time_now = datetime.now(timezone)
    time_now = time_now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    return time_now


def set_approve_status(approval, donation):
    timeNow = set_time_now()
    if current_user.email == "admin000@admin.com":
        donation.approval_status_1 = approval
        donation.approval_date_1 = timeNow
    elif current_user.email == "admin001@admin.com":
        donation.approval_status_2 = approval
        donation.approval_date_2 = timeNow
    else:
        donation.approval_status_3 = approval
        donation.approval_date_3 = timeNow
    db.session.commit()
    if ((donation.approval_status_1 == "Approved") and (donation.approval_status_2 == "Approved")
        and (donation.approval_status_3 == "Approved")):
        retrieve_confirmed_donation()


def retrieve_confirmed_donation():
    new_donation = Donation.query.filter_by(approval_status_1='Approved', approval_status_2='Approved',
                                            approval_status_3='Approved').first()
    new_mine = BlockChain(session['current_node'])
    new_mine.chain_retrive()
    node_list = get_peer()
    for node in node_list:
        new_mine.peer.add(node['node_address'])
    if new_mine.mine(new_donation):
        if new_mine.resolve_conflict:
            return False
        new_donation.approval_status_1 = "Added"
        new_donation.approval_status_2 = "Added"
        new_donation.approval_status_3 = "Added"
    else:
        print("Resolve conflict: ",new_mine.resolve_conflict)
        print("some thing wrong when adding new block")
        new_donation.approval_status_1 = "Approved"
        new_donation.approval_status_2 = "Approved"
        new_donation.approval_status_3 = "Approved"
    db.session.commit()
    return True


def mine_new_block():
    donation_list = Donation.query.filter_by(approval_status_1='Approved', approval_status_2='Approved',
                                            approval_status_3='Approved')
    new_mine = BlockChain(session['current_node'])
    new_mine.chain_retrive()
    new_mine.load_node()
    for donation in donation_list:
        if new_mine.resolve_conflict:
            return False
        if new_mine.mine(donation):
            donation.approval_status_1 = 'Added'
            donation.approval_status_2 = 'Added'
            donation.approval_status_3 = 'Added'
        else:
            print("Resolve conflict: ", new_mine.resolve_conflict)
            print("some thing wrong when adding new block")
            donation.approval_status_1 = 'Approved'
            donation.approval_status_2 = 'Approved'
            donation.approval_status_3 = 'Approved'
    db.session.commit()
    return True

def get_peer():
    all_node = Node.query.all()
    node_list = [d.serializable for d in all_node]
    return node_list