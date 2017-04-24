from lib.tokenizer import Tokenizer, TokenType

# Context-free grammar to implement (adapted from https://github.com/antlr/grammars-v4/blob/master/json/JSON.g4)
#
# jayson   -> value
#
# value    -> STRING
#             NUMBER
#             LITERAL
#             object
#             array
#
# object   -> BRACE_LEFT pair (COMMA pair)* BRACE_RIGHT
#          -> BRACE_LEFT BRACE_RIGHT
#
# pair     -> STRING COLON value
#
# array    -> BRACKET_LEFT value (COMMA value)* BRACKET_RIGHT
#          -> BRACKET_LEFT BRACKET_RIGHT

class Parser:

    def __init__(self, input):
        self.input = input

        # tokenize input
        tokenizer = Tokenizer(self.input)
        self.tokens = tokenizer.tokenize()

    def __repr__(self):
        return self.tokens

    def __peek(self, pos = 0):
        return self.tokens[pos].tokenType

    def __next(self):
        return self.tokens.pop(0)


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
            raise ValueError("Panic!")


    def __parse_string(self):
        token = self.__next()
        assert(token.tokenType == TokenType.STRING)
        return token.content[1:-1]

    def __parse_number(self):
        token = self.__next()
        assert(token.tokenType == TokenType.NUMBER)
        return int(token.content)

    def __parse_literal(self):
        token = self.__next()
        assert(token.tokenType == TokenType.LITERAL)

        if token.content == 'true':
            return True
        elif token.content == 'false':
            return False
        elif token.content == 'null':
            return None
        else:
            raise ValueError("Panic!")

    def __parse_object(self):

        # open the object
        token = self.__next()
        assert(token.tokenType == TokenType.BRACE_LEFT)

        # check if empty object
        if self.__peek() == TokenType.BRACE_RIGHT:
            self.__next()
            return {}

        # iterate over all pairs of this object
        the_object = {}
        while True:
            key = self.__parse_string()

            token = self.__next()
            assert(token.tokenType == TokenType.COLON)

            value = self.__parse_value()

            the_object[key] = value

            if (self.__peek() == TokenType.BRACE_RIGHT): # we done here
                self.__next()
                break
            elif (self.__peek() == TokenType.COMMA): # next
                self.__next()
                continue
            else:
                raise ValueError("Panic!")

        return the_object

    def __parse_array(self):
        the_array = []

        # open the array
        token = self.__next()
        assert(token.tokenType == TokenType.BRACKET_LEFT)

        # check if empty array
        if self.__peek() == TokenType.BRACKET_RIGHT:
            self.__next()
            return []

        # iterate over all items of this array
        while True:
            element = self.__parse_value()
            the_array.append(element)

            if (self.__peek() == TokenType.BRACKET_RIGHT): # we done here
                self.__next()
                break
            elif (self.__peek() == TokenType.COMMA): # next
                self.__next()
                continue
            else:
                raise ValueError("Panic!")

        return the_array

    def parse(self):
        return self.__parse_value()
