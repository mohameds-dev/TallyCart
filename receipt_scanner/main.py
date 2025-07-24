import os
import tkinter as tk
from tkinter import filedialog
from image_processor.preprocessor import load_image, resize_image, save_image, preprocess_image
from image_processor.content_reader import read_image_content
from llm.prompt_provider import create_prompt_to_parse_ocr_text, create_prompt_to_revise_scanned_receipt
from llm.llama3 import get_response as get_response_llama3
from llm.mistral import get_response as get_response_mistral
# from dotenv import load_dotenv
import time
import json

def get_image_path():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image")
    root.destroy()
    return image_path

def get_text_from_image(image_path):
    sample_name = f"{image_path.split('/')[-1]}_{time.strftime('%Y-%m-%d_%H-%M-%S')}"
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

    image = preprocess_image(image, config)


    processed_image_path = f'data/processed_samples/images/{sample_name}.jpg'
    save_image(image, processed_image_path)

    extracted_lines = read_image_content(processed_image_path)
    ocr_text = "\n".join(extracted_lines)

    output_text_file_path = f"data/processed_samples/texts/{sample_name}.txt"
    os.makedirs(os.path.dirname(output_text_file_path), exist_ok=True)
    with open(output_text_file_path, 'w') as f:
        f.write(f"Processed image: {processed_image_path}\nWith config:\n {config}\n\n")
        f.write(ocr_text)

    return ocr_text

def run_llm_on_text(ocr_text):
    prompt = create_prompt_to_parse_ocr_text(ocr_text)
    response = get_response_llama3(prompt)

    print("Calling LLM to revise OCR text...")
    prompt = create_prompt_to_revise_scanned_receipt(ocr_text, response)
    response = get_response_mistral(prompt)

    return response

def main():

    print("Starting...")
    # load_dotenv()

    # image_path = get_image_path()
    image_path = 'data/receipts_images/receipt1.jpg'
    ocr_text = get_text_from_image(image_path)
    # print(ocr_text)
    # response = run_llm_on_text(ocr_text)
    # print(response)

    



if __name__ == "__main__":
    main()
