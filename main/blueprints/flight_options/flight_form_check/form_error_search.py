import re


def form_error_search(departing_date, arrival_date, cabin_class,
                      currency_code, from_airport_code, to_airport_code):

    errors_list = []

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', departing_date):
        errors_list.append("Not a valid date format: {}".format(departing_date))
    if arrival_date:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', arrival_date):
            errors_list.append("Not a valid date format: {}".format(arrival_date))
    if int(cabin_class) not in [1, 2, 3, 4]:
        errors_list.append("Not a valid cabin_class :{}".
                           format(cabin_class))
    if not re.match(r"[A-Z]{3}", currency_code):
        errors_list.append("Not a valid currency code: {}".
                           format(currency_code))
    if not re.match(r'^[A-Z]{3}$', from_airport_code):
        errors_list.append("Not a valid departure airport code: {}".
                           format(from_airport_code))
    if not re.match(r'^[A-Z]{3}$', to_airport_code):
        errors_list.append("Not a valid arrival airport code: {}".
                           format(to_airport_code))

    return errors_list
