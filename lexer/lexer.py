import re
from typing import Match

from errors.error import LexerError
from lexer.regex_matched import MatchedToken
from lexer.source import Source, FileSource
from lexer.token.tokens import BaseToken, Position
from lexer.token.token_type import TokenType
from lexer.regex2token import regex2token


class Lexer:
    def __init__(self, source_: Source = None):
        self.source = source_
        self.position = Position(0, 0)
        self.regex2token: dict = init_regex2token()

    def get_tokens_from_next_line(self):
        line = self.source.read_line()
        tokens = self.get_tokens_from_line(line)
        self.position.row += 1
        return tokens

    def get_tokens_from_line(self, line):
        if line:
            tokens = self.lex_line(line)
        else:
            tokens = [BaseToken(TokenType.T_EOT, self.position)]
        return tokens

    def lex_line(self, line):
        self.position.column = 0
        tokens = []
        while self.position.column < len(line):
            token = self.find_token(line)
            if token.type is not TokenType.T_IGNORE:
                tokens.append(token)
        return tokens

    def find_token(self, line):
        try:
            matched_token = self._find_matching_token(line)
            return matched_token.create_token()
        except LexerError as e:
            print(f'Error: unexpected character: {e.illegal_char} at position: {e.position.print_location()}')
            exit(0)

    def _find_matching_token(self, line):
        for regex in self.regex2token:
            match: Match = regex.match(line, self.position.column)
            if match:
                m_tok = MatchedToken(self.regex2token[regex], match.group(0), self.position.copy(),
                                     Position(self.position.row, match.end(0)))
                self.position.column = match.end(0)
                return m_tok

        raise LexerError(line[self.position.column], self.position)


def init_regex2token():
    regex2token_compiled = {}
    for regex in regex2token:
        regex_compiled = re.compile(regex)
        regex2token_compiled[regex_compiled] = regex2token[regex]
    return regex2token_compiled


if __name__ == '__main__':
    source = FileSource('test_files/testfile3.txt')
    lexer = Lexer(source)
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
