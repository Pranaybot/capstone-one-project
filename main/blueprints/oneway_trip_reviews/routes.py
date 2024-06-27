from flask import render_template, redirect, url_for, \
    session, flash, g, current_app
from main.forms import OneWayTripReviewForm, OneWayTripReviewUpdateForm
from main.extensions.bcrypt_and_database import db
from main.service_classes.oneway_review_service import OneWayReviewService
from . import oneway_trip_reviews_bp


@oneway_trip_reviews_bp.route("/oneway_trip_reviews")
def oneway_trip_reviews():

    oneway_reviews = OneWayReviewService.get_oneway_reviews(session[current_app.config['CURR_USER_KEY']], db)

    return render_template("oneway_trip_reviews.html", reviews=oneway_reviews)  # Pass name of user as well


@oneway_trip_reviews_bp.route("/oneway_trip_reviews/add/<int:payment_id>", methods=["GET", "POST"])
def oneway_trip_add_review(payment_id):
    
    form = OneWayTripReviewForm()
    if form.validate_on_submit():
        OneWayReviewService.add_oneway_review(payment_id, form, db)

        return redirect(f"/oneway_trip_reviews")

    return render_template("oneway_trip_new_review.html", form=form)


@oneway_trip_reviews_bp.route('/oneway_trip_reviews/<int:review_id>/delete', methods=["GET", "POST"])
def oneway_trip_reviews_destroy(review_id):

    OneWayReviewService.delete_oneway_review(review_id, db)
    return redirect(f"/oneway_trip_reviews")


@oneway_trip_reviews_bp.route('/oneway_trip_reviews/<int:review_id>/edit',
           methods=["GET", "POST"])
def oneway_trip_reviews_update(review_id):

    form = OneWayTripReviewUpdateForm()

    if form.validate_on_submit():
        OneWayReviewService.update_oneway_review(review_id, form, db)
        return redirect(f"/oneway_trip_reviews")

    return render_template("oneway_update_review.html", form=form)
