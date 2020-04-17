from errors.error import LexerError
from lexer.source import Source, FileSource
from lexer.token.tokens import BaseToken, Position, create_token
from lexer.token.token_type import TokenType
from lexer.regex2token import compile_regex2token
from errors.error import print_error_and_exit


class Lexer:
    def __init__(self, source_: Source = None):
        self.source = source_
        self.position = Position(0, 0)
        self.regex2token = compile_regex2token()

    def get_tokens_from_file(self):
        tokens_from_file = []
        while True:
            tokens = self._get_tokens_from_next_line()
            if tokens[0] == BaseToken(TokenType.T_EOT):
                break
            tokens_from_file.append(tokens)
        return tokens_from_file

    def _get_tokens_from_next_line(self):
        line = self.source.read_line()
        tokens = self._get_tokens_from_line(line)
        self.position.row += 1
        return tokens

    def _get_tokens_from_line(self, line):
        if line:
            tokens = self._lex_line(line)
        else:
            tokens = [BaseToken(TokenType.T_EOT, self.position)]
        return tokens

    def _lex_line(self, line):
        self.position.column = 0
        tokens = []
        while self.position.column < len(line):
            token = self._find_next_token_in_line(line)
            if token.type is not TokenType.T_IGNORE:
                tokens.append(token)
            self.position.column = token.pos_end.column
        return tokens

    def _find_next_token_in_line(self, line):
        try:
            return self._find_matching_token(line)
        except LexerError as e:
            print_error_and_exit(e)

    def _find_matching_token(self, line):
        for regex in self.regex2token:
            match = regex.match(line, self.position.column)
            if match:
                token_type = self.regex2token[regex]
                value = match.group(0)
                pos_start = self.position.copy()
                pos_end = Position(self.position.row, match.end(0))
                matching_token = create_token(token_type, value, pos_start, pos_end)
                return matching_token

        raise LexerError(line[self.position.column], self.position)


if __name__ == '__main__':
    source = FileSource('test_files/testfile2lines.txt')
    lexer = Lexer(source)
    print(lexer.get_tokens_from_file())
