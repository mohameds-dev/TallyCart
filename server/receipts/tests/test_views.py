import io
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import ReceiptScan
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import os
from unittest.mock import patch

# Minimal 1x1 JPEG bytes so tests don't depend on external files or real image I/O
def _minimal_jpeg_bytes():
    buf = io.BytesIO()
    Image.new('RGB', (1, 1), color='white').save(buf, format='JPEG')
    return buf.getvalue()

class ReceiptScanViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.receipt_scan_request_url = reverse('receipt-scan')
        self.receipt_scan_list_url = reverse('receipts-list')
        self.receipt_scan_detail_url = lambda scan_id: reverse('receipt-detail', args=[scan_id])
        self.receipt_scan_requestdata = {
            'image': SimpleUploadedFile(
                name='test_image.jpg',
                content=_minimal_jpeg_bytes(),
                content_type='image/jpeg'
            )
        }
        self._task_patch = patch('receipts.tasks.process_receipt_task.delay')
        self._mock_delay = self._task_patch.start()
        self._mock_delay.reset_mock()

    def tearDown(self):
        self._task_patch.stop()
        self.remove_images_created_in_tests()
    
    def remove_images_created_in_tests(self):
        for scan in ReceiptScan.objects.all():
            if scan.image and os.path.exists(scan.image.path):
                    os.remove(scan.image.path)

    def test_receipt_scan_request_post_takes_image_and_returns_201_status_code(self):
        response = self.client.post(self.receipt_scan_request_url, self.receipt_scan_requestdata)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_receipt_scan_list_view_get_returns_200_status_code(self):
        self.assertEqual(self.client.get(self.receipt_scan_list_url).status_code, status.HTTP_200_OK)

    def test_receipt_scan_list_view_get_returns_empty_list_when_no_scans_exist(self):
        self.assertEqual(self.client.get(self.receipt_scan_list_url).data, [])

    def test_receipt_scan_list_view_get_returns_list_of_size_1_when_one_scan_exists(self):
        self.client.post(self.receipt_scan_request_url, self.receipt_scan_requestdata)
        self.assertEqual(len(self.client.get(self.receipt_scan_list_url).data), 1)

    def test_receipt_scan_detail_view_get_returns_404_status_code_when_there_are_no_scans(self):
        self.assertEqual(self.client.get(self.receipt_scan_detail_url(scan_id=1)).status_code, status.HTTP_404_NOT_FOUND)

    def test_receipt_scan_request_post_returns_the_correct_id(self):
        response = self.client.post(self.receipt_scan_request_url, self.receipt_scan_requestdata)
        self.assertEqual(response.data['id'], ReceiptScan.objects.get(id=response.data['id']).id)
    
    def test_receipt_scan_request_post_creates_a_scan_with_pending_status(self):
        response = self.client.post(self.receipt_scan_request_url, self.receipt_scan_requestdata)
        self.assertEqual(ReceiptScan.objects.get(id=response.data['id']).status, 'pending')

    def test_receipt_scan_request_post_calls_the_process_receipt_task(self):
        self.client.post(self.receipt_scan_request_url, self.receipt_scan_requestdata)
        self._mock_delay.assert_called_once()
