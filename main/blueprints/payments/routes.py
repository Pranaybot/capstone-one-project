from flask import render_template, \
    redirect, request, flash, url_for, session, g, current_app
from main.utils import final_update_session_oneway_trip, update_session_round_trip_arrival
from main.forms import PaymentForm
from main.blueprints.payments.data_check.currency_code_conversion import price_conversion
from main.blueprints.payments.data_check.trips_error_checking import trips_error_checking
from main.service_classes.one_way_payment_service import OneWayPaymentService
from main.service_classes.round_trip_payment_service import RoundTripPaymentService
import ast
from . import payments_bp


@payments_bp.route("/payments/add/oneway_trip", methods=["GET", "POST"])
def oneway_trip_add_payment():

    departure_airport = request.args.get('oneWayFromAirportCode')
    arrival_airport = request.args.get('oneWayToAirportCode')
    departure_airport_name = request.args.get('oneWayFromAirportName')
    arrival_airport_name = request.args.get('oneWayToAirportName')
    departure_date = request.args.get('oneWayFromDate')
    airline = request.args.get('oneWayAirline')
    duration = request.args.get('oneWayDuration')
    ticket_price = request.args.get('oneWayDeparturePrice')

    final_update_session_oneway_trip(departure_airport, arrival_airport, departure_airport_name,
                                     arrival_airport_name, airline, departure_date, duration, ticket_price)

    form = PaymentForm()
    if form.validate_on_submit():
        timestamp = form.timestamp.data
        payment_method = form.payment_method.data

        formatted_oneway_ticket_price = price_conversion(ticket_price, None,
                                                         session["ONEWAY_TRIP_INFO"]["oneway_currency_code"])

        OneWayPaymentService.add_one_way_payment(session[current_app.config['CURR_USER_KEY']], request.args,
                                                 timestamp, session["ONEWAY_TRIP_INFO"],
                                                 formatted_oneway_ticket_price, payment_method)

        del session["ONEWAY_TRIP_INFO"]
        return redirect(f"/oneway_trip_payments")

    return render_template("oneway_trip_new_payment.html", form=form,
                           oneway_depart_info_dict=session["ONEWAY_TRIP_INFO"])


@payments_bp.route("/trips")
def trips():
    if g.user:
        ticket_id = request.args.get("ticketNumber")  # Use request.args
        ticket_type = request.args.get("ticketType")  # Use request.args

        if ticket_type == "round_trip" and int(ticket_id) >= 1:

            payment = RoundTripPaymentService.get_round_trip_payment(session[current_app.config['CURR_USER_KEY']],
                                                                       ticket_id)

            if len(payment) == 1:
                return render_template("round_trip_payments.html", payments=payment)
            else:
                flash("You entered the wrong round_trip_id", 'warning')
                return redirect("/")
        elif ticket_type == "one_way" and int(ticket_id) >= 1:

            payment = OneWayPaymentService.get_one_way_payment(session[current_app.config['CURR_USER_KEY']],
                                                                ticket_id)

            if len(payment) == 1:
                return render_template("oneway_trip_payments.html", payments=payment)
            else:
                flash("You entered the wrong oneway_trip_id", 'warning')
                return redirect("/")
        else:
            errors_list = trips_error_checking(ticket_type, ticket_id)
            for error in errors_list:
                flash(error, 'warning')
            return redirect('/')
    else:
        flash("You have to log in", 'warning')
        return redirect("/")


@payments_bp.route("/oneway_trip_payments")
def oneway_trip_payments():

    payments = OneWayPaymentService.get_one_way_payments(session[current_app.config['CURR_USER_KEY']])

    return render_template("oneway_trip_payments.html", payments=payments)


@payments_bp.route("/round_trip_payments")
def round_trip_payments():

    payments = RoundTripPaymentService.get_round_trip_payments(session[current_app.config['CURR_USER_KEY']])

    return render_template("round_trip_payments.html", payments=payments)


@payments_bp.route("/payments/add/round_trip", methods=["GET", "POST"])
def round_trip_add_payment():

    departure_airport = request.args.get('fromAirportCode')
    arrival_airport = request.args.get('toAirportCode')
    departure_airport_name = request.args.get('fromAirportName')
    arrival_airport_name = request.args.get('toAirportName')
    airline = request.args.get('airline')
    duration = request.args.get('duration')
    departure_dict = ast.literal_eval(request.args.get('departureDict'))
    arrival_ticket_price = request.args.get('arrivalPrice')

    update_session_round_trip_arrival(departure_airport, arrival_airport, departure_airport_name,
                                      arrival_airport_name, airline, duration, arrival_ticket_price)

    form = PaymentForm()
    if form.validate_on_submit():
        timestamp = form.timestamp.data
        payment_method = form.payment_method.data

        formatted_round_trip_price = price_conversion(
            departure_dict["round_trip_depart_price"],
            arrival_ticket_price,
            departure_dict["round_trip_depart_currency_code"]
        )

        RoundTripPaymentService.add_round_trip_payment(session[current_app.config['CURR_USER_KEY']], request.args,
                                                       timestamp, departure_dict,
                                                       formatted_round_trip_price, payment_method,
                                                       flight_arrival_date=session["ROUND_TRIP_ARRIVAL_INFO"]
                                                       ["round_trip_arrival_date"])

        del departure_dict
        del session["ROUND_TRIP_DEPARTURE_INFO"]
        del session["ROUND_TRIP_ARRIVAL_INFO"]
        return redirect(f"/round_trip_payments")

    return render_template("round_trip_new_payment.html", form=form,
                           departure_info_dict=departure_dict,
                           arrival_info_dict=session["ROUND_TRIP_ARRIVAL_INFO"])
