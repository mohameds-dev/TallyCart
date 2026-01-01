from django.test import TestCase
from ..tasks import process_receipt_task
from ..models import ReceiptScan
from unittest.mock import patch

class ProcessReceiptTaskTests(TestCase):

    def setUp(self):
        self.sample_scan_object = ReceiptScan.objects.create(image='test_image.jpg')

    def test_process_receipt_task_sets_status_to_completed(self):
        scan = self.sample_scan_object
        process_receipt_task(scan.pk)
        scan.refresh_from_db()

        self.assertEqual(scan.status, 'completed')

    def test_process_receipt_task_calls_scan_image_text(self):
        scan = self.sample_scan_object
        with patch('receipt_processor.tasks.scan_image_text') as mock_scan_image_text:
            mock_scan_image_text.return_value = 'Mocked OCR text'
            process_receipt_task(scan.pk)
            mock_scan_image_text.assert_called_once()

    def test_process_receipt_task_sets_ocr_text_to_the_return_value_of_scan_image_text(self):
        scan = self.sample_scan_object
        with patch('receipt_processor.tasks.scan_image_text') as mock_scan_image_text:
            mock_scan_image_text.return_value = 'Mocked OCR text'
            process_receipt_task(scan.pk)
            scan.refresh_from_db()

            self.assertEqual(scan.ocr_text, 'Mocked OCR text')

    def test_process_receipt_task_calls_get_llm_response(self):
        scan = self.sample_scan_object
        with patch('receipt_processor.tasks.get_llm_response') as mock_get_llm_response:
            process_receipt_task(scan.pk)
            mock_get_llm_response.assert_called_once()

    @patch('receipt_processor.tasks.get_llm_response')
    @patch('receipt_processor.tasks.scan_image_text')
    def test_process_receipt_task_calls_get_llm_response_with_ocr_text_included_in_the_prompt(self, mock_scan_image_text, mock_get_llm_response):
        scan = self.sample_scan_object
        mock_scan_image_text.return_value = 'Mocked OCR text'
        process_receipt_task(scan.pk)
        called_arg = mock_get_llm_response.call_args[0][0]

        self.assertIn('Mocked OCR text', called_arg)

    def test_process_receipt_task_sets_status_to_failed_if_scan_image_text_raises_an_exception(self):
        scan = self.sample_scan_object
        with patch('receipt_processor.tasks.scan_image_text') as mock_scan_image_text:
            mock_scan_image_text.side_effect = Exception('Mocked exception')
            process_receipt_task(scan.pk)
            scan.refresh_from_db()

            self.assertEqual(scan.status, 'failed')
