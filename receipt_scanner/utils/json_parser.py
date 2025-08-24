import re
import json


def extract_json_str_from_text(text) -> str:
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json_str
    else:
        raise ValueError("No JSON found in the text")



def parse_json_dict_from_text(text) -> dict:
    json_str = extract_json_str_from_text(text)
    return json.loads(json_str)

if __name__ == "__main__":
    json_file_path = '/mnt/hddm/MyProjects/TallyCart/receipt_scanner/data/processed_samples/sample_receipt2/receipt2_run_llm_on_text.json'
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    
    json_data = parse_json_dict_from_text(json_data['output'])
    # write it to receipt2_ground_truth.json
    with open('receipt2_ground_truth.json', 'w') as file:
        json.dump(json_data, file, indent=4)