from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, Email, Length, AnyOf, Optional, ValidationError


class SignUpForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=8), Length(max=64)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=8), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), Length(max=128)])
    name = StringField('Name', validators=[DataRequired(), Length(min=10), Length(max=50)])


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), Length(max=128)])


class PaymentForm(FlaskForm):
    timestamp = DateTimeField('Payment timestamp', validators=[Optional()])
    payment_method = StringField('Payment method', validators=[DataRequired(),
                                                               AnyOf(values=["Credit card", "Debit card",
                                                                             "Wire-transfer", "PayPal",
                                                                             "Cash"],
                                                               message="The value is invalid. It must be a "
                                                                       "choice from these options: %(values)s.")])


class RoundTripReviewForm(FlaskForm):

    round_trip_review_payment_id = IntegerField('Payment ID', validators=[DataRequired()])
    rating = DecimalField('Rating', places=1, validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    timestamp = DateTimeField('Review timestamp', validators=[Optional()])


class OneWayTripReviewForm(FlaskForm):

    oneway_trip_review_payment_id = IntegerField('Payment ID', validators=[DataRequired()])
    rating = DecimalField('Rating', places=1, validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    timestamp = DateTimeField('Review timestamp', validators=[Optional()])

