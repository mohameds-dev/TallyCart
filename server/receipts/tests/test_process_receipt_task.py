from django.test import TestCase
from ..tasks import process_receipt_task
from ..models import ReceiptScan
from unittest.mock import patch, MagicMock

class ProcessReceiptTaskTests(TestCase):

    def setUp(self):
        self.sample_scan_object = ReceiptScan.objects.create(image='test_image.jpg')
        # Mock LLM so no test hits the real API (no 429s)
        self._gemini_patcher = patch('receipts.llm.client.get_gemini_response')
        mock_gemini = self._gemini_patcher.start()
        mock_response = MagicMock()
        mock_response.text = '{}'
        mock_gemini.return_value = mock_response

    def tearDown(self):
        self._gemini_patcher.stop()

    def test_process_receipt_task_sets_status_to_completed(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text', return_value='mocked ocr text'):
            process_receipt_task(scan.pk)
        scan.refresh_from_db()
        self.assertEqual(scan.status, 'completed')

    def test_process_receipt_task_sets_status_to_completed_with_mocked_scan_function(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text', return_value='mocked ocr text'):
            process_receipt_task(scan.pk)
        scan.refresh_from_db()
        self.assertEqual(scan.status, 'completed')

    def test_process_receipt_task_calls_scan_image_text(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text') as mock_scan_image_text:
            mock_scan_image_text.return_value = 'Mocked OCR text'
            process_receipt_task(scan.pk)
            mock_scan_image_text.assert_called_once()

    def test_process_receipt_task_sets_ocr_text_to_the_return_value_of_scan_image_text(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text', return_value='Mocked OCR text'):
            process_receipt_task(scan.pk)
        scan.refresh_from_db()
        self.assertEqual(scan.ocr_text, 'Mocked OCR text')

    def test_process_receipt_task_calls_parse_ocr_text_with_llm(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text', return_value='Mocked OCR text'):
            with patch('receipts.tasks.parse_ocr_text_with_llm') as mock_parse:
                mock_parse.return_value = {}
                with patch('receipts.tasks.revise_parsed_receipt_with_llm', return_value={}):
                    process_receipt_task(scan.pk)
                mock_parse.assert_called_once()

    @patch('receipts.tasks.revise_parsed_receipt_with_llm', return_value={})
    @patch('receipts.tasks.parse_ocr_text_with_llm', return_value={})
    @patch('receipts.tasks.scan_image_text')
    def test_process_receipt_task_calls_parse_with_ocr_text_in_prompt(self, mock_scan_image_text, mock_parse, mock_revise):
        scan = self.sample_scan_object
        mock_scan_image_text.return_value = 'Mocked OCR text'
        process_receipt_task(scan.pk)
        called_arg = mock_parse.call_args[0][0]
        self.assertIn('Mocked OCR text', called_arg)

    def test_process_receipt_task_sets_status_to_failed_if_scan_image_text_raises_an_exception(self):
        scan = self.sample_scan_object
        with patch('receipts.tasks.scan_image_text') as mock_scan_image_text:
            mock_scan_image_text.side_effect = Exception('Mocked exception')
            process_receipt_task(scan.pk)
            scan.refresh_from_db()

            self.assertEqual(scan.status, 'failed')
