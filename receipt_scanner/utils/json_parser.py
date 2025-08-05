import re
import json


def get_json_from_text(text):
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json_str
    else:
        raise ValueError("No JSON found in the text")



if __name__ == '__main__':
    text = "```json\n{\n  \"store_name\": \"Prime Bazaar Med Center\",\n  \"store_address\": \"8403 ALMEDA RD #B\\nHOUSTON; TX 77054\",\n  \"receipt_datetime\": \"2025-04-08 19:16\",\n  \"items\": [\n    {\n      \"item\": \"Chicken Tenders\",\n      \"quantity\": 1.43,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.99,\n      \"price\": 5.71\n    },\n    {\n      \"item\": \"Chicken Tenders\",\n      \"quantity\": 1.0,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.99,\n      \"price\": 6.10\n    },\n    {\n      \"item\": \"Chicken Drumstick\",\n      \"quantity\": 1.77,\n      \"unit\": \"lb\",\n      \"unit_price\": 2.49,\n      \"price\": 4.41\n    },\n    {\n      \"item\": \"Chicken Tenders\",\n      \"quantity\": 1.42,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.99,\n      \"price\": 5.67\n    },\n    {\n      \"item\": \"Chicken Drumstick skinless\",\n      \"quantity\": 2.02,\n      \"unit\": \"lb\",\n      \"unit_price\": 2.49,\n      \"price\": 5.03\n    },\n    {\n      \"item\": \"Chicken Drumstick skinless\",\n      \"quantity\": 2.01,\n      \"unit\": \"lb\",\n      \"unit_price\": 2.49,\n      \"price\": 5.00\n    },\n    {\n      \"item\": \"Chicken Drumstick skinless\",\n      \"quantity\": 1.85,\n      \"unit\": \"lb\",\n      \"unit_price\": 2.49,\n      \"price\": 4.61\n    },\n    {\n      \"item\": \"Chicken Thigh Boneless Cubes\",\n      \"quantity\": 1.54,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.49,\n      \"price\": 5.37\n    },\n    {\n      \"item\": \"Chicken Thigh Boneless Cubes\",\n      \"quantity\": 1.77,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.49,\n      \"price\": 6.18\n    },\n    {\n      \"item\": \"Beef Ground lean 90/10\",\n      \"quantity\": 1.6,\n      \"unit\": \"lb\",\n      \"unit_price\": 6.99,\n      \"price\": 11.18\n    },\n    {\n      \"item\": \"Beef Ground lean 90/10\",\n      \"quantity\": 1.42,\n      \"unit\": \"lb\",\n      \"unit_price\": 6.99,\n      \"price\": 9.93\n    },\n    {\n      \"item\": \"Beef Ground lean 90/10\",\n      \"quantity\": 1.46,\n      \"unit\": \"lb\",\n      \"unit_price\": 6.99,\n      \"price\": 10.21\n    }\n  ],\n  \"total\": 79.40\n}\n```\n"
    json_str = get_json_from_text(text)
    print(json_str)
