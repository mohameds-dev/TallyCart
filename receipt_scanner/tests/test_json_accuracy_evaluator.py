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

    def test_evaluate_accuracy_takes_two_empty_lists_and_returns_100(self):
        ground_truth_data = []
        sample_data = []

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_empty_ground_truth_data_and_non_empty_sample_data_and_returns_0(self):
        ground_truth_data = []
        sample_data = [10, 20]

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 0)

    def test_evaluate_accuracy_takes_two_lists_with_two_elements_swapped_and_returns_0(self):
        ground_truth_data = [10, 20]
        sample_data = [20, 10]

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 0)

    def test_evaluate_accuracy_takes_two_lists_with_one_correct_and_one_misplaced_entry_and_returns_50_percent(self):
        ground_truth_data = [10, 30]
        sample_data = [10, 20, 30]

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 50)

    def test_evaluate_accuracy_takes_two_equal_strings_and_returns_100(self):
        ground_truth_data = 'Hello, world!'
        sample_data = 'Hello, world!'

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_empty_strings_and_returns_100(self):
        self.assertEqual(evaluate_accuracy('', ''), 100)

    def test_evaluate_accuracy_takes_a_70_percent_complete_sample_string_and_returns_70(self):
        ground_truth_data = 'Hello, world!'
        sample_data = 'Hello, '

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 70)

    def test_evaluate_accuracy_takes_lists_with_dicts_with_3_entries_containing_2_extra_entries_and_returns_33_percent(self):
        ground_truth_data = [{'key1': 10}]
        sample_data = [{'key1': 10, 'key2': 20, 'key3': 30}]

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 33.33)
