from utils.generate_receipt_scan_sample import generate_receipt_scan_sample
from utils.json_accuracy_evaluator import evaluate_accuracy
import json, csv, os, time
from datetime import datetime


def main():
    images_path = 'data/receipts_images'
    images = [
        # '12_23_2024-fiesta_mart_18.jpg'
        'receipt1.jpg',
        'receipt2.jpg',
    ]

    csv_file_path = 'data/processed_samples/accuracy_record.csv'
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'sample', 'accuracy'])
    


    for image in images:
        image_path = f'{images_path}/{image}'
        sample_id = f'{image.split('.')[0]}@{int(time.time())}'

        sample_data = generate_receipt_scan_sample(image_path, sample_id)
        try:
            ground_truth_json_path = f'{image_path.split('.')[0]}_ground_truth.json'
            ground_truth_dict = json.load(open(ground_truth_json_path))
            accuracy = evaluate_accuracy(ground_truth_dict, sample_data['json_data'])
        except FileNotFoundError:
            print(f"Ground truth file for {image} not found at {ground_truth_json_path}. Skipping accuracy evaluation.")
            accuracy = 'N/A'

        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sample_id, accuracy])

    
if __name__ == "__main__":
    main()
