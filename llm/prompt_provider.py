def create_prompt(ocr_text):
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
  

Output only the JSON. No explanations.

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
  ]
}

Now parse:

""" + ocr_text