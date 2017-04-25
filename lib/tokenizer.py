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

    # looks at the string. pass None to look from the current to the end
    def __look(self, count = 1):
        if count is None:
            return self.string[self.cursor :]
        else:
            return self.string[self.cursor : self.cursor + count]

    # advances the cursor
    def __advance(self, count = 1):
        self.cursor = self.cursor + count

    # returns a new token and advances the cursor
    def __pop_token(self, tokenType, content = None):
        token = Token(tokenType, content)

        if content is not None:
            count = len(content)
        else:
            count = 1

        self.__advance(count)

        return token


    # returns the next token in the string
    def __next(self):

        # are we done?
        if not self.cursor < len(self.string):
            return None

        # skip whitespace characters
        while self.__look().isspace():
            self.__advance()

        # tokenize structural characters
        if self.__look() == '{':
            return self.__pop_token(TokenType.BRACE_LEFT)
        elif self.__look() == '}':
            return self.__pop_token(TokenType.BRACE_RIGHT)
        elif self.__look() == '[':
            return self.__pop_token(TokenType.BRACKET_LEFT)
        elif self.__look() == ']':
            return self.__pop_token(TokenType.BRACKET_RIGHT)
        elif self.__look() == ':':
            return self.__pop_token(TokenType.COLON)
        elif self.__look() == ',':
            return self.__pop_token(TokenType.COMMA)

        # tokenize literal symbols
        elif self.__look(4) == 'null':
            return self.__pop_token(TokenType.LITERAL, 'null')
        elif self.__look(4) == 'true':
            return self.__pop_token(TokenType.LITERAL, 'true')
        elif self.__look(5) == 'false':
            return self.__pop_token(TokenType.LITERAL, 'false')

        # numbers and strings are the hardest
        else:

            # try to find a number
            match = re.match(r'-?[0-9]+', self.__look(None))
            if match:
                matched_text = match.group(0)
                return self.__pop_token(TokenType.NUMBER, matched_text)

            # try strings
            # cheats: http://stackoverflow.com/questions/249791/regex-for-quoted-string-with-escaping-quotes
            match = re.match(r'"(?:[^"\\]|\\.)*"', self.__look(None))
            if match:
                matched_text = match.group(0)
                return self.__pop_token(TokenType.STRING, matched_text)

            # it should never reach this point when tokenizing, so throw exception
            raise ValueError("Error tokenizing input")

    # call this to tokenize the string given to the class
    def tokenize(self):

        while True:
            token = self.__next()
            if token is None:
                break
            self.tokens.append(token)

        return self.tokens
