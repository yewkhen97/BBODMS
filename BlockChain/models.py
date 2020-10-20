from BlockChain import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    userType = db.Column(db.String(5), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png ')
    address = db.Column(db.String(120))
    phone_num = db.Column(db.String(11))
    job_title = db.Column(db.String(20))
    donation = db.relationship('Donation', backref='pic', lazy=True)


    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.userType}', '{self.image_file}','{self.password}')"

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OrganOwner = db.Column(db.String(100), nullable=False)
    OrganName = db.Column(db.String(100), nullable=False)
    donate_date = db.Column(db.DateTime, nullable=False)
    approval_status = db.Column(db.String(10), nullable=False, default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Donation('{self.OrganName}', '{self.donate_date}', '{self.OrganOwner}','{self.approval_status}')"