from enum import Enum
import re

class TokenType(Enum):
    BRACE_LEFT = 0      # {
    BRACE_RIGHT = 1     # }
    BRACKET_LEFT = 2    # [
    BRACKET_RIGHT = 3   # ]
    COLON = 4           # :
    COMMA = 5           # ,
    LITERAL = 6         # true false null
    NUMBER = 8          # 666
    STRING = 9          # "benfica"

class Token:

    def __init__(self, tokenType, content = None):
        self.tokenType = tokenType
        self.content = content

    def __repr__(self):
        return "<{0} {1}>".format(self.tokenType, self.content) if self.content else "<{0}>".format(self.tokenType)

    def __eq__(self, other):
        return self.tokenType == other.tokenType and self.content == other.content

class Tokenizer(object):

    def __init__(self, string):
        self.string = string.strip()
        self.cursor = 0
        self.tokens = []

    # returns the next token in the string
    def __next(self):

        # are we done?
        if not self.cursor < len(self.string):
            return None

        # skip whitespace characters
        while self.string[self.cursor].isspace():
            self.cursor = self.cursor + 1

        # tokenize structural characters
        looking_at = self.string[self.cursor]
        if looking_at == '{':
            token = Token(TokenType.BRACE_LEFT)
            self.cursor = self.cursor + 1
            return token

        elif looking_at == '}':
            token = Token(TokenType.BRACE_RIGHT)
            self.cursor = self.cursor + 1
            return token

        elif looking_at == '[':
            token = Token(TokenType.BRACKET_LEFT)
            self.cursor = self.cursor + 1
            return token

        elif looking_at == ']':
            token = Token(TokenType.BRACKET_RIGHT)
            self.cursor = self.cursor + 1
            return token

        elif looking_at == ':':
            token = Token(TokenType.COLON)
            self.cursor = self.cursor + 1
            return token

        elif looking_at == ',':
            token = Token(TokenType.COMMA)
            self.cursor = self.cursor + 1
            return token

        # tokenize literal symbols
        elif self.string[self.cursor : self.cursor + 4] == 'null':
            token = Token(TokenType.LITERAL, 'null')
            self.cursor = self.cursor + 4
            return token

        elif self.string[self.cursor : self.cursor + 4] == 'true':
            token = Token(TokenType.LITERAL, 'true')
            self.cursor = self.cursor + 4
            return token

        elif self.string[self.cursor : self.cursor + 5] == 'false':
            token = Token(TokenType.LITERAL, 'false')
            self.cursor = self.cursor + 5
            return token

        # numbers and strings are the hardest
        # try to find a number
        match = re.match(r'-?[0-9]+', self.string[self.cursor:])
        if match:
            matched_text = match.group(0)
            token = Token(TokenType.NUMBER, matched_text)
            self.cursor = self.cursor + len(matched_text)
            return token

        # try strings
        # cheats: http://stackoverflow.com/questions/249791/regex-for-quoted-string-with-escaping-quotes
        match = re.match(r'"(?:[^"\\]|\\.)*"', self.string[self.cursor:])
        if match:
            matched_text = match.group(0)
            token = Token(TokenType.STRING, matched_text)
            self.cursor = self.cursor + len(matched_text)
            return token

        # it should never reach this point when tokenizing, so throw exception
        raise ValueError("Error tokenizing input")

    def tokenize(self):
        #print "Tokenizing..."
        while True:
            token = self.__next()
            if token is None:
                break

            #print "__next() returns", token
            self.tokens.append(token)

        return self.tokens
