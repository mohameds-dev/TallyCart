import os
import tkinter as tk
from tkinter import filedialog
from image_processor.preprocessor import load_image, resize_image, save_image, preprocess_image
from image_processor.content_reader import read_image_content
from llm.prompt_provider import create_prompt_to_parse_ocr_text, create_prompt_to_revise_scanned_receipt
from llm.llama3 import get_response as get_response_llama3
from llm.mistral import get_response as get_response_mistral
from llm.google_genai import get_response as get_response_google_genai
# from dotenv import load_dotenv
import time
import json
from dotenv import load_dotenv
from utils.logger import set_sample_id, log_args_result_and_time, get_sample_id, set_log_dir
load_dotenv()

DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")


def get_image_path():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image")
    root.destroy()
    return image_path

@log_args_result_and_time()
def get_text_from_image(image_path):
    image = load_image(image_path)
    # TODO: understand the config better
    # TODO: experiment with different configs in colab and understand the different results
    # TODO: grab the receipts images that are already processed in the csv
        # TODO: take the images in different conditions for realistic results
        # TODO: name the image files with the condition, store and the date
        # TODO: create a json or csv with the ground truth for each image (take from already made csv)
    # TODO: run the ocr with the different configs and save the results on the drive
    # TODO: create a script to compare the results to the ground truths and see the accuracy
    # TODO: note the config with the best results on average

    config = {
        'greyscale': True,
        'clahe': {
            'clipLimit': 2.0,
            'tileGridSize': (8, 8)
        },
        'resize': {
            'max_width': 1200
        }
    }

    processed_image_path = f'{os.getenv("DATA_FOLDER_PATH")}/processed_samples/sample_{get_sample_id()}/{image_path.split("/")[-1].split(".")[0]}_processed.jpg'
    image = preprocess_image(image, config)
    save_image(image, processed_image_path)

    extracted_lines = read_image_content(processed_image_path)
    ocr_text = "\n".join(extracted_lines)

    return ocr_text

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
    # response = get_response_llama3(prompt)
    response = get_response_google_genai(prompt)

    print("Calling LLM to revise OCR text...")
    prompt = create_prompt_to_revise_scanned_receipt(ocr_text, response)
    # response = get_response_mistral(prompt)
    response = get_response_google_genai(prompt)

    return response


def generate_receipt_scan_sample():
    set_sample_id(1)
    data_folder_path = os.getenv('DATA_FOLDER_PATH')
    sample_folder_path = f'{data_folder_path}/processed_samples/sample_{get_sample_id()}'
    os.makedirs(sample_folder_path, exist_ok=True)
    set_log_dir(sample_folder_path)
    print(f"Starting to generate sample{get_sample_id()}...")
    # load_dotenv()

    # image_path = get_image_path()
    image_path = 'data/receipts_images/receipt1.jpg'
    ocr_text = get_text_from_image(image_path)
    # print(ocr_text)
    response = run_llm_on_text(ocr_text)
    # print(response)
    print(f"Sample {get_sample_id()} generated successfully")



from utils.json_accuracy_evaluator import evaluate, generate_report
def main():
    generate_receipt_scan_sample()
    
if __name__ == "__main__":
    main()
