from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from sqlalchemy.exc import IntegrityError
import os

from round_trip_departure_form_check import round_trip_departure_form_check
from round_trip_arrival_form_check import round_trip_arrival_form_check
from oneway_trip_form_check import oneway_trip_form_check
from currency_code_conversion import price_conversion
from trips_error_checking import trips_error_checking
from forms import SignUpForm, LoginForm, PaymentForm, RoundTripReviewForm, OneWayTripReviewForm
from models import db, connect_db, User, RoundTripPayment, OneWayTripPayment, RoundTripReview, OneWayTripReview
from dotenv import load_dotenv

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
load_dotenv()
oneway_trip_url = 'https://serpapi.com/search.json?engine=google_flights&api_key={}' \
                  '&type=2&departure_id={}&arrival_id={}&outbound_date={}&adults={}' \
                  '&children={}&infants_in_seat={}&travel_class={}&currency={}&hl={}' \
                  '&stops=1'
round_trip_departure_url = 'https://serpapi.com/search?engine=google_flights&api_key={}&' \
                 'departure_id={}&arrival_id={}&outbound_date={}&return_date={}&' \
                 'adults={}&children={}&infants_in_seat={}&travel_class={}&currency={}&hl={}' \
                 '&stops=1'
round_trip_arrival_url = 'https://serpapi.com/search?engine=google_flights&api_key={}&' \
                 'departure_id={}&arrival_id={}&outbound_date={}&return_date={}&' \
                 'adults={}&children={}&infants_in_seat={}&travel_class={}&currency={}&hl={}' \
                 '&stops=1&departure_token={}' \

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['SQLALCHEMY_ECHO'] = os.getenv("SQLALCHEMY_ECHO")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = os.getenv("DEBUG_TB_INTERCEPT_REDIRECTS")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.app_context().push()

connect_db(app)
db.create_all()


@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):

    session[CURR_USER_KEY] = user.id


def do_logout():

    session_keys = [CURR_USER_KEY, "ONE_WAY_TRIP_INFO",
                    "ROUND_TRIP_DEPARTURE_INFO", "ROUND_TRIP_ARRIVAL_INFO"]
    for key in session_keys:
        if key in session:
            del session[key]


