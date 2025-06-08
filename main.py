import cv2
import easyocr

# Resize image first
image_path = 'data/receipts_images/receipt1.jpg'
image = cv2.imread(image_path)

# Check if image loaded
if image is None:
    print("Failed to load image.")
    exit()

# Resize to max width while maintaining aspect ratio
max_width = 1000
height, width = image.shape[:2]
if width > max_width:
    scale_ratio = max_width / width
    image = cv2.resize(image, (max_width, int(height * scale_ratio)))

# Save resized copy to temp file
temp_path = 'data/resized_images/temp_resized.jpg'
cv2.imwrite(temp_path, image)

# OCR
reader = easyocr.Reader(['en'], gpu=True)
results = reader.readtext(temp_path, detail=0)

print("\nExtracted Text:")
for line in results:
    print(line)
