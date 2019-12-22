from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd168651a2aa242e14428a991c42164ef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Groundwater@2019@localhost/groundwater'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groundwater.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from groundwater import water
