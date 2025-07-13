from django.test import TestCase
from products.utils import *

class TestDateFormatter(TestCase):
    def test_date_formatter_converts_csv_date_to_date_object(self):
            self.assertEqual(format_date('2/20/2025'), datetime.strptime('2025-02-20', '%Y-%m-%d'))

class TestPriceConverter(TestCase):
    def test_price_formatter_converts_csv_price_to_float(self):
        self.assertEqual(convert_price_to_float('$1.49'), 1.49)

class TestUnitValidator(TestCase):
    def test_unit_validator_raises_exception_if_unit_is_invalid(self):
        with self.assertRaises(ValueError):
            validate_unit('some invalid unit')

    def test_unit_validator_raises_exception_if_unit_is_wrong_case(self):
        with self.assertRaises(ValueError):
            validate_unit('Lb')

    def test_unit_validator_accepts_unit_of_lb(self):
        self.assertEqual(validate_unit('lb'), None)

    def test_unit_validator_accepts_unit_of_oz(self):
        self.assertEqual(validate_unit('oz'), None)

    def test_unit_validator_accepts_unit_of_gal(self):
        self.assertEqual(validate_unit('gal'), None)

    def test_unit_validator_accepts_unit_of_ea(self):
        self.assertEqual(validate_unit('ea'), None)   

    def test_unit_validator_accepts_unit_of_g(self):
        self.assertEqual(validate_unit('g'), None)

    def test_unit_validator_accepts_unit_of_kg(self):
        self.assertEqual(validate_unit('kg'), None)

    def test_unit_validator_accepts_unit_of_ml(self):
        self.assertEqual(validate_unit('ml'), None)

    def test_unit_validator_accepts_unit_of_l(self):
        self.assertEqual(validate_unit('l'), None)


