from unittest import TestCase
from utils.json_accuracy_evaluator import evaluate_accuracy

class TestJsonAccuracyEvaluator(TestCase):
    def test_evaluate_accuracy_takes_two_empty_dicts_and_returns_100(self):
        ground_truth_data = dict()
        sample_data = dict()

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_dicts_with_same_keys_and_returns_100(self):
        ground_truth_data = {'key1': 10, 'key2': 20}
        sample_data = {'key1': 10, 'key2': 20}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_dicts_with_different_keys_and_returns_0(self):
        ground_truth_data = {'key1': 10, 'key2': 20}
        sample_data = {'key3': 10, 'key4': 30}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 0)

    def test_evaluate_accuracy_takes_two_dicts_with_different_values_and_returns_0(self):
        ground_truth_data = {'key1': 10, 'key2': 20}
        sample_data = {'key1': 20, 'key2': 30}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 0)
    
    def test_evaluate_accuracy_takes_two_dicts_with_one_out_of_two_entries_matching_and_returns_50(self):
        ground_truth_data = {'key1': 10, 'key2': 20}
        sample_data = {'key1': 10}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 50)

    def test_evaluate_accuracy_takes_sample_data_with_one_of_three_entries_and_returns_33_percent(self):
        ground_truth_data = {'key1': 10, 'key2': 20, 'key3': 30}
        sample_data = {'key1': 10}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 33.33)

    def test_evaluate_accuracy_takes_sample_data_with_two_of_three_entries_and_returns_66_percent(self):
        ground_truth_data = {'key1': 10, 'key2': 20, 'key3': 30}
        sample_data = {'key1': 10, 'key2': 20}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 66.67)

    def test_evaluate_accuracy_takes_sample_data_with_3_entries_containing_1_extra_entry_and_returns_66_percent(self):
        ground_truth_data = {'key1': 10, 'key2': 20}
        sample_data = {'key1': 10, 'key2': 20, 'key3': 30}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 66.67)

    def test_evaluate_accuracy_takes_sample_data_with_3_entries_containing_2_extra_entries_and_returns_33_percent(self):
        ground_truth_data = {'key1': 10}
        sample_data = {'key1': 10, 'key2': 20, 'key3': 30}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 33.33)

    def test_evaluate_accuracy_takes_two_dicts_with_one_entry_being_a_matching_dict_and_returns_100(self):
        ground_truth_data = {'key1': {'key11': 10, 'key12': 20}}
        sample_data = {'key1': {'key11': 10, 'key12': 20}}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_dicts_with_one_entry_being_a_partially_matching_dict_and_returns_50(self):
        ground_truth_data = {'key1': {'key11': 10, 'key12': 20}}
        sample_data = {'key1': {'key11': 10}}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 50)

    def test_evaluate_accuracy_takes_two_dicts_containing_matching_lists_and_returns_100(self):
        ground_truth_data = {'key1': [10, 20]}
        sample_data = {'key1': [10, 20]}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_dicts_containing_partially_matching_lists_and_returns_50(self):
        ground_truth_data = {'key1': [10, 20]}
        sample_data = {'key1': [10, 30]}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 50)
