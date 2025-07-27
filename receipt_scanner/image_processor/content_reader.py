import easyocr


def read_image_content(image_path):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(image_path, detail=0)