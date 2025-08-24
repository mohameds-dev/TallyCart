import easyocr
from utils.logger import log_args_result_and_time
from image_processor.preprocessor import load_image, save_image, preprocess_image

def read_image_content(image_path):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(image_path, detail=0)

@log_args_result_and_time()
def get_text_from_image(image_path):
    image = load_image(image_path)

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

    processed_image_path = image_path.replace('.jpg', '_processed.jpg')
    image = preprocess_image(image, config)
    save_image(image, processed_image_path)

    extracted_lines = read_image_content(processed_image_path)
    ocr_text = "\n".join(extracted_lines)

    return ocr_text