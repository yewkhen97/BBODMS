from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'edeb4bd9aa87d514843726'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from BlockChain.Controller.ManageUser.UserRoute import users
from BlockChain.Controller.ManageDonation.DonationRoute import ManageDonation
from BlockChain.Controller.ViewBlock.BlockRoute import BlockRoute
app.register_blueprint(users)
app.register_blueprint(ManageDonation)
app.register_blueprint(BlockRoute)


if __name__ == '__main__':
   from argparse import ArgumentParser
   parser = ArgumentParser()
   parser.add_argument('-p', '--port', default=5000)
   args = parser.parse_args()
   port = args.port
   app.run(host="0.0.0.0", port=port)
