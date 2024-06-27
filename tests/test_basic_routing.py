from app import create_app
from unittest import TestCase


class BasicRouting(TestCase):

    def test_index_page(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_different_page(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/flights')
            self.assertEqual(response.status_code, 200)

    def test_page_with_content(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/faq')
            html = response.get_data(as_text=True)

            self.assertIn('<h3>Need extra help? Contact us.</h3>', html)

    def test_page_without_error(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/airport_rules')
            self.assertNotEqual(response.status_code, 404)

    def test_unknown_page(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/cats_are_cool')
            self.assertEqual(response.status_code, 404)

    def test_flight_form_with_wrong_http_request(self):
        app = create_app()
        with app.test_client() as client:
            response = client.post('/oneway_trip',
                                  data={'oneWayFromAirportCode': 'DTW',
                                        'oneWayToAirportCode': 'MCO',
                                        'oneWayFromDate': '2024-07-10',
                                        'oneWayNumAdults': '1',
                                        'oneWayNumChildren': '1',
                                        'oneWayNumInfants': '1',
                                        'oneWayCabinClass': '2',
                                        'oneWayCurrencyCode': 'USD',
                                        'oneWayRegionCode': ''})
            self.assertEqual(response.status_code, 405)


    def test_internal_server_error(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get('/round_trip_departure',
                                   data={'fromAirportCode': 'DTW',
                                         'toAirportCode': 'MCO',
                                         'fromDate': '2024-07-10',
                                         'toDate': '2024-07-14',
                                         'numAdults': '1',
                                         'numChildren': '1',
                                         'numInfants': '1',
                                         'cabinClass': '2',
                                         'currencyCode': 'USD',
                                         'regionCode': ''})
            self.assertEqual(response.status_code, 500)




