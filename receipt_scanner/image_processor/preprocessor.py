import cv2

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

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    return enhanced

def save_image(image, path):
    cv2.imwrite(path, image)