import unittest
from src import tables
from src import exceptions


class CstTableManagerTest(unittest.TestCase):
    def test_create_table_success(self):
        table = tables.CsvTableManager('data.csv')
        self.assertIsInstance(table, tables.CsvTableManager)

    def test_create_table_error(self):
        with self.assertRaises(exceptions.FileExtensionError) as e:
            table = tables.CsvTableManager('data.xml')

    def test_open_success(self):
        table = tables.CsvTableManager('data.csv')
        self.assertEqual(table.open_data(), None)

    def test_save(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.save_data(), None)

    def test_add_column_success(self):
        pass

    def test_add_column_error(self):
        pass

    def test_get_column_data_success(self):
        pass

    def test_get_column_data_error(self):
        pass

    def test_add_line_success(self):
        pass

    def test_add_line_error(self):
        pass

    def test_delete_column_success(self):
        pass

    def test_delete_column_error(self):
        pass