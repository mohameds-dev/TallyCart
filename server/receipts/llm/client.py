from .gemini_api import get_response as get_gemini_response
from .prompts import create_prompt_to_parse_ocr_text, create_prompt_to_revise_scanned_receipt

def _get_llm_text_response(prompt):
    return get_gemini_response(prompt).text.strip()

def parse_ocr_text_with_llm(ocr_text):
    prompt = create_prompt_to_parse_ocr_text(ocr_text)
    return _get_llm_text_response(prompt)

def revise_parsed_receipt_with_llm(ocr_text, parsed_receipt):
    prompt = create_prompt_to_revise_scanned_receipt(ocr_text, parsed_receipt)
    return _get_llm_text_response(prompt)