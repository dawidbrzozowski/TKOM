from lexer.token.tokens import Position


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position):
        self.illegal_char = illegal_char
        self.position = position

    def print_error_and_exit(self):
        print(f'Error: unexpected character: {self.illegal_char} at position: {self.position.print_location()}')
        exit(0)


class InvalidSyntaxError(Exception):
    def __init__(self, position: Position, message):
        self.pos_start = position
        self.message = message

    def print_error_and_exit(self):
        print(f'Error: invalid syntax at: {self.pos_start}. {self.message}')
        exit(0)
