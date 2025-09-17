# This file makes the models directory a Python package
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instances to be initialized in app.py
db = SQLAlchemy()
bcrypt = Bcrypt()