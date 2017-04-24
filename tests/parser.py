# run me with python -m unittest tests.parser.TestParser

import unittest
from lib.parser import Parser

class TestParser(unittest.TestCase):

    def test_number(self):
        sample = """
            666
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertEqual(result, 666)

    def test_true(self):
        sample = """
            true
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertEqual(result, True)

    def test_false(self):
        sample = """
            false
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertEqual(result, False)

    def test_null(self):
        sample = """
            null
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertEqual(result, None)

    def test_array(self):
        sample = """
            []
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertListEqual(result, [])
