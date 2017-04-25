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

    def test_empty_array(self):
        sample = """
            []
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertListEqual(result, [])

    def test_simple_array(self):
        sample = """
            [1,2,3,"go!"]
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertListEqual(result, [1, 2, 3, 'go!'])

    def test_empty_object(self):
        sample = """
            {}
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertDictEqual(result, {})

    def test_simple_object(self):
        sample = """
            {"um":1, "dois":2}
        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertDictEqual(result, { 'um': 1, 'dois': 2 })


    def test_given_example(self):
        sample = r"""
            {
                "yes": true,
                "no": false,
                "nothing": null,
                "number": 123,
                "negative_number": -123,
                "strings": "A \"string\".\nFor real.",
                "object": {"omg": "things"},
                "list": [1, "a", {}, []]
            }

        """
        parser = Parser(sample)
        result = parser.parse()

        self.assertDictEqual(result, { 'yes': True, 'no': False, 'nothing': None, 'number': 123, \
            'negative_number': -123, 'strings': 'A \"string\".\nFor real.', 'object': \
            { 'omg': 'things' }, 'list': [1, 'a', {}, []] })
