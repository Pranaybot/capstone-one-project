from main.extensions.connect_db import db
from main.extensions.bcrypt_and_database import current_time


class RoundTripPayment(db.Model):

    __tablename__ = 'round_trip_payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_trip_payment_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    flight_first_departure_airport = db.Column(db.Text, nullable=False)
    flight_first_arrival_airport = db.Column(db.Text, nullable=False)
    flight_first_airline_name = db.Column(db.Text, nullable=False)
    flight_departure_date = db.Column(db.Text, nullable=False)
    flight_first_duration = db.Column(db.Numeric(scale=2), nullable=False)
    flight_last_departure_airport = db.Column(db.Text, nullable=False)
    flight_last_arrival_airport = db.Column(db.Text, nullable=False)
    flight_last_airline_name = db.Column(db.Text, nullable=False)
    flight_arrival_date = db.Column(db.Text, nullable=False)
    flight_last_duration = db.Column(db.Numeric(scale=2), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=current_time)
    num_adults = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, nullable=False)
    num_infants = db.Column(db.Integer, nullable=False)
    cabin_class = db.Column(db.Text, nullable=False)
    total_amount_paid = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)

    # Relationship to RoundTripReview (one-to-many)
    round_trip_reviews = db.relationship('RoundTripReview', backref='payment')

