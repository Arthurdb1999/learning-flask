from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

from app import routes, database