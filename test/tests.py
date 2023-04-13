import unittest
from src import tables
from src import exceptions


class CsvTableManagerTest(unittest.TestCase):
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
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_column(column_name='test_add',
                                          column_data=range(len(table.data)),
                                          nullable=False
                                          ), None)

    def test_add_column_nullable_success(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_column(column_name='test_add',
                                          column_data=range(len(table.data) - 1),
                                          nullable=True), None)

    def test_add_column_error(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.AddColumnException):
            table.add_column(column_name='test_add',
                             column_data=['hello'],
                             nullable=False)

    def test_get_column_data_success(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.get_column_data(column_name='name'), ("андрей", 'максим', 'анжелика', 'анна'))

    def test_get_column_data_error(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.get_column_data(column_name='ot_exists')

    def test_add_line_success(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_line(line_data=range(len(table.columns)),
                                        nullable=False), None)

    def test_add_line_nullable_success(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_line(line_data=range(len(table.columns) - 1),
                                        nullable=True), None)

    def test_add_line_error(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.AddLineException):
            table.add_line(line_data=['hello', ],
                           nullable=False)

    def test_delete_column_success(self):
        table = tables.CsvTableManager('data.csv', delete_mode=True)
        table.open_data()
        table.delete_column(column_name='name')
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.get_column_data(column_name='name')

    def test_delete_mode_false(self):
        table = tables.CsvTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.DeletingModeException):
            table.delete_column(column_name='name')

    def test_delete_column_error(self):
        table = tables.CsvTableManager('data.csv', delete_mode=True)
        table.open_data()
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.delete_column(column_name='javascript_sucks')

class PandasTableManagerTest(unittest.TestCase):
    def test_create_table_success(self):
        table = tables.PandasTableManager('data.csv')
        self.assertIsInstance(table, tables.PandasTableManager)

    def test_create_table_error(self):
        with self.assertRaises(exceptions.FileExtensionError) as e:
            table = tables.PandasTableManager('data.xml')

    def test_open_success(self):
        table = tables.PandasTableManager('data.csv')
        self.assertEqual(table.open_data(), None)

    def test_save(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.save_data(), None)

    def test_add_column_success(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_column(column_name='test_add',
                                          column_data=range(len(table.data)),
                                          nullable=False
                                          ), None)

    def test_add_column_nullable_success(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_column(column_name='test_add',
                                          column_data=range(len(table.data) - 1),
                                          nullable=True), None)

    def test_add_column_error(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.AddColumnException):
            table.add_column(column_name='test_add',
                             column_data=['hello'],
                             nullable=False)

    def test_get_column_data_success(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.get_column_data(column_name='name'), ("андрей", 'максим', 'анжелика', 'анна'))

    def test_get_column_data_error(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.get_column_data(column_name='ot_exists')

    def test_add_line_success(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_line(line_data=range(len(table.columns)),
                                        nullable=False), None)

    def test_add_line_nullable_success(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        self.assertEqual(table.add_line(line_data=range(len(table.columns) - 1),
                                        nullable=True), None)

    def test_add_line_error(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.AddLineException):
            table.add_line(line_data=['hello', ],
                           nullable=False)

    def test_delete_column_success(self):
        table = tables.PandasTableManager('data.csv', delete_mode=True)
        table.open_data()
        table.delete_column(column_name='name')
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.get_column_data(column_name='name')

    def test_delete_mode_false(self):
        table = tables.PandasTableManager('data.csv')
        table.open_data()
        with self.assertRaises(exceptions.DeletingModeException):
            table.delete_column(column_name='name')

    def test_delete_column_error(self):
        table = tables.PandasTableManager('data.csv', delete_mode=True)
        table.open_data()
        with self.assertRaises(exceptions.ColumnDoesNotExists):
            table.delete_column(column_name='javascript_sucks')