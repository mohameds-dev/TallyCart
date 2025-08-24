from difflib import SequenceMatcher

class AccuracyEvaluator:
    def __init__(self):
        self.fields_matched = 0
        self.fields_total = 0
        self.type_evaluators = {
            dict: self.evaluate_accuracy_dict,
            list: self.evaluate_accuracy_list,
            str: self.evaluate_accuracy_str,
        }

    def count_len_recursively(self, data):
        if isinstance(data, dict):
            return sum(self.count_len_recursively(value) for value in data.values())
        elif isinstance(data, list):
            return sum(self.count_len_recursively(item) for item in data)
        else:
            return 1

    def evaluate_accuracy_primitive(self, ground_truth_data, sample_data):
        self.fields_total += 1
        if ground_truth_data == sample_data:
            self.fields_matched += 1

    def evaluate_accuracy_dict(self, ground_truth_data, sample_data):
        for key, value in ground_truth_data.items():
            if type(value) in self.type_evaluators:
                self.type_evaluators[type(value)](value, sample_data.get(key, None))
            else:
                self.evaluate_accuracy_primitive(value, sample_data.get(key, None))

        self.fields_total += len(sample_data) - len(set(sample_data.keys()).intersection(set(ground_truth_data.keys())))

    def evaluate_accuracy_list(self, ground_truth_data_list, sample_data_list):
        len_gt = len(ground_truth_data_list) if ground_truth_data_list is not None else 0
        len_sample = len(sample_data_list) if sample_data_list is not None else 0

        if len_gt == len_sample == 0:
            self.fields_matched += 1
            self.fields_total += 1
        elif len_gt == 0 and len_sample > 0:
            self.fields_total += len_sample
        else:
            for i in range(min(len_gt, len_sample)):
                evaluate = self.type_evaluators.get(type(ground_truth_data_list[0]), self.evaluate_accuracy_primitive)
                evaluate(ground_truth_data_list[i], sample_data_list[i])

    def evaluate_accuracy_str(self, ground_truth_data_str, sample_data_str):
        if ground_truth_data_str is sample_data_str is None:
            self.fields_matched += 1
            self.fields_total += 1
        elif ground_truth_data_str is None:
            self.fields_total += len(sample_data_str)
        elif sample_data_str is None:
            self.fields_total += len(ground_truth_data_str)
        else:
            self.fields_total += 1
            self.fields_matched +=\
                1 if len(ground_truth_data_str) == len(sample_data_str) == 0\
                else SequenceMatcher(None, ground_truth_data_str, sample_data_str).ratio()

    def evaluate_accuracy(self, ground_truth_data, sample_data):
        self.type_evaluators[type(ground_truth_data)](ground_truth_data, sample_data)

def evaluate_accuracy(ground_truth_data, sample_data):
    evaluator = AccuracyEvaluator()
    evaluator.evaluate_accuracy(ground_truth_data, sample_data)

    return round(100*evaluator.fields_matched/evaluator.fields_total if evaluator.fields_total > 0 else 100, 2)
