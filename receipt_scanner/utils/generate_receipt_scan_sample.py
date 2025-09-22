import os
from llm.prompt_provider import create_prompt_to_parse_ocr_text, create_prompt_to_revise_scanned_receipt
from llm.google_genai import get_response as get_response_google_genai
import json
import random
from dotenv import load_dotenv
from utils.logger import set_sample_id, log_args_result_and_time, get_sample_id, set_log_dir
from utils.json_parser import parse_json_dict_from_text
from image_processor.content_reader import get_text_from_image
load_dotenv()

DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")


@log_args_result_and_time()
def run_llm_on_text(ocr_text):
    '''
    Receives the ocr text and returns the parsed receipt. Sequence:
    1. Call the LLM to parse the ocr text and return a json
    2. Call the LLM to revise the parsed json and the ocr text and return the corrected json
    Args:
        ocr_text (str): The text extracted from the image using ocr
    Returns:
        str: The parsed receipt
    '''
    prompt = create_prompt_to_parse_ocr_text(ocr_text)
    response = get_response_google_genai(prompt)
    prompt = create_prompt_to_revise_scanned_receipt(ocr_text, response)
    response = get_response_google_genai(prompt)

    return response

def generate_receipt_scan_sample(image_path, sample_id=None):
    if sample_id is None:
        sample_id = random.randint(1, 1000000)
        print(f"Generated random sample id: {sample_id}")

    set_sample_id(sample_id)
    sample_folder_path = f'{DATA_FOLDER_PATH}/processed_samples/sample_{get_sample_id()}'
    os.makedirs(sample_folder_path, exist_ok=True)
    import shutil
    copied_image_path = f'{sample_folder_path}/{image_path.split("/")[-1]}'
    shutil.copy(image_path, copied_image_path)
    set_log_dir(sample_folder_path)
    print(f"Starting to generate sample {get_sample_id()}...")

    ocr_text = get_text_from_image(copied_image_path)
    response = run_llm_on_text(ocr_text)
    json_file_path = f'{sample_folder_path}/receipt_{get_sample_id()}_final_json_output.json'
    json_data = parse_json_dict_from_text(response)
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=4)


    print(f"Sample {get_sample_id()} generated successfully")

    return {
        "sample_id": get_sample_id(),
        "json_data": json_data,
        "json_file_path": json_file_path
    }
