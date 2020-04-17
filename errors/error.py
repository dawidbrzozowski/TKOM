from lexer.token.tokens import Position


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position):
        self.illegal_char = illegal_char
        self.position = position


def print_error_and_exit(error: LexerError):
    print(f'Error: unexpected character: {error.illegal_char} at position: {error.position.print_location()}')
    exit(0)
