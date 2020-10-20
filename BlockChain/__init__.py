from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'edeb4bd9aa87d514843726'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from BlockChain.Controller.ManageUser.UserRoute import users
from BlockChain.Controller.ManageDonation.DonationRoute import ManageDonation
from BlockChain.Controller.ViewBlock.BlockRoute import BlockRoute
app.register_blueprint(users)
app.register_blueprint(ManageDonation)
app.register_blueprint(BlockRoute)
