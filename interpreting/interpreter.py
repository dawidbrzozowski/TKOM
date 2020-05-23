import functools
from argparse import ArgumentParser

from errors.error import RunTimeError
from interpreting.context import Context
from interpreting.utils import check_type_match
from interpreting.values import Number, IntNumber, DoubleNumber, BoolValue
from lexer.lexer import StdInLexer, FileLexer
from lexer.token.token_type import TokenType
from parsing.nodes import *
from parsing.parser import Parser


def run_time_exception_safety(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except RunTimeError as e:
            e.print_error_and_exit()
        return result

    return wrapper_decorator


class Interpreter:

    @run_time_exception_safety
    def visit(self, node, context):
        node_name = type(node).__name__
        visit_method_name = f'visit_{node_name}'
        visit_method = getattr(self, visit_method_name, self.visit_not_found)
        return visit_method(node, context)

    def visit_IntNode(self, node: IntNode, context):
        return IntNumber(node.token.value, node.pos_start, node.pos_end, context)

    def visit_DoubleNode(self, node: DoubleNode, context):
        return DoubleNumber(node.token.value, node.pos_start, node.pos_end, context)

    def visit_StringNode(self, node: StringNode, context):
        print('StringNode visited')

    def visit_StatementsNode(self, node: StatementsNode, context):
        for statement in node.statements:
            print(self.visit(statement, context))

    def visit_UnaryOperationNode(self, node: UnaryOperationNode, context):
        number = self.visit(node.node, context)

        if node.operation.type == TokenType.T_MINUS:
            number = number.multiply(Number(-1))
        elif node.operation.type == TokenType.T_NOT:
            number = number.not_()
        number.set_position(node.pos_start, node.pos_end)
        return number

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, context):
        print('Binary operation node visited')
        left = self.visit(node.left, context)
        right = self.visit(node.right, context)
        operation = node.operation
        result = None
        if operation.type == TokenType.T_PLUS:
            result = left.add(right)
        elif operation.type == TokenType.T_MINUS:
            result = left.subtract(right)
        elif operation.type == TokenType.T_MUL:
            result = left.multiply(right)
        elif operation.type == TokenType.T_DIV:
            result = left.divide(right)
        elif operation.type == TokenType.T_LESS:
            result = left.is_less_than(right)
        elif operation.type == TokenType.T_LESS_OR_EQ:
            result = left.is_less_or_eq(right)
        elif operation.type == TokenType.T_GREATER:
            result = left.is_greater_than(right)
        elif operation.type == TokenType.T_GREATER_OR_EQ:
            result = left.is_greater_or_eq(right)
        elif operation.type == TokenType.T_EQ:
            result = left.is_equal(right)
        elif operation.type == TokenType.T_NOT_EQ:
            result = left.is_not_equal(right)
        elif operation.type == TokenType.T_AND:
            result = left.and_(right)
        elif operation.type == TokenType.T_OR:
            result = left.or_(right)
        result.set_position(node.pos_start, node.pos_end)
        return result

    def visit_VariableAccessNode(self, node: VariableAccessNode, context):
        variable_name = node.name.value
        value = context.symbol_table.get(variable_name)
        if not value:
            raise RunTimeError(node.pos_start, f'{variable_name} not defined.', context)
        value = value.copy()
        value.set_position(node.pos_start, node.pos_end)
        return value

    def visit_VariableAssignmentNode(self, node: VariableAssignmentNode, context):
        variable_name = node.name.value
        value = self.visit(node.value, context)
        check_type_match(node.type, value, context)
        context.symbol_table.set(variable_name, value)
        return value

    def visit_BoolNode(self, node: BoolNode, context):
        return BoolValue(True if node.token.type == TokenType.T_TRUE else False, node.pos_start, node.pos_end, context)

    def visit_not_found(self, node, context):
        raise RunTimeError(node.pos_start, f'Could not find method for node: {type(node).__name__}', context)


def main(args):
    lexer = StdInLexer() if args.source_type == 'stdin' else FileLexer(args.file_path)
    parser = Parser(lexer)
    ast = parser.parse()
    print(ast)
    context = Context('<main>')
    interpreter = Interpreter()
    interpreter.visit(ast, context)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='test_files/testfile1line.txt', required=False)
    parser.add_argument('--source_type', type=str, choices=['stdin', 'file'], default='file')
    args = parser.parse_args()
    main(args)
