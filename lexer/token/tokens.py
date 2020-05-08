from lexer.token.token_type import TokenType


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f'({self.row}:{self.column})'

    def print_location(self):
        return f'({self.row}:{self.column})'

    def copy(self):
        return Position(self.row, self.column)


class BaseToken:
    def __init__(self, type_: TokenType, pos_start: Position = None, pos_end: Position = None):
        self.type = type_
        self.pos_start = pos_start
        self.pos_end = pos_end

    # def __repr__(self):
    #     return f'TOKEN (Type: {self.type} {self.print_location()})'
    def __repr__(self):
        return f'{self.type}'

    def __eq__(self, other):
        return True if self.type == other.type else False

    def print_location(self):
        if self.pos_start is not None and self.pos_end is not None:
            return f'Pos_start: {self.pos_start.print_location()} Pos_end: {self.pos_end.print_location()}'
        return 'Unspecified position'


class ValueToken(BaseToken):
    def __init__(self, type_: TokenType, value, pos_start: Position = None, pos_end: Position = None):
        super().__init__(type_, pos_start, pos_end)
        self.value = value

    # def __repr__(self):
    #     return f'TOKEN (Type: {self.type} Value: {self.value} {self.print_location()})'

    def __repr__(self):
        return f'{self.type}:{self.value}'

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        return False


def create_token(token_type: TokenType, value, pos_start, pos_end):
    if token_type.has_value_field():
        return ValueToken(token_type, value, pos_start, pos_end)
    else:
        return BaseToken(token_type, pos_start, pos_end)
