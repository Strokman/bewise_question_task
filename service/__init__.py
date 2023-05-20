import service

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


# from os import urandom

app = Flask(__name__)

# app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task.db'

db = SQLAlchemy(app)

from service import routes


