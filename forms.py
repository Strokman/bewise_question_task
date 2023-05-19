from flask_wtf import FlaskForm
from wtforms import IntegerField


class CountForApiRequest(FlaskForm):

    def __init__(self):
        self.count = IntegerField()