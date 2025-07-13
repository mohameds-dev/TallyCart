from datetime import datetime

def format_date(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y')

def convert_price_to_float(price_string):
    return float(price_string.replace('$', ''))

def validate_unit(unit):
    if unit not in ['lb', 'oz', 'gal', 'ea']:
        raise ValueError(f"Invalid unit: {unit}")
