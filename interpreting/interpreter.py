from argparse import ArgumentParser

from interpreting.visitator import Visitator
from lexer.lexer import StdInLexer, FileLexer
from parsing.parser import Parser


class Interpreter:
    def __init__(self):
        self.visitator = Visitator()

    def interpret(self, ast):
        if ast:
            return self.visitator.perform_visiting(ast)
        else:
            return 'Provide code and try again.'


class Evaluator:
    def __init__(self):
        self.interpreter = Interpreter()

    def evaluate(self, source_type, file_path=None):
        lexer = StdInLexer() if source_type == 'stdin' else FileLexer(file_path)
        parser = Parser(lexer)
        ast = parser.parse()
        return self.interpreter.interpret(ast)


def main(args):
    evaluator = Evaluator()
    result = evaluator.evaluate(args.source_type, args.file_path)
    if result:
        print(result)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='test_files/presentation_test.txt', required=False)
    parser.add_argument('--source_type', type=str, choices=['stdin', 'file'], default='file')
    args = parser.parse_args()
    main(args)
