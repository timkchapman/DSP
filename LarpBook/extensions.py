from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_stripe import Stripe

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
session = Session()
stripe = Stripe()
