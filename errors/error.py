from lexer.token.tokens import Position


class LexerError(Exception):
    def __init__(self, illegal_char, position: Position):
        self.illegal_char = illegal_char
        self.position = position
