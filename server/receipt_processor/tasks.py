from celery import shared_task
from .models import ReceiptScan
from .parsers.ocr_service import scan_image_text
from .llm.client import get_llm_response

@shared_task
def process_receipt_task(scan_id):
    scan = ReceiptScan.objects.get(id=scan_id)
    scan.status = 'processing'
    scan.save()
    try:
        scan.ocr_text = scan_image_text(scan.image.path)
        get_llm_response('*Prompt* using this text: ' + scan.ocr_text)
        scan.status = 'completed'
    except Exception as e:
        scan.status = 'failed'
    finally:
        scan.save()
