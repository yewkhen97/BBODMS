from BlockChain import db
from BlockChain.models import Donation
from BlockChain.blockchain import *
from flask_login import current_user

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
    retrieve_confirmed_donation()


def retrieve_confirmed_donation():
    new_donation = Donation.query.filter_by(approval_status='Approved').first()
    new_mine = BlockChain()
    new_mine.mine(new_donation)
    new_donation.approval_status = "Added"
    db.session.commit()

