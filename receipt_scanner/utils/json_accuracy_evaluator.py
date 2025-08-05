from thefuzz import fuzz
import json, os
from dotenv import load_dotenv
load_dotenv()
DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")
from json_parser import get_json_from_text

# --- Module 1: Specific Value Comparators ---
# These functions compare single values and return a score from 0.0 to 1.0.

def compare_strings(gt_str, llm_str):
    """Compares two strings using fuzzy matching and returns a similarity score."""
    if not isinstance(gt_str, str) or not isinstance(llm_str, str):
        return 0.0
    return fuzz.ratio(gt_str, llm_str) / 100.0

def compare_numbers(gt_num, llm_num):
    """Compares two numbers for exact equality."""
    # Note: For floats, you might want to allow a small tolerance.
    if type(gt_num) != type(llm_num):
        return 0.0
    return 1.0 if gt_num == llm_num else 0.0

def compare_booleans(gt_bool, llm_bool):
    """Compares two booleans for exact equality."""
    if not isinstance(gt_bool, bool) or not isinstance(llm_bool, bool):
        return 0.0
    return 1.0 if gt_bool == llm_bool else 0.0


# --- Module 2: The Recursive Evaluator ---
# This is the core engine that traverses the JSON.

def evaluate(gt_data, llm_data, path_prefix=""):
    """
    Recursively compares two data structures (dictionaries, lists, or values).
    Returns a flat list of detailed results.
    """
    results = []

    # Case 1: Dictionaries (JSON objects)
    if isinstance(gt_data, dict):
        # Ensure llm_data is also a dict for comparison
        llm_data = llm_data if isinstance(llm_data, dict) else {}
        
        all_keys = set(gt_data.keys()) | set(llm_data.keys())

        for key in all_keys:
            current_path = f"{path_prefix}.{key}" if path_prefix else key
            
            if key in gt_data and key in llm_data:
                # Key exists in both, so recurse deeper
                results.extend(evaluate(gt_data[key], llm_data[key], path_prefix=current_path))
            elif key in gt_data:
                # Key is missing from LLM output
                results.append({"field": current_path, "score": 0.0, "notes": "Field missing from output"})
            else:
                # Key is an extra field in LLM output
                results.append({"field": current_path, "score": 0.0, "notes": "Extra field in output"})

    # Case 2: Lists
    elif isinstance(gt_data, list):
        # Ensure llm_data is also a list for comparison
        llm_data = llm_data if isinstance(llm_data, list) else []
        
        for i in range(max(len(gt_data), len(llm_data))):
            current_path = f"{path_prefix}[{i}]"
            item_gt = gt_data[i] if i < len(gt_data) else "MISSING_ITEM"
            item_llm = llm_data[i] if i < len(llm_data) else "MISSING_ITEM"
            results.extend(evaluate(item_gt, item_llm, path_prefix=current_path))

    # Case 3: Primitive Values (string, number, bool, etc.)
    else:
        score = 0.0
        # This is our "dispatcher" that calls the right comparator
        if isinstance(gt_data, str):
            score = compare_strings(gt_data, llm_data)
        elif isinstance(gt_data, (int, float)):
            score = compare_numbers(gt_data, llm_data)
        elif isinstance(gt_data, bool):
            score = compare_booleans(gt_data, llm_data)
        elif gt_data is None:
            score = 1.0 if llm_data is None else 0.0
        
        # Add result for the primitive value
        results.append({
            "field": path_prefix,
            "score": score,
            "ground_truth": gt_data,
            "llm_output": llm_data
        })
        
    return results

# --- Module 3: Reporting ---
# This function takes the results and presents them nicely.

def generate_report(results):
    """Calculates the overall score and prints a detailed report."""
    if not results:
        print("No fields to compare.")
        return

    # Calculate overall accuracy
    total_score = sum(r['score'] for r in results)
    overall_accuracy = (total_score / len(results)) * 100

    print("--- JSON Accuracy Evaluation Report ---")
    print(f"\nOverall Accuracy: {overall_accuracy:.2f}%\n")
    print(f"{'Field':<30} | {'Score (%)':<10} | {'Ground Truth':<30} | {'LLM Output':<30} | Notes")
    print("-" * 110)

    for r in results:
        gt_str = str(r.get('ground_truth', 'N/A'))
        llm_str = str(r.get('llm_output', 'N/A'))
        score_pct = r['score'] * 100
        notes = r.get('notes', '')
        print(f"{r['field']:<30} | {score_pct:<10.2f} | {gt_str[:28]:<30} | {llm_str[:28]:<30} | {notes}")



def main():
    sample_id = 1
    ground_truth_json = json.load(open(f'{DATA_FOLDER_PATH}/receipts_images/receipt1_ground_truth.json'))
    llm_output_json = json.load(open(f'{DATA_FOLDER_PATH}/processed_samples/sample_{sample_id}/{sample_id}_run_llm_on_text.json'))
    llm_output_json = json.loads(get_json_from_text(llm_output_json['output']))

    print(f'type of ground_truth_json: {type(ground_truth_json)}')
    print(f'type of llm_output_json: {type(llm_output_json)}')

    evaluation_results = evaluate(ground_truth_json, llm_output_json)

    generate_report(evaluation_results)
    
if __name__ == "__main__":
    main()