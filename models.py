from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    # Relationship to RoundTripPayment (one-to-many)
    round_trip_payments = db.relationship('RoundTripPayment', backref='user')

    # Relationship to OneWayTripPayment (one-to-many)
    one_way_trip_payments = db.relationship('OneWayTripPayment', backref='user')

    @classmethod
    def signup(cls, username, email, password, name):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            name=name
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class RoundTripPayment(db.Model):

    __tablename__ = 'round_trip_payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_trip_payment_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    flight_first_departure_airport = db.Column(db.Text, nullable=False)
    flight_first_arrival_airport = db.Column(db.Text, nullable=False)
    flight_first_airline_name = db.Column(db.Text, nullable=False)
    flight_first_departure_timestamp = db.Column(db.Text, nullable=False)
    flight_first_arrival_timestamp = db.Column(db.Text, nullable=False)
    flight_first_duration = db.Column(db.Numeric(scale=2), nullable=False)
    flight_last_departure_airport = db.Column(db.Text, nullable=False)
    flight_last_arrival_airport = db.Column(db.Text, nullable=False)
    flight_last_airline_name = db.Column(db.Text, nullable=False)
    flight_last_departure_timestamp = db.Column(db.Text, nullable=False)
    flight_last_arrival_timestamp = db.Column(db.Text, nullable=False)
    flight_last_duration = db.Column(db.Numeric(scale=2), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    num_adults = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, nullable=False)
    num_infants = db.Column(db.Integer, nullable=False)
    cabin_class = db.Column(db.Text, nullable=False)
    total_amount_paid = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)

    # Relationship to RoundTripReview (one-to-one)
    round_trip_reviews = db.relationship('RoundTripReview', backref='payment')


class OneWayTripPayment(db.Model):

    __tablename__ = 'one_way_trip_payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oneway_trip_payment_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    flight_departure_airport = db.Column(db.Text, nullable=False)
    flight_arrival_airport = db.Column(db.Text, nullable=False)
    flight_airline_name = db.Column(db.Text, nullable=False)
    flight_departure_timestamp = db.Column(db.Text, nullable=False)
    flight_duration = db.Column(db.Numeric(scale=2), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    num_adults = db.Column(db.Integer, nullable=False)
    num_children = db.Column(db.Integer, nullable=False)
    num_infants = db.Column(db.Integer, nullable=False)
    cabin_class = db.Column(db.Text, nullable=False)
    total_amount_paid = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)

    # Relationship to OneWayTripReview (one-to-one)
    one_way_trip_reviews = db.relationship('OneWayTripReview', backref='payment')


class RoundTripReview(db.Model):

    __tablename__ = 'round_trip_review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_trip_review_payment_id = db.Column(db.Integer, db.ForeignKey('round_trip_payments.id', ondelete='cascade'))
    rating = db.Column(db.Numeric(precision=2, scale=1), nullable=False)
    review = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())


class OneWayTripReview(db.Model):

    __tablename__ = 'one_way_trip_review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oneway_trip_review_payment_id = db.Column(db.Integer, db.ForeignKey('one_way_trip_payments.id', ondelete='cascade'))
    rating = db.Column(db.Numeric(precision=2, scale=1), nullable=False)
    review = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())


def connect_db(app):

    db.app = app
    db.init_app(app)


