import functools
from argparse import ArgumentParser

from errors.error import RunTimeError
from interpreting.context import Context
from interpreting.utils import check_type_match
from interpreting.values import IntValue, DoubleValue, BoolValue, StringValue, Function, Value, FunctionArgument
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
        return IntValue(node.token.value, node.pos_start, node.pos_end, context)

    def visit_DoubleNode(self, node: DoubleNode, context):
        return DoubleValue(node.token.value, node.pos_start, node.pos_end, context)

    def visit_StringNode(self, node: StringNode, context):
        return StringValue(node.token.value, node.pos_start, node.pos_end, context)

    def visit_StatementsNode(self, node: StatementsNode, context):
        for statement in node.statements:
            result = self.visit(statement, context)
        return result

    def visit_UnaryOperationNode(self, node: UnaryOperationNode, context):
        value = self.visit(node.node, context)

        if node.operation.type == TokenType.T_MINUS:
            value = value.multiply(IntValue(-1))
        elif node.operation.type == TokenType.T_NOT:
            value = value.not_()
        value.set_position(node.pos_start, node.pos_end)
        return value

    def visit_BinaryOperationNode(self, node: BinaryOperationNode, context):
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
        variable_name = node.name
        value = self.visit(node.value, context)
        self.verify_assignment(variable_name, value, node.type, context)
        context.symbol_table.set(variable_name.value, value)
        return value

    def verify_assignment(self, variable_name, value, defined_type, context):
        check_type_match(defined_type, value, context)
        if defined_type is None:
            current_value = context.symbol_table.get(variable_name.value)
            if not current_value:
                raise RunTimeError(variable_name.pos_start,
                                   'This variable has not been defined yet. Put a type.', context)

            if current_value.type_ != value.type_:
                raise RunTimeError(value.pos_start,
                                   f'Tried to put a value of type {value.type_}'
                                   f' to a variable of type {current_value.type_}', context)

    def visit_BoolNode(self, node: BoolNode, context):
        return BoolValue(True if node.token.type == TokenType.T_TRUE else False, node.pos_start, node.pos_end, context)

    def visit_IfNode(self, node: IfNode, context):
        for condition, statement in node.cases:
            condition_result = self.visit(condition, context)
            if condition_result.value:
                statement_value = self.visit(statement, context)
                return statement_value
        if node.else_case:
            else_statement_value = self.visit(node.else_case, context)
            return else_statement_value

    def visit_WhileNode(self, node: WhileNode, context):
        condition = self.visit(node.condition_node, context)
        while condition.value:
            self.visit(node.body_node, context)
            condition = self.visit(node.condition_node, context)

    def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode, context):
        function_name = node.function_name.value
        function_context = Context(function_name, context, context.position)
        arguments = [self.visit(argument, context) for argument in node.arguments]
        return_type = node.return_type_node
        body = node.body
        function = Function(function_name, arguments, body, return_type, function_context, node.pos_start, node.pos_end)
        context.symbol_table.set(function_name, function)

    def visit_CallFunctionNode(self, node: CallFunctionNode, context):
        function_name = node.function_name.value
        function = context.symbol_table.get(function_name)
        if function is None:
            raise RunTimeError(node.pos_start, f'Function with name: {function_name} is not defined.', context)
        arguments = [self.visit(argument, context) for argument in node.arguments]
        if len(arguments) != len(function.argument_definitions):
            raise RunTimeError(node.pos_start,
                               f'Wrong amount of arguments. Expected: {len(function.argument_definitions)}.'
                               f' Got: {len(arguments)}', context)
        for argument, defined_argument in zip(arguments, function.argument_definitions):
            if argument.type_ != defined_argument.type:
                raise RunTimeError(node.pos_start, f'Wrong type of argument. Expected {defined_argument.type} '
                                                   f'got: {argument.type_}', context)
            else:
                function.context.symbol_table.set(defined_argument.name, argument)

        return self.execute_function(function)

    def execute_function(self, function):
        result = self.visit(function.body, function.context)
        return result

    def visit_FunctionArgumentNode(self, node: FunctionArgumentNode, context):
        variable_name = node.name.value
        argument = FunctionArgument(variable_name, node.type.type)
        return argument

    def visit_not_found(self, node, context):
        raise RunTimeError(node.pos_start, f'Could not find method for node: {type(node).__name__}', context)


def main(args):
    lexer = StdInLexer() if args.source_type == 'stdin' else FileLexer(args.file_path)
    parser = Parser(lexer)
    ast = parser.parse()
    print(ast)
    context = Context('<main>')
    interpreter = Interpreter()
    print(interpreter.visit(ast, context))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='test_files/testfile1line.txt', required=False)
    parser.add_argument('--source_type', type=str, choices=['stdin', 'file'], default='file')
    args = parser.parse_args()
    main(args)
