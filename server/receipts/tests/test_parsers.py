import numpy as np
from django.test import TestCase
from ..parsers.ocr_service import scan_image_text
from ..parsers.json_dict_parsers import parse_json_dict_from_text
from unittest.mock import patch

class OcrServiceTests(TestCase):
    def setUp(self):
        self.sample_image_path = 'data/receipts_images/receipt1.jpg'
        self.sample_ocr_text = "Rne Bazacs\naanre\nPrime Bazaar Med Center\n8403 ALMEDA RD #B\nHOUSTON, TX 77054\n2819741366\nWWWPRIMEBAZAARTX COM\n08-Apr-2025 7:00:16P\nTransaction 101035\nChicken Tenders\nS5.71\n1.43 Ib\nS3.99/lb\nTenders\nS6.10\n1.53 Ib\nS3.99/1b\nDrumstick\nS4.41\n1.77 Ib\nS2.49/1b\nChicken Tenders\nS5.67\n1.42 Ib\nS3.99/1b\n1\nChicken Drumstick\nS5.03\nskinless\n2.02 Ib\nS2.49/1b\n1\nChicken Drumstick\nS5.00\nskinless\n2.01 Ib\nS2.49/1b\n1\nChicken Drumstick\nS4.61\nskinless\n1.85 Ib\nS2.49/1b\nChicken Thigh\n85.37\nBoneless Cubes\n1.54 Ib\nS3.49/1b\nChicken Thigh\nS6.18\nBoneless Cubes\n1.77 Ib\nS3.49/1b\nBeef Cround lean\nS11.18\n90/10\n1.6 Ib @ $6.99/1b\n1\nBeef Ground lean\nS9.93\n90/10\n1.42 Ib\nS6.99/1b\n1\nBeef Ground lean\nS10.21\n90/10\n1.46 Ib @ S6.99/lb\nTotal\nCREDIT CARD SALE\nS79.40\nDISCOVER 1684\nChicken\nChicken\nskinless\n579.40"
    
    def test_scan_image_text_returns_a_string(self):
        fake_image = np.zeros((50, 100, 3), dtype=np.uint8)
        with patch('receipts.parsers.ocr_service.load_image', return_value=fake_image):
            with patch('receipts.parsers.ocr_service.read_image_content', return_value=['line one', 'line two']):
                with patch('receipts.parsers.ocr_service.save_image'):
                    result = scan_image_text(self.sample_image_path)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'line one\nline two')

    

class JsonDictParsersTests(TestCase):
    def setUp(self):
        self.sample_text_1 = 'Here is your json: ```json\n{\n  \"store_name\": \"Prime Bazaar Med Center\",\n  \"store_address\": \"8403 ALMEDA RD #B\\nHOUSTON, TX 77054\",\n  \"receipt_datetime\": \"2025-04-08 19:00\",\n  \"items\": [\n    {\n      \"item\": \"Chicken Tenders\",\n      \"quantity\": 1.43,\n      \"unit\": \"lb\",\n      \"unit_price\": 3.99,\n      \"price\": 5.71\n    }\n  ],\n  \"total\": 79.40\n}\n```\n'
        self.sample_text_2 = 'Here is your json: ```json\n{\n  \"name\": \"John Doe\",\n  \"age\": 30,\n  \"city\": \"New York\"\n}\n```\n'
    
    def test_parse_json_dict_from_text_returns_a_dict(self):
        result = parse_json_dict_from_text(self.sample_text_1)
        self.assertIsInstance(result, dict)

    def test_parse_json_dict_from_text_takes_sample_text_1_and_returns_dict_with_correct_keys(self):
        result = parse_json_dict_from_text(self.sample_text_1)

        self.assertEqual(list(result.keys()), ['store_name', 'store_address', 'receipt_datetime', 'items', 'total'])

    def test_parse_json_dict_from_text_takes_sample_text_2_and_returns_dict_with_correct_keys(self):
        result = parse_json_dict_from_text(self.sample_text_2)

        self.assertEqual(list(result.keys()), ['name', 'age', 'city'])