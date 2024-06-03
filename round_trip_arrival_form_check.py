import re
import requests


def round_trip_arrival_form_check(response, from_airport_code, to_airport_code,
                        departing_date, arrival_date, num_adults,
                        num_children, num_infants, cabin_class,
                        currency_code, region_code, departure_token):

    errors_list = []

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", departing_date):
        errors_list.append("Not a valid date format: {}".format(departing_date))
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", arrival_date):
        errors_list.append("Not a valid date format: {}".format(arrival_date))
    if int(cabin_class) not in [1, 2, 3, 4]:
        errors_list.append("Not a valid cabin_class :{}".
                           format(cabin_class))
    if not re.match(r"[A-Z]{3}", currency_code):
        errors_list.append("Not a valid currency code: {}".
                           format(currency_code))
    if not re.match(r"[A-Z]{3}", from_airport_code):
        errors_list.append("Not a valid departure airport code: {}".
                           format(from_airport_code))
    if not re.match(r"[A-Z]{3}", to_airport_code):
        errors_list.append("Not a valid arrival airport code: {}".
                           format(to_airport_code))

    if len(errors_list) > 0:
        return False, errors_list
    else:
        form_data = requests.get(url=response)
        if form_data.status_code == 200:
            form_data_json = form_data.json()
            if len(form_data_json) == 0:
                errors_list.append("No arrival flights found from search.")
                errors_list.append("Please fill out round trip form with different information.")
                return False, errors_list
            else:
                return True, form_data_json["best_flights"]
        else:
            errors_list.append("Error retrieving api data")
            return False, errors_list



