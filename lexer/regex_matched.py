from token.token import Token
from token.token_type import TokenType


class MatchedToken:
    def __init__(self, token_type, value):
        self.token_type:TokenType = token_type
        self.value = value

    def get_token(self):
        if self.token_type.has_value_field():
            return Token(self.token_type, self.value)
        else:
            return Token(self.token_type)