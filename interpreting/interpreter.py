from argparse import ArgumentParser

from interpreting.visitator import Visitator
from lexer.lexer import StdInLexer, FileLexer
from parsing.parser import Parser


class Interpreter:
    def __init__(self):
        self.visitator = Visitator()

    def interpret(self, ast):
        return self.visitator.visit(ast)


def main(args):
    lexer = StdInLexer() if args.source_type == 'stdin' else FileLexer(args.file_path)
    parser = Parser(lexer)
    ast = parser.parse()
    interpreter = Interpreter()

    res = interpreter.interpret(ast)
    if res:
        print(res)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='test_files/testfile1line.txt', required=False)
    parser.add_argument('--source_type', type=str, choices=['stdin', 'file'], default='file')
    args = parser.parse_args()
    main(args)
