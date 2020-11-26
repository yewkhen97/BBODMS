from BlockChain import db, login_manager
from flask_login import UserMixin
from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None

    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


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
    gender = db.Column(db.String(6))
    user = db.relationship('Donation', backref='pic', lazy=True)

    @property
    def serializable(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'userType': self.userType}


class Donation(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    donor = db.Column(db.String(100), nullable=False)
    organ_name = db.Column(db.String(100), nullable=False)
    blood_type = db.Column(db.String(2), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hla_group = db.Column(db.String(10), nullable=False)
    register_date = db.Column(db.String, nullable=False)
    approval_status_1 = db.Column(db.String(10), nullable=False, default='pending')
    approval_status_2 = db.Column(db.String(10), nullable=False, default='pending')
    approval_status_3 = db.Column(db.String(10), nullable=False, default='pending')
    block_index = db.Column(db.Integer, nullable=True)
    update_block = db.Column(db.Boolean, default=False)
    applier_details = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def serialize(self):
        d = Serializer.serialize(self)
        return d

    @property
    def serializable(self):
        return {'id': self.id, 'donor': self.donor, 'organ_name': self.organ_name, 'blood_type': self.blood_type,
                'height': self.height, 'weight': self.weight, 'age': self.age, 'hla_group': self.hla_group,
                'register_date': self.register_date, 'approval_status_1':self.approval_status_1,
                'approval_status_2':self.approval_status_2, 'approval_status_3':self.approval_status_3,
                'block_index': self.block_index, 'update_block': self.update_block,
                'applier_details': self.applier_details, 'user_id': self.user_id }

