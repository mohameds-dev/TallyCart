from django.test import TestCase
from django.core.management.base import CommandError
from products.management.commands.load_products_data import Command
from unittest.mock import patch
import tempfile
import os

class CommandHandleTest(TestCase):
    def setUp(self):
        self.command = Command()
        self.tempfile = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.tempfile_path = self.tempfile.name
        self._write_csv_content('store_product_id,product_name\n1,Apple\n2,Banana\n')

    def tearDown(self):
        self.tempfile.close()
        if os.path.exists(self.tempfile_path):
            os.unlink(self.tempfile_path)

    def _write_csv_content(self, content):
        with open(self.tempfile_path, 'w') as f:
            f.write(content)

    def test_add_arguments_adds_csv_file_argument(self):
        parser = self.command.create_parser('manage.py', 'load_products_data')
        self.command.add_arguments(parser)
        args = parser.parse_args(['load_products_data', 'some_file.csv'])

        self.assertEqual(args.csv_file, 'some_file.csv')

    def test_handle_raises_command_error_if_file_not_found(self):
        with self.assertRaises(CommandError):
            self.command.handle(csv_file='not_a_real_file.csv')

    def test_handle_calls_process_row_for_each_row(self):
        with patch.object(self.command, 'process_row') as mock_process_row:
            self.command.handle(csv_file=self.tempfile_path)

            self.assertEqual(mock_process_row.call_count, 2)

    def test_handle_writes_to_stderr_on_row_error(self):
        self._write_csv_content('store_product_id,product_name\n1,Apple\n')
        with patch.object(self.command, 'process_row', side_effect=Exception("fail")):
            with patch.object(self.command, 'stderr') as mock_stderr:
                self.command.handle(csv_file=self.tempfile_path)

                mock_stderr.write.assert_called()
