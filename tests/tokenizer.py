# run me with python -m unittest tests.tokenizer.TestTokenizer

import unittest
from lib.tokenizer import Tokenizer, Token, TokenType

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

class TestTokenizer(unittest.TestCase):

    def test_number(self):
        sample = """
            666
        """
        tokenizer = Tokenizer(sample)
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token(TokenType.NUMBER, '666'))

    def test_string(self):
        sample = """
            "xyzzy" "foobar"
        """
        tokenizer = Tokenizer(sample)
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0], Token(TokenType.STRING, '"xyzzy"'))
        self.assertEqual(tokens[1], Token(TokenType.STRING, '"foobar"'))

    def test_string_with_quotes(self):
        sample = r"""
            "xyzzy is a \"word\"" "foobar is a \"word\" too"
        """
        tokenizer = Tokenizer(sample)
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0], Token(TokenType.STRING, r'"xyzzy is a \"word\""'))
        self.assertEqual(tokens[1], Token(TokenType.STRING, r'"foobar is a \"word\" too"'))


    def test_literal(self):
        sample = """
            true false null
        """
        tokenizer = Tokenizer(sample)
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0], Token(TokenType.LITERAL, 'true'))
        self.assertEqual(tokens[1], Token(TokenType.LITERAL, 'false'))
        self.assertEqual(tokens[2], Token(TokenType.LITERAL, 'null'))

    def test_mixed(self):
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
        tokenizer = Tokenizer(sample)
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 47)
        expected_values = [
            Token(TokenType.BRACE_LEFT),
            Token(TokenType.STRING, '"yes"'),
            Token(TokenType.COLON),
            Token(TokenType.LITERAL, 'true'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"no"'),
            Token(TokenType.COLON),
            Token(TokenType.LITERAL, 'false'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"nothing"'),
            Token(TokenType.COLON),
            Token(TokenType.LITERAL, 'null'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"number"'),
            Token(TokenType.COLON),
            Token(TokenType.NUMBER, '123'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"negative_number"'),
            Token(TokenType.COLON),
            Token(TokenType.NUMBER, '-123'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"strings"'),
            Token(TokenType.COLON),
            Token(TokenType.STRING, r'"A \"string\".\nFor real."'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"object"'),
            Token(TokenType.COLON),
            Token(TokenType.BRACE_LEFT),
            Token(TokenType.STRING, '"omg"'),
            Token(TokenType.COLON),
            Token(TokenType.STRING, '"things"'),
            Token(TokenType.BRACE_RIGHT),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"list"'),
            Token(TokenType.COLON),
            Token(TokenType.BRACKET_LEFT),
            Token(TokenType.NUMBER, '1'),
            Token(TokenType.COMMA),
            Token(TokenType.STRING, '"a"'),
            Token(TokenType.COMMA),
            Token(TokenType.BRACE_LEFT),
            Token(TokenType.BRACE_RIGHT),
            Token(TokenType.COMMA),
            Token(TokenType.BRACKET_LEFT),
            Token(TokenType.BRACKET_RIGHT),
            Token(TokenType.BRACKET_RIGHT),
            Token(TokenType.BRACE_RIGHT)
        ]
        self.assertEqual(len(expected_values), 47)
        self.assertEqual(len(tokens), 47)
        for i in range(0, len(expected_values)):
            self.assertEqual(tokens[i], expected_values[i])
