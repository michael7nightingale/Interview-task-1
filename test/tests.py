import unittest
from src import tables
from src import exceptions
from src import celebration_generator
from app import app



class TableMangerTest(unittest.TestCase):

    def open_success_csv(self):
        table = tables.CsvTableManager('data.csv')
        self.assertEqual(table.open_data(), None)

    # def open_fail_csv(self):
    #     table = tables.CsvTableManager()



