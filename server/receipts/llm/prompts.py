def create_prompt_to_parse_ocr_text(ocr_text):
    return """
SYSTEM:
You are a receipt parser. Given raw OCR text from a grocery receipt, return only a valid JSON object with:

- "store_name": string  
- "store_address": string  
- "receipt_datetime": string in format YYYY-MM-DD HH:MM  
- "items": list of objects with:
  - "item": name (include descriptors like “skinless” or “90/10”)
  - "quantity": float
  - "unit": string (must be one of "lb", "ea", "oz")
  - "unit_price": float (must match the unit)
  - "price": float
  

Output only the JSON. No explanations. If you encounter any errors, add them to the "errors" list.

Example OCR text:

SuperMart
123 MAIN ST, CITY
2024-12-01 14:22
Beef Ground 
90/10
$9.99
1.50 Ib
$6.66/lb

Expected JSON:
{
  "store_name": "SuperMart",
  "store_address": "123 MAIN ST, CITY",
  "receipt_datetime": "2024-12-01 14:22",
  "items": [
    {
      "item": "Beef Ground (90/10)",
      "quantity": 1.5,
      "unit": "lb",
      "unit_price": 6.66,
      "price": 9.99
    }
  ],
  "errors": []
}

Now parse:

""" + ocr_text

def create_prompt_to_revise_scanned_receipt(ocr_text, parsed_data_string):
    return f"""
SYSTEM:
You are revising the scanned receipt data as part of a receipt parsing pipeline.

You are given:
- The original OCR text
- The parsed data from the OCR text

You need to revise the parsed data to correct any errors or omissions. Look out for:

- Missing items
- Incorrect item quantities
- Incorrect item prices (like $6.00 instead of 56.00 or S5.00)
- Incorrect item units (like "lb" instead of "Ib")

Your output should be a valid JSON object. No explanations, no other text.

Here is the original OCR text:
{ocr_text}

Here is the parsed data:
{parsed_data_string}

Your revised data:
"""