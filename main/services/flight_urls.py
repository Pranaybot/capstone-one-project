# main/services/flight_urls.py

class FlightURLs:
    @staticmethod
    def oneway_trip(api_key, departure_id, arrival_id, outbound_date, adults, children, infants_in_seat, travel_class,
                    currency, hl):
        return ('https://serpapi.com/search.json?engine=google_flights&api_key={}' 
                '&type=2&departure_id={}&arrival_id={}&outbound_date={}&adults={}' 
                '&children={}&infants_in_seat={}&travel_class={}&currency={}&hl={}' 
                '&stops=1').format(api_key, departure_id, arrival_id, outbound_date, adults, children, infants_in_seat,
                                   travel_class, currency, hl)

    @staticmethod
    def round_trip_departure(api_key, departure_id, arrival_id, outbound_date, return_date, adults, children,
                             infants_in_seat, travel_class, currency, hl):
        return ('https://serpapi.com/search.json?engine=google_flights&api_key={}&' 
                'departure_id={}&arrival_id={}&outbound_date={}&return_date={}&' 
                'adults={}&children={}&infants_in_seat={}&travel_class={}'
                '&currency={}&hl={}&stops=1').format(
            api_key, departure_id, arrival_id, outbound_date, return_date, adults, children, infants_in_seat,
            travel_class, currency, hl)

    @staticmethod
    def round_trip_arrival(api_key, departure_id, arrival_id, outbound_date, return_date, adults, children,
                           infants_in_seat, travel_class, currency, hl, departure_token):
        return ('https://serpapi.com/search.json?engine=google_flights&api_key={}&' 
                'departure_id={}&arrival_id={}&outbound_date={}&return_date={}&' 
                'adults={}&children={}&infants_in_seat={}&travel_class={}&currency={}&hl={}' 
                '&departure_token={}&stops=1').format(api_key, departure_id, arrival_id, outbound_date, return_date,
                                                      adults, children, infants_in_seat, travel_class, currency, hl,
                                                      departure_token)
