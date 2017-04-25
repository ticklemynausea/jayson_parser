from lib.tokenizer import Tokenizer, TokenType

# Context-free grammar to implement
# adapted from https://github.com/antlr/grammars-v4/blob/master/json/JSON.g4)
#
# jayson   -> value
#
# value    -> STRING
#             NUMBER
#             LITERAL
#             object
#             array
#
# object   -> BRACE_LEFT STRING COLON value (COMMA STRING COLON value)* BRACE_RIGHT
#          -> BRACE_LEFT BRACE_RIGHT
#
# array    -> BRACKET_LEFT value (COMMA value)* BRACKET_RIGHT
#          -> BRACKET_LEFT BRACKET_RIGHT

#
# Recursive descent parser class
class Parser:

    def __init__(self, input):
        self.input = input

        # tokenize input
        tokenizer = Tokenizer(self.input)
        self.tokens = tokenizer.tokenize()

    # returns the type of the next token
    def __peek(self):
        return self.tokens[0].tokenType

    # returns the next token, optionally asserting its type
    def __next(self, tokenType = None):
        token = self.tokens.pop(0)
        if tokenType is not None:
            assert(token.tokenType == tokenType)
        return token

    # skips the next token if it is of the given type
    def __skip(self, tokenType):
        if self.__peek() == tokenType:
            self.__next(tokenType) # such redundant checks...
            return True
        else:
            return False

    # parse `value` non-terminator symbol
    def __parse_value(self):
        if self.__peek() == TokenType.STRING:
            return self.__parse_string()
        elif self.__peek() == TokenType.NUMBER:
            return self.__parse_number()
        elif self.__peek() == TokenType.LITERAL:
            return self.__parse_literal()
        elif self.__peek() == TokenType.BRACE_LEFT:
            return self.__parse_object()
        elif self.__peek() == TokenType.BRACKET_LEFT:
            return self.__parse_array()
        else:
            raise ValueError("Panic! Expected {0}, {1}, {2}, {3} or {4}, got {5} instead".format(TokenType.STRING,
                TokenType.NUMBER, TokenType.LITERAL, TokenType.BRACE_RIGHT, TokenType.BRACKET_LEFT, self.__peek()))

    # parse `STRING` terminator
    def __parse_string(self):
        token = self.__next()
        assert(token.tokenType == TokenType.STRING)
        return token.content[1:-1].decode('string_escape')

    # parse `NUMBER` terminator
    def __parse_number(self):
        token = self.__next(TokenType.NUMBER)
        return int(token.content)

    # parse `LITERAL` terminator
    def __parse_literal(self):
        token = self.__next(TokenType.LITERAL)

        if token.content == 'true':
            return True
        elif token.content == 'false':
            return False
        elif token.content == 'null':
            return None
        else:
            # the tokenizer should never let a literal have other values, unimportant error message
            raise ValueError("Panic! Impossible situation!")

    # parse `object` non-terminator
    def __parse_object(self):

        # open the object
        token = self.__next(TokenType.BRACE_LEFT)

        # check if empty object
        if self.__skip(TokenType.BRACE_RIGHT):
            return {}

        # iterate over all pairs of this object
        result = {}
        while True:
            key = self.__parse_string()

            token = self.__next(TokenType.COLON)

            value = self.__parse_value()

            result[key] = value

            if self.__skip(TokenType.BRACE_RIGHT): # we done here
                break
            elif self.__skip(TokenType.COMMA): # next
                continue
            else:
                raise ValueError("Panic! Expected {0} or {1}, got {2} instead".format(TokenType.BRACE_RIGHT,
                    TokenType.COMMA, self.__peek()))

        return result

    # parse `array` non-terminator
    def __parse_array(self):

        # open the array
        token = self.__next(TokenType.BRACKET_LEFT)

        # check if empty array
        if self.__skip(TokenType.BRACKET_RIGHT):
            return []

        # iterate over all items of this array
        result = []
        while True:
            element = self.__parse_value()
            result.append(element)

            if self.__skip(TokenType.BRACKET_RIGHT): # we done here
                break
            elif self.__skip(TokenType.COMMA): # next
                continue
            else:
                raise ValueError("Panic! Expected {0} or {1}, got {2} instead".format(TokenType.BRACKET_RIGHT,
                    TokenType.COMMA, self.__peek()))

        return result

    # evaluate the python equivalent of the given jayson string
    def parse(self):
        return self.__parse_value()
