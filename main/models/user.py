from main.extensions.connect_db import db
from main.extensions.bcrypt_and_database import bcrypt


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
