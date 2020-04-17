import argparse

from errors.error import LexerError
from lexer.source import FileSource, StdInSource
from lexer.token.tokens import BaseToken, Position, create_token
from lexer.token.token_type import TokenType
from lexer.regex2token import compile_regex2token
from errors.error import print_error_and_exit


class LexerBase:
    def __init__(self, source=None):
        self.source = source
        self.position = Position(row=1, column=0)
        self.regex2token = compile_regex2token()
        self.all_tokens = None
        self.token_iterator = 0

    def get_next_token(self):
        if self.token_iterator < len(self.all_tokens):
            token = self.all_tokens[self.token_iterator]
            self.token_iterator += 1
            return token
        return None

    def next_token_exists(self):
        return True if self.token_iterator < len(self.all_tokens) else False

    def _get_all_tokens(self):
        tokens_from_stdin = []
        while not self.source.is_end_of_text():
            tokens = self._get_tokens_from_next_line()
            tokens_from_stdin.extend(tokens)
        return tokens_from_stdin

    def _get_tokens_from_next_line(self):
        line = self.source.read_line()
        tokens = self._get_tokens_from_line(line)
        self.position.row += 1
        return tokens

    def _get_tokens_from_line(self, line):
        if line:
            tokens = self._lex_line(line)
        else:
            tokens = [BaseToken(TokenType.T_EOT, self.position.copy(), self.position.copy())]
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


class FileLexer(LexerBase):
    def __init__(self, file_path):
        super().__init__(source=FileSource(file_path))
        self.all_tokens = self._get_all_tokens()


class StdInLexer(LexerBase):
    def __init__(self):
        super().__init__(source=StdInSource())
        self.all_tokens = self._get_all_tokens()


def main(args):
    lexer = StdInLexer() if args.lexer_type == 'stdin' else FileLexer(args.file_path)
    while lexer.next_token_exists():
        print(lexer.get_next_token())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='test_files/presentation_test.txt', required=False)
    parser.add_argument('--lexer_type', type=str, choices=['stdin', 'file'], default='file')
    args = parser.parse_args()
    main(args)
