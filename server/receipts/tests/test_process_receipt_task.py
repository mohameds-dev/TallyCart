from django.test import TestCase
from ..tasks import process_receipt_task
from ..models import ReceiptScan
from unittest.mock import patch

PATCH_SCAN = 'receipts.tasks.scan_image_text'
PATCH_PARSE = 'receipts.tasks.parse_ocr_text_with_llm'
PATCH_REVISE = 'receipts.tasks.revise_parsed_receipt_with_llm'

class ProcessReceiptTaskTests(TestCase):
    def setUp(self):
        self.scan = ReceiptScan.objects.create(image='test_image.jpg')
        self._scan_p = patch(PATCH_SCAN, return_value='ocr text')
        self._parse_p = patch(PATCH_PARSE, return_value='{}')
        self._revise_p = patch(PATCH_REVISE, return_value='{}')
        self._scan_p.start()
        self._parse_p.start()
        self._revise_p.start()

    def tearDown(self):
        self._revise_p.stop()
        self._parse_p.stop()
        self._scan_p.stop()

    def test_sets_status_to_completed(self):
        process_receipt_task(self.scan.pk)
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'completed')

    def test_calls_scan_image_text(self):
        with patch(PATCH_SCAN) as mock_scan:
            mock_scan.return_value = 'ocr'
            process_receipt_task(self.scan.pk)
            mock_scan.assert_called_once()

    def test_sets_ocr_text_from_scan_result(self):
        with patch(PATCH_SCAN, return_value='Mocked OCR text'):
            process_receipt_task(self.scan.pk)
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.ocr_text, 'Mocked OCR text')

    def test_calls_parse_with_ocr_text(self):
        with patch(PATCH_SCAN, return_value='Mocked OCR text'):
            with patch(PATCH_PARSE) as mock_parse:
                mock_parse.return_value = '{}'
                process_receipt_task(self.scan.pk)
                mock_parse.assert_called_once_with('Mocked OCR text')

    def test_sets_status_to_failed_when_scan_raises(self):
        with patch(PATCH_SCAN, side_effect=Exception('Mocked exception')):
            try:
                process_receipt_task(self.scan.pk)
            except Exception as e:
                self.assertEqual(str(e), 'Mocked exception')
        self.scan.refresh_from_db()
        self.assertEqual(self.scan.status, 'failed')
