from unittest import TestCase
from receipts.utils.json_accuracy_evaluator import evaluate_accuracy

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

    def test_evaluate_accuracy_takes_two_dicts_with_many_nested_fields_and_returns_correct_value(self):
        ground_truth_data = {
            'dict1': {
                'key1': 10,
                'key2': 20,
                'dict2': {
                    'key3': 30,
                    'key4': 40
                }
            },
            'list1': [10, 20, 30],
            'list2': ['abc', 'def', 20],
            'list3': [10, 20, {}],
            'str1': 'Hello, world!',
            'str2': 'Hello, world!',
        }

        sample_data = {
            'dict1': {
                'key1': 10,
                'key2': 20,
                'dict2': {
                    'key3': 30,
                    'key4': 40
                }
            },
            'str2': 'Hello, people!',
        }

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 26.34)

    def test_evaluate_accuracy_takes_two_identical_large_dicts_and_returns_100(self):
        ground_truth_data = {
            'product_name': 'Product Name',
            'price_snapshots':[
                {'price': 100, 'date': '2021-01-01', 'time': '12:00:00', 'shop_name': 'Shop Name1'},
                {'price': 100, 'date': '2021-01-02', 'time': '12:00:00', 'shop_name': 'Shop Name2'},
                {'price': 101, 'date': '2021-01-03', 'time': '12:00:00', 'shop_name': 'Shop Name1'},
                {'price': 102, 'date': '2021-01-04', 'time': '12:00:00', 'shop_name': 'Shop Name2'},
                {'price': 103, 'date': '2021-01-05', 'time': '12:00:00', 'shop_name': 'Shop Name1'},
                {'price': 104, 'date': '2021-01-06', 'time': '12:00:00', 'shop_name': 'Shop Name2'},
                {'price': 105, 'date': '2021-01-07', 'time': '12:00:00', 'shop_name': 'Shop Name1'},
                {'price': 106, 'date': '2021-01-08', 'time': '12:00:00', 'shop_name': 'Shop Name2'},
                {'price': 107, 'date': '2021-01-09', 'time': '12:00:00', 'shop_name': 'Shop Name1'},
                {'price': 108, 'date': '2021-01-10', 'time': '12:00:00', 'shop_name': 'Shop Name2'},
            ],
            'tags': ['tag1', 'tag2', 'tag3'],
        }
        sample_data = ground_truth_data.copy()

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 100)

    def test_evaluate_accuracy_takes_two_dicts_half_matching_and_returns_50(self):
        ground_truth_data = {'key1': 10, 'key2': 20, 'key3': 30, 'key4': 40}
        sample_data = {'key1': 10, 'key2': 20, 'key3': 40, 'key4': 50}

        self.assertEqual(evaluate_accuracy(ground_truth_data, sample_data), 50)
