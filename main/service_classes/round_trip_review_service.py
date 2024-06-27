from main.models import RoundTripReview, RoundTripPayment, User


class RoundTripReviewService:

    def add_round_trip_review(payment_id, form, db):

        round_trip_review_payment_id = payment_id
        rating = round(float(form.rating.data), 1),
        review = form.review.data
        timestamp = form.timestamp.data

        review = RoundTripReview(
            round_trip_review_payment_id=round_trip_review_payment_id,
            rating=rating,
            review=review,
            timestamp=timestamp
        )

        db.session.add(review)
        db.session.commit()

    def get_round_trip_reviews(curr_id, db):

        # Get the current user ID from the session
        current_user_id = curr_id

        # Filter the query by user ID and payment ID
        user_reviews = (
            db.session.query(
                RoundTripReview.id,
                RoundTripReview.round_trip_review_payment_id,
                RoundTripReview.rating,
                RoundTripReview.review,
                RoundTripReview.timestamp
            ).join(RoundTripPayment, RoundTripPayment.id == RoundTripReview.round_trip_review_payment_id)
             .filter(RoundTripPayment.round_trip_payment_user_id == current_user_id)
             .order_by(RoundTripReview.timestamp.desc())
             .limit(100)
             .all()
        )

        return user_reviews

    def delete_round_trip_review(review_id, db):

        review = RoundTripReview.query.get(review_id)
        db.session.delete(review)
        db.session.commit()

    def update_round_trip_review(review_id, form, db):

        review_to_update = RoundTripReview.query.get(review_id)

        review_to_update.round_trip_review_payment_id = form.round_trip_review_payment_id.data
        review_to_update.rating = form.rating.data
        review_to_update.review = form.review.data
        review_to_update.timestamp = form.timestamp.data

        db.session.commit()
