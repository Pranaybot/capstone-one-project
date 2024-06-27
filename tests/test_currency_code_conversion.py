from app import create_app
from unittest import TestCase
from main.blueprints.payments.data_check import price_conversion


class CurrencyConversion(TestCase):

    def test_currency_conversion_success(self):
        app = create_app()
        with app.test_client() as client:
            currency_conversion = price_conversion('132', '95',
                                                   'USD')
            self.assertEqual(currency_conversion, '$227.0')

    def test_currency_conversion_failure(self):
        app = create_app()
        with app.test_client() as client:
            currency_conversion = price_conversion('132', '95',
                                                   'USD')
            self.assertNotEqual(currency_conversion, '£227.0')

    def test_currency_conversion_incorrect_total_price(self):
        app = create_app()
        with app.test_client() as client:
            currency_conversion = price_conversion('600', '150',
                                                   'USD')
            self.assertNotEqual(currency_conversion, '$1400.0')

    def test_currency_conversion_with_first_price_only(self):
        app = create_app()
        with app.test_client() as client:
            currency_conversion = price_conversion('600', None,
                                                   'USD')
            self.assertEqual(currency_conversion, '$600.0')