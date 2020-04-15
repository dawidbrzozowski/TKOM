from lexer.token_type import TokenType


class Token:
    def __init__(self, type_: TokenType, value, row=None):
        self.type = type_
        self.value = value
        self.row = row
