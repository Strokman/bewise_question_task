import questions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv


# from os import urandom

app = Flask(__name__)

# app.config['SECRET_KEY'] = urandom(12)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{getenv("USERNAME")}:' \
#                                         f'{getenv("PASSWD")}@{getenv("HOST")}:' \
#                                         f'{getenv("PORT")}/gis_shishlina'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     f'postgresql://strokman:gPdybKpr04020051@strokman.synology.me:55432/gis_shishlina'
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)

from questions import routes
