from BlockChain import db
from BlockChain.models import Donation
from BlockChain.blockchain import *
from flask_login import current_user
from flask import session


def set_donation(form):
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    timeNow = datetime.now(timezone)
    donation = Donation(OrganName=form.OrganName.data, OrganOwner=form.OrganOwner.data, pic=current_user,
                        donate_date=timeNow)
    db.session.add(donation)
    db.session.commit()
    return True


def get_donation_list():
        result=Donation.query.filter_by(pic=current_user)
        return result


def get_pending_List():
    list=Donation.query.filter_by(approval_status="pending")
    return list


def get_details(id):
    result=Donation.query.get_or_404(id)
    return result


def set_approve_status(form, donation):
    donation.approval_status = form.approval_status.data
    db.session.commit()


def retrieve_confirmed_donation():
    new_donation = Donation.query.filter_by(approval_status='Approved').first()
    new_mine = BlockChain(session['current_node'])
    print("current session in donation model:",session['current_node'])
    new_mine.chain_retrive()
    print(new_mine.chain)
    if new_mine.mine(new_donation):
        if new_mine.resolve_conflict:
            return False
        new_donation.approval_status = "Added"
    else:
        print("Resolve conflict: ",new_mine.resolve_conflict)
        print("some thing wrong when adding new block")
        new_donation.approval_status = "Approved"
    db.session.commit()
    return True

def mine_new_block():
    donation_list = Donation.query.filter_by(approval_status='Added')
    new_mine = BlockChain(session['current_node'])
    new_mine.chain_retrive()
    new_mine.load_node()
    for donation in donation_list:
        if new_mine.resolve_conflict:
            return False
        if new_mine.mine(donation):
            donation.approval_status = "Added"
        else:
            print("Resolve conflict: ", new_mine.resolve_conflict)
            print("some thing wrong when adding new block")
            donation.approval_status = "Approved"
    db.session.commit()
    return True
