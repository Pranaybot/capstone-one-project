import requests
from main.services.flight_urls import FlightURLs
from main.blueprints.flight_options.flight_form_check.form_error_search import form_error_search


def round_trip_arrival_form_check(api_key, from_airport_code, to_airport_code,
                        departing_date, arrival_date, num_adults,
                        num_children, num_infants, cabin_class,
                        currency_code, region_code, departure_token):

    errors_list = form_error_search(departing_date, arrival_date, cabin_class,
                      currency_code, from_airport_code, to_airport_code)

    if len(errors_list) > 0:
        return False, errors_list
    else:
        round_trip_arrival_url = FlightURLs.round_trip_arrival(api_key, from_airport_code, to_airport_code,
                                                               departing_date, arrival_date, num_adults,
                                                               num_children, num_infants, cabin_class,
                                                               currency_code, region_code, departure_token)

        form_data = requests.get(url=round_trip_arrival_url)
        if form_data.status_code == 200:
            form_data_json = form_data.json()
            if len(form_data_json) == 0:
                errors_list.append("No arrival flights found from search.")
                errors_list.append("Please fill out round trip form with different information.")
                return False, errors_list
            else:
                return True, form_data_json
        else:
            errors_list.append("Error retrieving api data")
            return False, errors_list



