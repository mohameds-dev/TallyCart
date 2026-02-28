import cv2
import easyocr

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image from {image_path}")
    
    return image

def resize_image(image, max_width=1000):
    height, width = image.shape[:2]
    if width > max_width:
        scale_ratio = max_width / width
        image = cv2.resize(image, (max_width, int(height * scale_ratio)))

    return image

def preprocess_image(image, config={}):

    if config.get('resize'):
        max_width = config.get('resize').get('max_width')
        image = resize_image(image, max_width)

    if config.get('greyscale'):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if config.get('clahe'):
        clip_limit = config.get('clahe').get('clipLimit')
        tile_grid_size = config.get('clahe').get('tileGridSize')
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        image = clahe.apply(image)

    return image

def save_image(image, path):
    cv2.imwrite(path, image)

def read_image_content(image_path):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(image_path, detail=0)

def scan_image_text(image_path):
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


