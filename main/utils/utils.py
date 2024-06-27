# main/utils/session_utils.py
from flask import session


def initial_update_session_round_trip_depart(num_adults, num_children, num_infants,
                                             cabin_class, currency_code, region_code,
                                             departure_date, arrival_date):

    session["ROUND_TRIP_DEPARTURE_INFO"] = {
        "round_trip_depart_date": departure_date,
        "round_trip_depart_num_adults": num_adults,
        "round_trip_depart_num_children": num_children,
        "round_trip_depart_num_infants": num_infants,
        "round_trip_depart_cabin_class": cabin_class,
        "round_trip_depart_currency_code": currency_code,
        "round_trip_depart_region_code": region_code
    }

    session["ROUND_TRIP_ARRIVAL_INFO"] = {
        "round_trip_arrival_date": arrival_date
    }


def final_update_session_round_trip_depart(departure_airport, departure_airport_name,
                                           arrival_airport, arrival_airport_name,
                                           airline, duration, ticket_price):

    session["ROUND_TRIP_DEPARTURE_INFO"].update({
        "round_trip_depart_from_code": departure_airport,
        "round_trip_depart_to_code": arrival_airport,
        "round_trip_depart_from_name": departure_airport_name,
        "round_trip_depart_to_name": arrival_airport_name,
        "round_trip_depart_airline": airline,
        "round_trip_depart_duration": duration,
        "round_trip_depart_price": ticket_price
    })


def initial_update_session_oneway_trip(num_adults, num_children, num_infants, cabin_class, currency_code):

    session["ONEWAY_TRIP_INFO"] = {
        "oneway_num_adults": num_adults,
        "oneway_num_children": num_children,
        "oneway_num_infants": num_infants,
        "oneway_cabin_class": cabin_class,
        "oneway_currency_code": currency_code
    }


def final_update_session_oneway_trip(departure_airport, arrival_airport, departure_airport_name,
                                     arrival_airport_name, airline, departure_date, duration, ticket_price):

    session["ONEWAY_TRIP_INFO"].update({
        "oneway_depart_airport_code": departure_airport,
        "oneway_arrive_airport_code": arrival_airport,
        "oneway_depart_airport_name": departure_airport_name,
        "oneway_arrive_airport_name": arrival_airport_name,
        "oneway_airline": airline,
        "oneway_departing_date": departure_date,
        "oneway_duration": duration,
        "oneway_ticket_price": ticket_price
    })


def update_session_round_trip_arrival(departure_airport, arrival_airport, departure_airport_name,
                                      arrival_airport_name, airline, duration, arrival_ticket_price):

    session["ROUND_TRIP_ARRIVAL_INFO"].update({
        "round_trip_arrival_from_code": departure_airport,
        "round_trip_arrival_to_code": arrival_airport,
        "round_trip_arrival_from_name": departure_airport_name,
        "round_trip_arrival_to_name": arrival_airport_name,
        "round_trip_arrival_airline": airline,
        "round_trip_arrival_duration": duration,
        "round_trip_arrival_price": arrival_ticket_price
    })

    del session["ROUND_TRIP_DEPARTURE_INFO"]["round_trip_depart_region_code"]




