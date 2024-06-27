from app import create_app
from unittest import TestCase
from main.blueprints.payments.data_check.trips_error_checking import trips_error_checking

class TripsErrorCheck(TestCase):

    def test_trips_error_search_success(self):
        app = create_app()
        with app.test_client() as client:
            error_check = trips_error_checking("round_trip", "2.0")
            self.assertEqual(len(error_check), 1)

    def test_trips_error_search_failure(self):
        app = create_app()
        with app.test_client() as client:
            error_check = trips_error_checking("round_trip", "5")
            self.assertEqual(len(error_check), 0)

    def test_trips_error_values_first_case(self):
        app = create_app()
        with app.test_client() as client:
            error_check = trips_error_checking(1, "5")
            self.assertIn('The ticket type: 1 must be a string value', error_check[0])
            self.assertIn('The ticket type: 1 is not "round_trip" or "one_way"', error_check[1])

    def test_trips_error_values_second_case(self):
        app = create_app()
        with app.test_client() as client:
            error_check = trips_error_checking("one_way", "5.091")
            self.assertIn('The ticket id: 5.091 is invalid. It must be a number greater than or '
                          'equal to 1', error_check[0])

    def test_trips_error_values_both_cases(self):
        app = create_app()
        with app.test_client() as client:
            error_check = trips_error_checking("R", "5.091")
            self.assertIn('The ticket type: R is not "round_trip" or "one_way', error_check[0])
            self.assertIn('The ticket id: 5.091 is invalid. It must be a number greater than or '
                          'equal to 1', error_check[1])