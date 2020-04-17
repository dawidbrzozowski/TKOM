from lexer.token.tokens import BaseToken, ValueToken
from lexer.token.token_type import TokenType


class MatchedToken:
    def __init__(self, token_type, value, start_pos, end_pos):
        self.token_type: TokenType = token_type
        self.value = value
        self.pos_start = start_pos
        self.pos_end = end_pos

    def create_token(self):
        if self.token_type.has_value_field():
            return ValueToken(self.token_type, self.value, self.pos_start, self.pos_end)
        else:
            return BaseToken(self.token_type, self.pos_start, self.pos_end)
