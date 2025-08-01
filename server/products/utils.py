from datetime import datetime
from decimal import Decimal

def format_date(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y')

def convert_price_to_float(price_string):
    return Decimal(price_string.replace('$', ''))

def validate_unit(unit):
    if unit not in ['lb', 'oz', 'gal', 'ea', 'g', 'kg', 'ml', 'l']:
        raise ValueError(f"Invalid unit: {unit}")
