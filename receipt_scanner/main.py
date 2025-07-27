import os
import tkinter as tk
from tkinter import filedialog
from image_processor.preprocessor import load_image, resize_image, save_image
from image_processor.content_reader import read_image_content
from llm.prompt_provider import create_prompt_to_parse_ocr_text, create_prompt_to_revise_scanned_receipt
from llm.llama3 import get_response as get_response_llama3
from llm.mistral import get_response as get_response_mistral
# from dotenv import load_dotenv


def get_image_path():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image")
    root.destroy()
    return image_path

def main():
    print("Starting...")
    # load_dotenv()
    print("Loading image...")

    # image_path = get_image_path()
    image_path = 'data/receipts_images/receipt1.jpg'

    image = load_image(image_path)
    image = resize_image(image, max_width=1200)
    # image = preprocess_image(image) # TODO: experiment with different preprocessing techniques
    print("Loaded & resized image!")

    resized_image_path = 'data/resized_images/temp_resized.jpg'
    save_image(image, resized_image_path)

    print("Saved resized image to temp file")
    print("Starting OCR...")

    results = read_image_content(resized_image_path)

    print("\nExtracted Text!\n")
    print("Calling LLM to parse OCR text...")

    ocr_text = "\n".join(results)
    prompt = create_prompt_to_parse_ocr_text(ocr_text)
    response = get_response_llama3(prompt)

    print("Calling LLM to revise OCR text...")
    prompt = create_prompt_to_revise_scanned_receipt(ocr_text, response)
    response = get_response_mistral(prompt)

    print(response)

    os.remove(resized_image_path)


if __name__ == "__main__":
    main()
