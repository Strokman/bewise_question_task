from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError, NumberRange


class CountForm(FlaskForm):

    count = IntegerField(label='How much questions?',
                         render_kw={'placeholder': 'How much questions?'},
                         validators=[NumberRange(1, 100), DataRequired()])
    submit = SubmitField(label='Submit')
