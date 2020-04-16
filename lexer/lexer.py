import re

from lexer.source import Source, FileSource
from lexer.token import Token
from lexer.token_type import TokenType
from lexer.token_type_regexp import token_exprs


class LexError(Exception):
    def __init__(self, char, line_num):
        self.char = char
        self.line_num = line_num

    def __repr__(self):
        return 'Illegal character: %s, at line %d\n' % (self.char, self.line_num)


class Lexer:
    def __init__(self, source_: Source = None):
        self.source = source_
        self.position = 0
        self.curr_line = 0
        self.token_regexps = token_exprs

    def get_tokens_from_next_line(self):
        line = self.source.read_line()
        return self.get_tokens_from_line(line)

    def get_tokens_from_line(self, line):
        if line:
            tokens = self.lex_line(line)
        else:
            tokens = [Token(TokenType.T_EOT, row=self.curr_line)]
        return tokens

    def lex_line(self, line):
        pos = 0
        tokens = []
        while pos < len(line):
            match = None
            for t_regexp in self.token_regexps:
                pattern, tag = t_regexp
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        if tag.name.startswith("V"):
                            token = Token(tag, text, self.curr_line)
                        else:
                            token = Token(tag, row=self.curr_line)
                        tokens.append(token)

                    break
            if not match:
                raise LexError(line[pos], self.curr_line)
            else:
                pos = match.end(0)
        return tokens


if __name__ == '__main__':
    source = FileSource('test_files/testfile1.txt')
    lexer = Lexer(source)
    print(lexer.get_tokens_from_next_line())
    print(lexer.get_tokens_from_next_line())
