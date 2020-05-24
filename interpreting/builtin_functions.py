from interpreting.context import Context
from interpreting.interpreter import Interpreter


class OverInterpreter:
    def __init__(self):
        self.context = Context('<main>')
        self.interpreter = Interpreter()

    def interpret(self, ast):
        self.interpreter.visit(ast, self.context)

    def add_builtin_functions(self):
        pass

    def add_print_function(self):
        function_name = 'print'
        function_context = Context(function_name, self.context, self.context.position)

    def print(self, value):
        print(value)
