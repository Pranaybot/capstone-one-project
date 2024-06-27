from flask import render_template, redirect, \
    url_for, session, flash, g, current_app
from main.forms import RoundTripReviewForm, RoundTripReviewUpdateForm
from main.extensions.bcrypt_and_database import db
from main.service_classes.round_trip_review_service import RoundTripReviewService
from . import round_trip_reviews_bp


@round_trip_reviews_bp.route("/round_trip_reviews")
def round_trip_reviews():

    user_reviews = RoundTripReviewService.get_round_trip_reviews(session[current_app.config['CURR_USER_KEY']], db)

    return render_template("round_trip_reviews.html", reviews=user_reviews)  # Pass name of user as well


@round_trip_reviews_bp.route("/round_trip_reviews/add/<int:payment_id>", methods=["GET", "POST"])
def add_round_trip_review(payment_id):
    
    form = RoundTripReviewForm()
    if form.validate_on_submit():
        RoundTripReviewService.add_round_trip_review(payment_id, form, db)

        return redirect(f"/round_trip_reviews")

    return render_template("round_trip_new_review.html", form=form)


@round_trip_reviews_bp.route('/round_trip_reviews/<int:review_id>/delete', methods=["GET", "POST"])
def round_trip_reviews_destroy(review_id):
    
    RoundTripReviewService.delete_round_trip_review(review_id, db)
    return redirect(f"/round_trip_reviews")


@round_trip_reviews_bp.route('/round_trip_reviews/<int:review_id>/edit',
           methods=["GET", "POST"])
def round_trip_reviews_update(review_id):

    form = RoundTripReviewUpdateForm()

    if form.validate_on_submit():
        RoundTripReviewService.update_round_trip_review(review_id, form, db)
        return redirect(f"/round_trip_reviews")

    return render_template("round_trip_update_review.html", form=form)
