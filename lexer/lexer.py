import re

from errors.error import LexerException
from lexer.regex_matched import MatchedToken
from lexer.source import Source, FileSource
from token.token import Token
from token.token_type import TokenType
from lexer.regex2token import regex2token


def init_regex2token():
    regex2token_compiled = {}
    for regex in regex2token:
        regex_compiled = re.compile(regex)
        regex2token_compiled[regex_compiled] = regex2token[regex]
    return regex2token_compiled


class Lexer:
    def __init__(self, source_: Source = None):
        self.source = source_
        self.column = 0
        self.row = 0
        self.regex2token: dict = init_regex2token()

    def get_tokens_from_next_line(self):
        line = self.source.read_line()
        return self.get_tokens_from_line(line)

    def get_tokens_from_line(self, line):
        if line:
            tokens = self.lex_line(line)
        else:
            tokens = [Token(TokenType.T_EOT)]
        return tokens

    def lex_line(self, line):
        self.column = 0
        tokens = []
        while self.column < len(line):
            token = self.find_token(line)
            if token:
                if token.type is not TokenType.T_IGNORE:
                    tokens.append(token)
            else:
                raise LexerException(line[self.column], self.row, self.column)
        self.row += 1
        return tokens

    def find_token(self, line):
        token = self.get_token(line)
        return token

    def get_token(self, line):
        try:
            matched_token = self._find_matching_token(line)
            return matched_token.get_token()
        except LexerException:
            print(LexerException)
            exit(0)

    def _find_matching_token(self, line):
        for regex in self.regex2token:
            match = regex.match(line, self.column)
            if match:
                self.column = match.end(0)
                return MatchedToken(self.regex2token[regex], match.group(0))
        raise LexerException(line[self.column], self.row, self.column)


if __name__ == '__main__':
    source = FileSource('test_files/testfile3.txt')
    lexer = Lexer(source)
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
