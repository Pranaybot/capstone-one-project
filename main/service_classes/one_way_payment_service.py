from main.extensions.connect_db import db
from main.models import OneWayTripPayment
from sqlalchemy import and_


class OneWayPaymentService:

    def add_one_way_payment(user_id, data, timestamp,
                            oneway_depart_info_dict,
                            ticket_price, payment_method):

        payment = OneWayTripPayment(
            oneway_trip_payment_user_id=user_id,
            flight_departure_airport=data.get('oneWayFromAirportName'),
            flight_arrival_airport=data.get('oneWayToAirportName'),
            flight_airline_name=data.get('oneWayAirline'),
            flight_departure_timestamp=data.get('oneWayFromDate'),
            flight_duration=format(float(data.get('oneWayDuration')), ".2f"),
            timestamp=timestamp,
            num_adults=int(oneway_depart_info_dict["oneway_num_adults"]),
            num_children=int(oneway_depart_info_dict["oneway_num_children"]),
            num_infants=int(oneway_depart_info_dict["oneway_num_infants"]),
            cabin_class=oneway_depart_info_dict["oneway_cabin_class"],
            total_amount_paid=ticket_price,
            payment_method=payment_method
        )

        db.session.add(payment)
        db.session.commit()

    def get_one_way_payments(user_id):

        # Get the current user ID from the session
        current_user_id = user_id

        # Filter one-way trip payments by user ID
        oneway_user_payments = (
            OneWayTripPayment.query
                .filter(OneWayTripPayment.oneway_trip_payment_user_id == current_user_id)  # Filter by user ID
                .order_by(OneWayTripPayment.timestamp.desc())
                .limit(100)
                .all()
        )

        return oneway_user_payments

    def get_one_way_payment(user_id, ticket_id):
        # Get the current user ID from the session
        current_user_id = user_id

        # Filter one-way trip payments by user ID and ticket ID
        oneway_trip_user_payment = (
            OneWayTripPayment.query
                .filter(and_(
                    OneWayTripPayment.oneway_trip_payment_user_id == current_user_id,
                    OneWayTripPayment.id == int(ticket_id)
                ))  # Filter by user ID
                .order_by(OneWayTripPayment.timestamp.desc())
                .limit(100)
                .all()
        )

        return oneway_trip_user_payment