@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                name=form.name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template("login_and_signup/signup.html", form=form)

        do_login(user)
        flash("Account created successfully", "success")
        return redirect("/")

    else:
        return render_template("login_and_signup/signup.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template("login_and_signup/login.html", form=form)


@app.route('/logout')
def logout():

    flash("You logged out successfully", "success")
    do_logout()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_codes/error_code_404.html'), 404


@app.errorhandler(405)
def server_access_not_allowed(e):
    return render_template('error_codes/error_code_405.html'), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error_codes/error_code_500.html'), 500


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/round_trip_departure", methods=['GET', 'POST'])
def round_trip_departure():
    from_airport_code = request.args.get('fromAirportCode')
    to_airport_code = request.args.get('toAirportCode')
    departing_date = request.args.get('fromDate')
    arrival_date = request.args.get('toDate')
    num_adults = request.args.get('numAdults')
    num_children = request.args.get('numChildren')
    num_infants = request.args.get('numInfants')
    cabin_class = request.args.get('cabinClass')
    currency_code = request.args.get('currencyCode')
    region_code = request.args.get('regionCode')

    session["ROUND_TRIP_DEPARTURE_INFO"] = {
        "round_trip_depart_num_adults": num_adults,
        "round_trip_depart_num_children": num_children,
        "round_trip_depart_num_infants": num_infants,
        "round_trip_depart_cabin_class": cabin_class,
        "round_trip_depart_currency_code": currency_code,
        "round_trip_depart_region_code": region_code
    }

    new_url = round_trip_departure_url.format(os.getenv("FLIGHT_API_KEY"),
                                    from_airport_code,
                                    to_airport_code,
                                    departing_date,
                                    arrival_date,
                                    num_adults,
                                    num_children,
                                    num_infants,
                                    cabin_class,
                                    currency_code,
                                    region_code)
    is_response, response = round_trip_departure_form_check(
                                          new_url,
                                          from_airport_code,
                                          to_airport_code,
                                          departing_date,
                                          arrival_date,
                                          num_adults,
                                          num_children,
                                          num_infants,
                                          cabin_class,
                                          currency_code,
                                          region_code)

    if is_response and response:
        if g.user:
            return render_template("flight_options/round_trip_departure.html", response=response)
        else:
            del session["ROUND_TRIP_DEPARTURE_INFO"]
            flash("You have to log in", 'warning')
            return redirect("/")
    elif not is_response and response:
        del session["ROUND_TRIP_DEPARTURE_INFO"]
        for error in response:
            flash(error, 'danger')
        return redirect('/')


@app.route("/round_trip_arrival", methods=['GET', 'POST'])
def round_trip_arrival():
    from_airport_code = request.form.get('fromAirportCode')
    to_airport_code = request.form.get('toAirportCode')
    airline = request.form.get('airline')
    departing_date = request.form.get('fromDate')
    arrival_date = request.form.get('toDate')
    duration = request.form.get('duration')
    departure_ticket_price = request.form.get('departurePrice')
    departure_token = request.form.get('departToken')

    round_trip_depart_info_dict = {
        "round_trip_depart_from_code": from_airport_code,
        "round_trip_depart_to_code": to_airport_code,
        "round_trip_depart_airline": airline,
        "round_trip_depart_depart_date": departing_date,
        "round_trip_depart_arrive_date": arrival_date,
        "round_trip_depart_duration": duration,
        "round_trip_depart_price": departure_ticket_price
    }
    session["ROUND_TRIP_DEPARTURE_INFO"].update(
        round_trip_depart_info_dict
    )
    del round_trip_depart_info_dict

    other_url = round_trip_arrival_url.format(
        os.getenv("FLIGHT_API_KEY"),
        from_airport_code,
        to_airport_code,
        departing_date,
        arrival_date,
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_adults"],
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_children"],
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_infants"],
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_cabin_class"],
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_currency_code"],
        session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_region_code"],
        departure_token
    )

    is_response, response = round_trip_arrival_form_check(
          other_url,
          from_airport_code,
          to_airport_code,
          departing_date,
          arrival_date,
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_adults"],
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_children"],
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_infants"],
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_cabin_class"],
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_currency_code"],
          session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_region_code"],
          departure_token
    )

    if is_response and response:
        return render_template("flight_options/round_trip_arrival.html", response=response,
                               departure_info_dict=session["ROUND_TRIP_DEPARTURE_INFO"])
    elif not is_response and response:
        flash(response[0], 'danger')
        flash(response[1], 'warning')
        del session["ROUND_TRIP_DEPARTURE_INFO"]
        return redirect('/')


@app.route("/oneway_trip", methods=['GET', 'POST'])
def oneway_trip():
    oneway_depart_airport_code = request.args.get('oneWayFromAirportCode')
    oneway_arrive_airport_code = request.args.get('oneWayToAirportCode')
    oneway_departing_date = request.args.get('oneWayFromDate')
    oneway_num_adults = request.args.get('oneWayNumAdults')
    oneway_num_children= request.args.get('oneWayNumChildren')
    oneway_num_infants = request.args.get('oneWayNumInfants')
    oneway_cabin_class = request.args.get('oneWayCabinClass')
    oneway_currency_code = request.args.get('oneWayCurrencyCode')
    oneway_region_code = request.args.get('oneWayRegionCode')

    session["ONE_WAY_TRIP_INFO"] = {
        "oneway_num_adults": oneway_num_adults,
        "oneway_num_children": oneway_num_children,
        "oneway_num_infants": oneway_num_infants,
        "oneway_cabin_class": oneway_cabin_class,
        "oneway_currency_code": oneway_currency_code
    }

    new_url = oneway_trip_url.format(os.getenv("FLIGHT_API_KEY"),
                                     oneway_depart_airport_code,
                                     oneway_arrive_airport_code,
                                     oneway_departing_date,
                                     oneway_num_adults,
                                     oneway_num_children,
                                     oneway_num_infants,
                                     oneway_cabin_class,
                                     oneway_currency_code,
                                     oneway_region_code)
    is_response, response = oneway_trip_form_check(
                                          new_url,
                                          oneway_depart_airport_code,
                                          oneway_arrive_airport_code,
                                          oneway_departing_date,
                                          oneway_num_adults,
                                          oneway_num_children,
                                          oneway_num_infants,
                                          oneway_cabin_class,
                                          oneway_currency_code,
                                          oneway_region_code)

    if is_response and response:
        if g.user:
            return render_template("flight_options/oneway_trip.html", response=response)
        else:
            del session["ONE_WAY_TRIP_INFO"]
            flash("You have to log in", 'warning')
            return redirect("/")
    elif not is_response and response:
        del session["ONE_WAY_TRIP_INFO"]
        for error in response:
            flash(error, 'danger')
        return redirect('/')


@app.route("/payments/add/oneway_trip", methods=["GET", "POST"])
def oneway_trip_add_payment():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    oneway_depart_airport_code = request.form.get('oneWayFromAirportCode')
    oneway_arrive_airport_code = request.form.get('oneWayToAirportCode')
    oneway_airline = request.form.get('oneWayAirline')
    oneway_departing_date = request.form.get('oneWayFromDate')
    oneway_duration = request.form.get('oneWayDuration')
    oneway_ticket_price = request.form.get('oneWayDeparturePrice')

    oneway_depart_info_dict = {
        "oneway_depart_airport_code": oneway_depart_airport_code,
        "oneway_arrive_airport_code": oneway_arrive_airport_code,
        "oneway_airline": oneway_airline,
        "oneway_departing_date": oneway_departing_date,
        "oneway_duration": oneway_duration,
        "oneway_ticket_price": oneway_ticket_price
    }
    session["ONE_WAY_TRIP_INFO"].update(oneway_depart_info_dict)
    del oneway_depart_info_dict

    form = PaymentForm()
    if form.validate_on_submit():
        timestamp = form.timestamp.data
        payment_method = form.payment_method.data

        formatted_oneway_ticket_price = price_conversion(oneway_ticket_price, None,
                                                         session["ONE_WAY_TRIP_INFO"]["oneway_currency_code"])

        payment = OneWayTripPayment(
            oneway_trip_payment_user_id=session[CURR_USER_KEY],
            flight_departure_airport=oneway_depart_airport_code,
            flight_arrival_airport=oneway_arrive_airport_code,
            flight_airline_name=oneway_airline,
            flight_departure_timestamp=oneway_departing_date,
            flight_duration=oneway_duration,
            timestamp=timestamp,
            num_adults=session["ONE_WAY_TRIP_INFO"]["oneway_num_adults"],
            num_children=session["ONE_WAY_TRIP_INFO"]["oneway_num_children"],
            num_infants=session["ONE_WAY_TRIP_INFO"]["oneway_num_infants"],
            cabin_class=session["ONE_WAY_TRIP_INFO"]["oneway_cabin_class"],
            total_amount_paid=formatted_oneway_ticket_price,
            payment_method=payment_method
        )

        db.session.add(payment)
        db.session.commit()

        del session["ONE_WAY_TRIP_INFO"]
        return redirect(f"/oneway_trip_payments")

    return render_template("payments_and_reviews/oneway_trip_new_payment.html", form=form,
                           oneway_depart_info_dict=session["ONE_WAY_TRIP_INFO"])


@app.route("/trips")
def trips():
    if g.user:
        ticket_id = request.args.get("ticketNumber")  # Use request.args
        ticket_type = request.args.get("ticketType")  # Use request.args

        if ticket_type == "round_trip" and int(ticket_id) >= 1:

            # Get the current user ID from the session
            current_user_id = session.get(CURR_USER_KEY)

            # Filter round trip payments by user ID
            round_trip_user_payments = (
                User.query
                    .join(RoundTripPayment)
                    .filter(RoundTripPayment.round_trip_payment_user_id == current_user_id
                            and int(ticket_id) == RoundTripPayment.id)  # Filter by user ID
                    .order_by(RoundTripPayment.timestamp.desc())
                    .limit(100)
                    .all()
            )

            return render_template("payments_and_reviews/round_trip_payments.html", user=g.user,
                                   payments=round_trip_user_payments)
        elif ticket_type == "one_way" and int(ticket_id) >= 1:

            # Get the current user ID from the session
            current_user_id = session.get(CURR_USER_KEY)

            # Filter one-way trip payments by user ID
            oneway_trip_user_payments = (
                User.query
                    .join(OneWayTripPayment)
                    .filter(OneWayTripPayment.oneway_trip_payment_user_id == current_user_id
                            and int(ticket_id) == OneWayTripPayment.id)  # Filter by user ID
                    .order_by(OneWayTripPayment.timestamp.desc())
                    .limit(100)
                    .all()
            )

            return render_template("payments_and_reviews/oneway_trip_payments.html", user=g.user,
                                   payments=oneway_trip_user_payments)
        else:
            errors_list = trips_error_checking(ticket_type, ticket_id)
            for error in errors_list:
                flash(error, 'warning')
            return redirect('/')
    else:
        flash("You have to log in", 'warning')
        return redirect("/")


@app.route("/flights")
def flights():
    return render_template("newgen_navbar_links/flights.html")


@app.route("/payments")
def payments():
    if g.user:
        return render_template("newgen_navbar_links/payments.html", user=session[CURR_USER_KEY])
    else:
        flash("You have to log in", 'warning')
        return redirect("/")


@app.route("/reviews")
def reviews():
    if g.user:
        return render_template("newgen_navbar_links/reviews.html", user=session[CURR_USER_KEY])
    else:
        flash("You have to log in", 'warning')
        return redirect("/")


@app.route("/oneway_trip_payments")
def oneway_trip_payments():

    # Get the current user ID from the session
    current_user_id = session.get(CURR_USER_KEY)

    # Filter one-way trip payments by user ID
    oneway_user_payments = (
        User.query
            .join(OneWayTripPayment)
            .filter(OneWayTripPayment.oneway_trip_payment_user_id == current_user_id)  # Filter by user ID
            .order_by(OneWayTripPayment.timestamp.desc())
            .limit(100)
            .all()
    )

    return render_template("payments_and_reviews/oneway_trip_payments.html",
                           user=current_user_id, payments=oneway_user_payments)


@app.route("/round_trip_payments")
def round_trip_payments():
    # Get the current user ID from the session
    current_user_id = session.get(CURR_USER_KEY)

    # Filter round trip payments by user ID
    round_trips_booked = (
        User.query
            .join(RoundTripPayment)
            .filter(RoundTripPayment.round_trip_payment_user_id == current_user_id)  # Filter by user ID
            .order_by(RoundTripPayment.timestamp.desc())
            .limit(100)
            .all()
    )

    return render_template("payments_and_reviews/round_trip_payments.html",
                           user=current_user_id, payments=round_trips_booked)


@app.route("/payments/add/round_trip", methods=["GET", "POST"])
def round_trip_add_payment():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    arrival_from_airport_code = request.form.get('fromAirportCode')
    arrival_to_airport_code = request.form.get('toAirportCode')
    arrival_airline = request.form.get('airline')
    arrival_departing_date = request.form.get('fromDate')
    arrival_arrival_date = request.form.get('toDate')
    arrival_duration = request.form.get('duration')
    arrival_ticket_price = request.form.get('arrivalPrice')

    session["ROUND_TRIP_ARRIVAL_INFO"] = {
        "round_trip_arrival_from_code": arrival_from_airport_code,
        "round_trip_arrival_to_code": arrival_to_airport_code,
        "round_trip_arrival_airline": arrival_airline,
        "round_trip_arrival_departing_date": arrival_departing_date,
        "round_trip_arrival_duration": arrival_duration,
        "round_trip_arrival_price": arrival_ticket_price
    }

    form = PaymentForm()
    if form.validate_on_submit():
        timestamp = form.timestamp.data
        payment_method = form.payment_method.data

        formatted_round_trip_price = price_conversion(
            session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_price"],
            arrival_ticket_price,
            session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_currency_code"]
        )

        payment = RoundTripPayment(
            round_trip_payment_user_id=session[CURR_USER_KEY],
            flight_first_departure_airport=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_from_code"],
            flight_first_arrival_airport=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_to_code"],
            flight_first_airline_name=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_airline"],
            flight_first_departure_timestamp=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_depart_date"],
            flight_first_arrival_timestamp=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_arrival_date"],
            flight_first_duration=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_duration"],
            flight_last_departure_airport=arrival_from_airport_code,
            flight_last_arrival_airport=arrival_to_airport_code,
            flight_last_airline_name=arrival_airline,
            flight_last_departure_timestamp=arrival_departing_date,
            flight_last_arrival_timestamp=arrival_arrival_date,
            flight_last_duration=arrival_duration,
            timestamp=timestamp,
            num_adults=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_adults"],
            num_children=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_children"],
            num_infants=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_infants"],
            cabin_class=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_cabin_class"],
            total_amount_paid=formatted_round_trip_price,
            payment_method=payment_method
        )

        db.session.add(payment)
        db.session.commit()

        del session["ROUND_TRIP_DEPARTURE_INFO"]
        del session["ROUND_TRIP_ARRIVAL_INFO"]
        return redirect(f"/round_trip_payments")

    return render_template("payments_and_reviews/round_trip_new_payment.html", form=form,
                           departure_info_dict=session["ROUND_TRIP_DEPARTURE_INFO"],
                           arrival_info_dict=session["ROUND_TRIP_ARRIVAL_INFO"])


@app.route("/oneway_trip_reviews")
def oneway_trip_reviews():

    # Get the current user ID from the session
    current_user_id = session.get(CURR_USER_KEY)

    # Filter the query by user ID
    user_reviews = (
        User.query
            .join(OneWayTripPayment)
            .join(OneWayTripReview)
            .filter(OneWayTripPayment.oneway_trip_payment_user_id == current_user_id)  # Filter by user ID
            .with_entities(
                OneWayTripPayment.timestamp,
                OneWayTripReview.rating,
                OneWayTripReview.review,
                OneWayTripReview.timestamp
            )
            .order_by(OneWayTripReview.timestamp.desc())
            .limit(100)
            .all()
    )

    return render_template("payments_and_reviews/oneway_trip_reviews.html",
                           user=current_user_id, reviews=user_reviews)  # Pass user ID as well


@app.route("/oneway_trip_reviews/add/<int:payment_id>", methods=["GET", "POST"])
def oneway_trip_add_review(payment_id):
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    form = OneWayTripReviewForm()
    if form.validate_on_submit():
        oneway_trip_review_payment_id = payment_id
        rating = form.rating.data
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

        return redirect(f"/oneway_trip_reviews")

    return render_template("payments_and_reviews/oneway_trip_new_review.html", form=form)


@app.route('/oneway_trip_reviews/<int:review_id>/delete', methods=["POST"])
def oneway_trip_reviews_destroy(review_id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = OneWayTripReview.query.get(review_id)
    db.session.delete(review)
    db.session.commit()

    return redirect(f"/oneway_trip_reviews")


@app.route('/oneway_trip_reviews/<int:review_id>/edit',
           methods=["GET", "POST"])
def oneway_trip_reviews_update(review_id):
    """Update profile for current user."""

    # IMPLEMENT THIS
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = OneWayTripReviewForm()
    review_to_update = OneWayTripReview.query.get(review_id)

    if form.validate_on_submit():
        review_to_update.oneway_trip_review_payment_id = form.oneway_trip_review_payment_id.data
        review_to_update.rating = form.rating.data
        review_to_update.review = form.review.data
        review_to_update.timestamp = form.timestamp.data

        db.session.commit()
        return redirect(f"/oneway_trip_reviews")

    else:
        flash("Invalid credentials.", 'danger')
        return render_template("/")


@app.route("/round_trip_reviews")
def round_trip_reviews():
    # Get the current user ID from the session
    current_user_id = session.get(CURR_USER_KEY)

    # Filter the query by user ID
    user_reviews = (
        User.query
            .join(RoundTripPayment)
            .join(RoundTripReview)
            .filter(RoundTripPayment.round_trip_payment_user_id == current_user_id)  # Filter by user ID
            .with_entities(
            RoundTripPayment.timestamp,
            RoundTripReview.rating,
            RoundTripReview.review,
            RoundTripReview.timestamp
        )
            .order_by(RoundTripReview.timestamp.desc())
            .limit(100)
            .all()
    )

    return render_template("payments_and_reviews/round_trip_reviews.html",
                           user=current_user_id, reviews=user_reviews)  # Pass user ID as well


@app.route("/round_trip_reviews/add/<int:payment_id>", methods=["GET", "POST"])
def add_round_trip_review(payment_id):
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    form = RoundTripReviewForm()
    if form.validate_on_submit():
        round_trip_review_payment_id = payment_id
        rating = form.rating.data
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

        return redirect(f"/round_trip_reviews")

    return render_template("payments_and_reviews/round_trip_new_review.html", form=form)


@app.route('/round_trip_reviews/<int:review_id>/delete', methods=["POST"])
def round_trip_reviews_destroy(review_id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = RoundTripReview.query.get(review_id)
    db.session.delete(review)
    db.session.commit()

    return redirect(f"/round_trip_reviews")


@app.route('/round_trip_reviews/<int:review_id>/edit',
           methods=["GET", "POST"])
def round_trip_reviews_update(review_id):
    """Update profile for current user."""

    # IMPLEMENT THIS
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = RoundTripReviewForm()
    review_to_update = RoundTripReview.query.get(review_id)

    if form.validate_on_submit():
        review_to_update.round_trip_review_payment_id = form.round_trip_review_payment_id.data
        review_to_update.rating = form.rating.data
        review_to_update.review = form.review.data
        review_to_update.timestamp = form.timestamp.data

        db.session.commit()
        return redirect(f"/round_trip_reviews")

    else:
        flash("Invalid credentials.", 'danger')
        return render_template("/")


@app.route("/login_signup")
def login_signup():
    return render_template("login_and_signup/login_signup.html")


@app.route("/airport_rules")
def airport_rules():
    return render_template("newgen_travel_options/airport_rules.html")


@app.route("/boarding_pass")
def boarding_pass():
    return render_template("newgen_travel_options/boarding_pass.html")


@app.route("/bags")
def bags():
    return render_template("newgen_travel_options/bags.html")


@app.route("/special_assistance")
def special_assistance():
    return render_template("newgen_travel_options/special_assistance.html")


@app.route("/contact_newgen")
def contact_newgen():
    return render_template("newgen_footer_links/contact_newgen.html")


@app.route("/faq")
def faq():
    return render_template("newgen_footer_links/faq.html")


@app.route("/receipts_refunds")
def receipts_refunds():
    return render_template("newgen_footer_links/receipts_refunds.html")


@app.route("/terms_and_conditions")
def terms_and_conditions():
    return render_template("newgen_footer_links/terms_and_conditions.html")


@app.route("/business_programs")
def business_programs():
    return render_template("newgen_footer_links/business_programs.html")


@app.route("/trip_insurance")
def trip_insurance():
    return render_template("newgen_footer_links/trip_insurance.html")


@app.after_request
def add_header(req):

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

