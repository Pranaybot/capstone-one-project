from main.extensions.connect_db import db
from main.models import RoundTripPayment
from sqlalchemy import and_


class RoundTripPaymentService:

    def add_round_trip_payment(user_id, data, timestamp,
                            round_trip_depart_info_dict,
                            ticket_price, payment_method,
                            flight_arrival_date):

        payment = RoundTripPayment(
            round_trip_payment_user_id=user_id,
            flight_first_departure_airport=round_trip_depart_info_dict["round_trip_depart_from_name"],
            flight_first_arrival_airport=round_trip_depart_info_dict["round_trip_depart_to_name"],
            flight_first_airline_name=round_trip_depart_info_dict["round_trip_depart_airline"],
            flight_departure_date=round_trip_depart_info_dict["round_trip_depart_date"],
            flight_first_duration=format(float(round_trip_depart_info_dict["round_trip_depart_duration"]), ".2f"),
            flight_last_departure_airport=data.get('fromAirportName'),
            flight_last_arrival_airport=data.get('toAirportName'),
            flight_last_airline_name=data.get('airline'),
            flight_arrival_date=flight_arrival_date,
            flight_last_duration=format(float(data.get('duration')), ".2f"),
            timestamp=timestamp,
            num_adults=int(round_trip_depart_info_dict["round_trip_depart_num_adults"]),
            num_children=int(round_trip_depart_info_dict["round_trip_depart_num_children"]),
            num_infants=int(round_trip_depart_info_dict["round_trip_depart_num_infants"]),
            cabin_class=round_trip_depart_info_dict["round_trip_depart_cabin_class"],
            total_amount_paid=ticket_price,
            payment_method=payment_method
        )

        db.session.add(payment)
        db.session.commit()

    def get_round_trip_payments(user_id):
        # Get the current user ID from the session
        current_user_id = user_id

        # Filter round trip payments by user ID
        round_trips_booked = (
            RoundTripPayment.query
                .filter(RoundTripPayment.round_trip_payment_user_id == current_user_id)  # Filter by user ID
                .order_by(RoundTripPayment.timestamp.desc())
                .limit(100)
                .all()
        )

        return round_trips_booked

    def get_round_trip_payment(user_id, ticket_id):
        # Get the current user ID from the session
        current_user_id = user_id

        # Filter round trip payments by user ID and ticket ID
        round_trip_user_payment = (
            RoundTripPayment.query
                .filter(and_(
                    RoundTripPayment.round_trip_payment_user_id == current_user_id,
                    RoundTripPayment.id == int(ticket_id)
                ))  # Filter by user ID
                .order_by(RoundTripPayment.timestamp.desc())
                .limit(100)
                .all()
        )

        return round_trip_user_payment
