class AccuracyEvaluator:
    def __init__(self):
        self.fields_matched = 0
        self.fields_total = 0
        self.type_evaluators = {
            dict: self.evaluate_accuracy_dict,
            list: self.evaluate_accuracy_list,
            # str: self.evaluate_accuracy_str,
        }

    def evaluate_accuracy_primitive(self, ground_truth_data, sample_data):
        self.fields_total += 1
        if ground_truth_data == sample_data:
            self.fields_matched += 1

    def evaluate_accuracy_dict(self, ground_truth_data, sample_data):
        for key, value in ground_truth_data.items():
            if type(value) in self.type_evaluators:
                self.type_evaluators[type(value)](value, sample_data[key])
            else:
                self.evaluate_accuracy_primitive(value, sample_data.get(key, None))

        self.fields_total += len(sample_data) - len(set(sample_data.keys()).intersection(set(ground_truth_data.keys())))

    def evaluate_accuracy_list(self, ground_truth_data, sample_data):
        for i in range(len(ground_truth_data)):
            if type(ground_truth_data[i]) in self.type_evaluators:
                self.type_evaluators[type(ground_truth_data[i])](ground_truth_data[i], sample_data[i])
            else:
                self.evaluate_accuracy_primitive(ground_truth_data[i], sample_data[i])

    def evaluate_accuracy(self, ground_truth_data, sample_data):
        self.type_evaluators[type(ground_truth_data)](ground_truth_data, sample_data)

def evaluate_accuracy(ground_truth_data, sample_data):
    evaluator = AccuracyEvaluator()
    evaluator.evaluate_accuracy(ground_truth_data, sample_data)
    return round(100*evaluator.fields_matched/evaluator.fields_total if evaluator.fields_total > 0 else 100, 2)
