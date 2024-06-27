from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField
from wtforms.validators import DataRequired, Optional, AnyOf


class PaymentForm(FlaskForm):
    timestamp = DateTimeField('Payment timestamp', validators=[Optional()])
    payment_method = StringField('Payment method', validators=[DataRequired(), AnyOf(values=
                                ["Credit card", "Debit card", "Wire-transfer", "PayPal", "Cash"],
                                message="The value is invalid. It must be a choice from these "
                                        "options: %(values)s.")])

