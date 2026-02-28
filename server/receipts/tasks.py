from celery import shared_task
from .models import ReceiptScan
from .parsers.ocr_service import scan_image_text
from .llm.client import parse_ocr_text_with_llm, revise_parsed_receipt_with_llm

@shared_task
def process_receipt_task(scan_id):
    scan = ReceiptScan.objects.get(id=scan_id)
    scan.status = 'processing'
    scan.save()
    try:
        scan.ocr_text = scan_image_text(scan.image.path) 
        parsed_receipt = parse_ocr_text_with_llm(scan.ocr_text)
        scan.receipt_data = revise_parsed_receipt_with_llm(scan.ocr_text, parsed_receipt)
        scan.status = 'completed'
    except Exception as e:
        print(f"Error processing receipt: {e}")
        scan.status = 'failed'
    finally:
        scan.save()
