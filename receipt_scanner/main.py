import os
import tkinter as tk
from tkinter import filedialog
import cv2
from image_processor.preprocessor import load_image, preprocess_image, resize_image
from image_processor.content_reader import read_image_content
from llm.prompt_provider import create_prompt
# from llm.llama3 import get_response
from llm.google_genai import get_response
from dotenv import load_dotenv


def get_image_path():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an image")
    root.destroy()
    return image_path

def main():
    print("Starting...")
    print("Loading environment variables...")
    load_dotenv()
    print("Environment variables loaded")
    print("Starting image preprocessing...")

    # image_path = get_image_path()
    image_path = 'data/receipts_images/receipt1.jpg'

    image = load_image(image_path)
    image = resize_image(image, max_width=1200)
    # image = preprocess_image(image) # TODO: experiment with different preprocessing techniques
    print("Preprocessed image")

    resized_image_path = 'data/resized_images/temp_resized.jpg'
    cv2.imwrite(resized_image_path, image)

    print("Saved resized image to temp file")
    print("Starting OCR...")

    results = read_image_content(resized_image_path)

    print("\nExtracted Text!\n")
    print("Calling LLM...")

    prompt = create_prompt("\n".join(results))
    response = get_response(prompt)

    print(response)

    os.remove(resized_image_path)


if __name__ == "__main__":
    main()
    