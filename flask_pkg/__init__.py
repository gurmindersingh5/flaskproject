from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta
from flask_jwt_extended import JWTManager

app = Flask(__name__,static_url_path='/flask_pkg/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "lovely17"

# config session in app
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False  # Sessions won't expire on browser close
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # Session timeout

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'ABC123ABC123'  # Replace with your secret key
jwt = JWTManager(app)

Session(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from . import routes
from . import models

with app.app_context():
    db.create_all()






