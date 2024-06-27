from main.models import OneWayTripReview, OneWayTripPayment


class OneWayReviewService:

    def add_oneway_review(payment_id, form, db):

        oneway_trip_review_payment_id = payment_id
        rating = round(float(form.rating.data), 1),
        review = form.review.data
        timestamp = form.timestamp.data

        review = OneWayTripReview(
            oneway_trip_review_payment_id=oneway_trip_review_payment_id,
            rating=rating,
            review=review,
            timestamp=timestamp
        )

        db.session.add(review)
        db.session.commit()

    def get_oneway_reviews(curr_id, db):

        # Get the current user ID from the session
        current_user_id = curr_id

        # Filter the query by user ID and payment ID
        user_reviews = (
            db.session.query(
                OneWayTripReview.id,
                OneWayTripReview.oneway_trip_review_payment_id,
                OneWayTripReview.rating,
                OneWayTripReview.review,
                OneWayTripReview.timestamp
            ).join(OneWayTripPayment, OneWayTripPayment.id == OneWayTripReview.oneway_trip_payment_id)
             .filter(OneWayTripPayment.oneway_trip_payment_user_id == current_user_id)
             .order_by(OneWayTripReview.timestamp.desc())
             .limit(100)
             .all()
        )
            
        return user_reviews

    def delete_oneway_review(review_id, db):

        review = OneWayTripReview.query.get(review_id)
        db.session.delete(review)
        db.session.commit()

    def update_oneway_review(review_id, form, db):

        review_to_update = OneWayTripReview.query.get(review_id)

        review_to_update.oneway_trip_review_payment_id = form.oneway_trip_review_payment_id.data
        review_to_update.rating = form.rating.data
        review_to_update.review = form.review.data
        review_to_update.timestamp = form.timestamp.data

        db.session.commit()
