from utils.generate_receipt_scan_sample import generate_receipt_scan_sample

def main():
    images_path = 'data/receipts_images'
    images = [
        '12_23_2024-fiesta_mart_18.jpg'
    ]

    for image in images:
        image_path = f'{images_path}/{image}'
        generate_receipt_scan_sample(image_path, image.split('.')[0])
    
if __name__ == "__main__":
    main()
