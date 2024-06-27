from main.extensions.connect_db import db
from main.extensions.bcrypt_and_database import current_time


class OneWayTripReview(db.Model):

    __tablename__ = 'one_way_trip_review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oneway_trip_review_payment_id = db.Column(db.Integer, db.ForeignKey('one_way_trip_payments.id', ondelete='cascade'))
    rating = db.Column(db.Numeric(precision=2, scale=1), nullable=False)
    review = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=current_time)
