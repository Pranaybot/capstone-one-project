from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Optional


class RoundTripReviewUpdateForm(FlaskForm):

    rating = DecimalField('Rating', places=1, validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    timestamp = DateTimeField('Review timestamp', validators=[Optional()])