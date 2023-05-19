from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError, NumberRange


class CountForm(FlaskForm):

    count = IntegerField(label='How much questions?',
                         render_kw={'placeholder': 'How much questions?'},
                         validators=[NumberRange(1, 100), DataRequired()])
    submit = SubmitField(label='Submit')

    # def validate_count(self):
    #     if self.count.data:
    #         if self.count.data < 0 or self.count.data > 100:
    #             raise ValidationError('Count should be non-negative integer from 1 to 100')
    #         else:
    #             return True
