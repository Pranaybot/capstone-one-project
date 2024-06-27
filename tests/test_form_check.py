from app import create_app
from unittest import TestCase
from main.blueprints.flight_options.flight_form_check import form_error_search


class FormCheck(TestCase):

    def test_form_error_search_success(self):
        app = create_app()
        with app.test_client() as client:
            error_check = form_error_search('2024-06-18', '2024-07-21',
                                           '10', 'DZ', 'MCO',
                                           'MCOD')
            self.assertEqual(len(error_check), 3)

    def test_form_error_search_failure(self):
        app = create_app()
        with app.test_client() as client:
            error_check = form_error_search('2024-06-18', '2024-07-21',
                                           '1', 'DZA', 'MCO',
                                           'LAX')
            self.assertEqual(len(error_check), 0)

    def test_form_error_invalid_values(self):
        app = create_app()
        with app.test_client() as client:
            error_check = form_error_search('2024-06-18', '07/05/2024',
                                           '10', 'A', 'MCO',
                                           'DTW')
            self.assertIn('07/05/2024', error_check[0])
            self.assertIn('A', error_check[2])

    def test_form_error_date_separator_check(self):
        app = create_app()
        with app.test_client() as client:
            error_check = form_error_search('2024-07-18', '2024/07-18',
                                           '1', 'USD', 'MCO',
                                           'DTW')

            self.assertIn('-', error_check[0])
            self.assertIn('/', error_check[0])

    def test_form_error_arrival_date_check(self):
        app = create_app()
        with app.test_client() as client:
            error_check = form_error_search('7-3-2024', None,
                                            '-2', 'USD', 'M',
                                            'D')

            self.assertNotRegex(r'^\d{4}-\d{2}-\d{2}$', error_check[1])

