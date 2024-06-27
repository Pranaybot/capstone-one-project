from flask import Blueprint, render_template, redirect, \
    request, url_for, flash, session, g, current_app
from main.blueprints.flight_options.flight_form_check import oneway_trip_form_check, \
    round_trip_departure_form_check, round_trip_arrival_form_check
from main.utils import initial_update_session_round_trip_depart, final_update_session_round_trip_depart, \
    initial_update_session_oneway_trip
from . import flight_options_bp


@flight_options_bp.route("/round_trip_departure", methods=['GET'])
def round_trip_departure():
    departure_airport = request.args.get('fromAirportCode')
    arrival_airport = request.args.get('toAirportCode')
    departure_date = request.args.get('fromDate')
    arrival_date = request.args.get('toDate')
    num_adults = request.args.get('numAdults')
    num_children = request.args.get('numChildren')
    num_infants = request.args.get('numInfants')
    cabin_class = request.args.get('cabinClass')
    currency_code = request.args.get('currencyCode')
    region_code = request.args.get('regionCode')

    initial_update_session_round_trip_depart(num_adults, num_children, num_infants,
                                             cabin_class, currency_code, region_code,
                                             departure_date, arrival_date)

    is_response, response = round_trip_departure_form_check(current_app.config['FLIGHT_API_KEY'], departure_airport,
                                                            arrival_airport, departure_date, arrival_date, num_adults,
                                                            num_children, num_infants, cabin_class, currency_code,
                                                            region_code)

    if is_response and response:
        if g.user:
            return render_template("round_trip_departure.html",
                response=response, depart_date=session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_date"])
        else:
            del session["ROUND_TRIP_DEPARTURE_INFO"]
            flash("You have to log in", 'warning')
            return redirect("/")
    elif not is_response and response:
        del session["ROUND_TRIP_DEPARTURE_INFO"]
        for error in response:
            flash(error, 'danger')
        return redirect('/')


@flight_options_bp.route("/round_trip_arrival", methods=['GET'])
def round_trip_arrival():
    departure_airport = request.args.get('fromAirportCode')
    arrival_airport = request.args.get('toAirportCode')
    departure_airport_name = request.args.get('fromAirportName')
    arrival_airport_name = request.args.get('toAirportName')
    departure_date = request.args.get('fromDate')
    arrival_date = session["ROUND_TRIP_ARRIVAL_INFO"]["round_trip_arrival_date"]
    airline = request.args.get('airline')
    duration = request.args.get('duration')
    ticket_price = request.args.get('departurePrice')
    departure_token = request.args.get('departToken')

    final_update_session_round_trip_depart(departure_airport, departure_airport_name,
                                           arrival_airport, arrival_airport_name,
                                           airline, duration, ticket_price)

    is_response, response = round_trip_arrival_form_check(current_app.config['FLIGHT_API_KEY'],
                                      departure_airport, arrival_airport, departure_date, arrival_date,
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_adults"],
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_children"],
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_num_infants"],
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_cabin_class"],
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_currency_code"],
                                      session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_region_code"],
                                      departure_token)

    if is_response and response:
        return render_template("round_trip_arrival.html", response=response,
                               departure_info_dict=session["ROUND_TRIP_DEPARTURE_INFO"],
                               arrival_date=arrival_date)
    elif not is_response and response:
        del session["ROUND_TRIP_DEPARTURE_INFO"]
        for error in response:
            flash(error, 'danger')
        return redirect('/')


@flight_options_bp.route("/oneway_trip", methods=['GET'])
def oneway_trip():
    departure_airport = request.args.get('oneWayFromAirportCode')
    arrival_airport = request.args.get('oneWayToAirportCode')
    departure_date = request.args.get('oneWayFromDate')
    num_adults = request.args.get('oneWayNumAdults')
    num_children = request.args.get('oneWayNumChildren')
    num_infants = request.args.get('oneWayNumInfants')
    cabin_class = request.args.get('oneWayCabinClass')
    currency_code = request.args.get('oneWayCurrencyCode')
    region_code = request.args.get('oneWayRegionCode')

    initial_update_session_oneway_trip(num_adults, num_children,
                                       num_infants, cabin_class,
                                       currency_code)

    is_response, response = oneway_trip_form_check(current_app.config['FLIGHT_API_KEY'], departure_airport,
                                                   arrival_airport, departure_date, num_adults, num_children,
                                                   num_infants, cabin_class, currency_code, region_code)

    if is_response and response:
        if g.user:
            return render_template("oneway_trip.html", response=response)
        else:
            del session["ONEWAY_TRIP_INFO"]
            flash("You have to log in", 'warning')
            return redirect("/")
    elif not is_response and response:
        del session["ONEWAY_TRIP_INFO"]
        for error in response:
            flash(error, 'danger')
        return redirect('/')