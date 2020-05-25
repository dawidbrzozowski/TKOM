from lexer.lexer import LexerBase
from lexer.source import Source

SOURCE_END = 'DONE'


class TestSource(Source):
    def __init__(self):
        self.lines = []
        self.eot = False

    def put_text(self, text):
        self.lines.append(text)

    def read_line(self):
        line = self.lines.pop(0) if len(self.lines) else SOURCE_END
        if line == SOURCE_END:
            self.eot = True
        return line

    def is_end_of_text(self):
        return self.eot


class TestLexer(LexerBase):
    def __init__(self, source):
        super().__init__(source)

    def lex(self):
        self.all_tokens = self._get_all_tokens()
