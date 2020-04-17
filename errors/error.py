class LexerException(Exception):
    def __init__(self, illegal_char, row: int, column:int):
        self.illegal_char = illegal_char
        self.row = row
        self.column = column

    def __repr__(self):
        return f'Token not found for: {self.illegal_char}. Row: {self.row}. Column: {self.column}'
