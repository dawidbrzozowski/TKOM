from lexer.token_type import TokenType


class Token:
    def __init__(self, type_: TokenType, value=None, row=None):
        self.type = type_
        self.value = value
        self.row = row

    def __repr__(self):
        if self.value:
            return f'TOKEN (Type: {self.type} Value: {self.value})'
        else:
            return f'TOKEN (Type: {self.type})'

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False

