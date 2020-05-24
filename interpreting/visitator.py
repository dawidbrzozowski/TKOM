import functools

from errors.error import RunTimeError
from interpreting.context import ContextManager
from interpreting.values import IntValue, DoubleValue, BoolValue, StringValue, FunctionDefinition, FunctionArgument, \
    ReturnValue
from lexer.token.token_type import TokenType
from lexer.token.token_type_repr import token_type_repr
from parsing.nodes import *


def run_time_exception_safety(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except RunTimeError as e:
            e.print_error_and_exit()
        return result

    return wrapper


class Visitator:
    def __init__(self):
        self.context_manager = ContextManager()

    @run_time_exception_safety
    def visit(self, node):
        node_name = type(node).__name__
        visit_method_name = f'visit_{node_name}'
        visit_method = getattr(self, visit_method_name, self.visit_not_found)
        return visit_method(node)

    def visit_IntNode(self, node: IntNode):
        return IntValue(node.token.value, node.pos_start, node.pos_end, self.context_manager.current_context)

    def visit_DoubleNode(self, node: DoubleNode):
        return DoubleValue(node.token.value, node.pos_start, node.pos_end, self.context_manager.current_context)

    def visit_StringNode(self, node: StringNode):
        return StringValue(node.token.value, node.pos_start, node.pos_end, self.context_manager.current_context)

    def visit_StatementsNode(self, node: StatementsNode):
        result = None
        for statement in node.statements:
            result = self.visit(statement)
            if result == 'break':
                break
            elif result == 'continue':
                break
            elif isinstance(result, ReturnValue):
                return result.value
        if isinstance(result, (IntValue, StringValue, DoubleValue, BoolValue)):
            return result

    def visit_UnaryOperationNode(self, node: UnaryOperationNode):
        value = self.visit(node.node)

        if node.operation.type == TokenType.T_MINUS:
            value = value.multiply(IntValue(-1))
        elif node.operation.type == TokenType.T_NOT:
            value = value.not_()
        value.set_position(node.pos_start, node.pos_end)
        return value

    def visit_BinaryOperationNode(self, node: BinaryOperationNode):
        left = self.visit(node.left)
        right = self.visit(node.right)
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

    def visit_VariableAccessNode(self, node: VariableAccessNode):
        variable_name = node.name.value
        value = self.context_manager.get_variable(variable_name)
        value = value.copy()
        value.set_position(node.pos_start, node.pos_end)
        return value

    def visit_VariableAssignmentNode(self, node: VariableAssignmentNode):
        variable_name = node.name
        value = self.visit(node.value)
        self.context_manager.add_variable(variable_name, value, node.type)

    def visit_BoolNode(self, node: BoolNode):
        return BoolValue(True if node.token.type == TokenType.T_TRUE else False, node.pos_start, node.pos_end,
                         self.context_manager.current_context)

    def visit_IfNode(self, node: IfNode):
        for condition, statement in node.cases:
            condition_result = self.visit(condition)
            if condition_result.value:
                statement_value = self.visit(statement)
                return statement_value
        if node.else_case:
            else_statement_value = self.visit(node.else_case)
            return else_statement_value

    def visit_WhileNode(self, node: WhileNode):
        condition = self.visit(node.condition_node)
        while condition.value:
            body_result = self.visit(node.body_node)
            if body_result == 'break':
                break
            condition = self.visit(node.condition_node)

    def visit_FunctionDefinitionNode(self, node: FunctionDefinitionNode):
        function_name = node.function_name.value
        arguments = [self.visit(argument) for argument in node.arguments]
        return_type = node.return_type_node
        body = node.body
        function = FunctionDefinition(function_name, arguments, body, return_type, node.pos_start, node.pos_end)
        self.context_manager.add_function(function_name, function)

    def visit_CallFunctionNode(self, node: CallFunctionNode):
        function_name = node.function_name.value
        function = self.context_manager.get_function(function_name)
        arguments = [self.visit(argument) for argument in node.arguments]
        if len(arguments) != len(function.argument_definitions):
            raise RunTimeError(node.pos_start,
                               f'Wrong amount of arguments. Expected: {len(function.argument_definitions)}.'
                               f' Got: {len(arguments)}', self.context_manager.current_context)
        self.context_manager.switch_context_to(function_name)
        for argument, defined_argument in zip(arguments, function.argument_definitions):
            if argument.type_ != defined_argument.type:
                raise RunTimeError(node.pos_start, f'Wrong type of argument. Expected {defined_argument.type} '
                                                   f'got: {argument.type_}', self.context_manager.current_context)
            else:
                self.context_manager.current_context.add_variable(defined_argument.name, argument)

        self.context_manager.current_context.position = node.pos_start.copy()
        function_result = self.execute_function(function)
        if token_type_repr.get(function.return_type) == 'void' and function_result.type_ is not None:
            raise RunTimeError(function.return_type.pos_start,
                               f'Expected return type: {token_type_repr.get(function.return_type.type.type)}'
                               f' got {function_result.type_}', function.context)
        elif function_result.type_ != token_type_repr.get(function.return_type.type.type):
            raise RunTimeError(function.return_type.pos_start,
                               f'Expected return type: {token_type_repr.get(function.return_type.type.type)}'
                               f' got {function_result.type_}', function.context)

        self.context_manager.switch_to_parent_context()
        return function_result

    def execute_function(self, function):
        result = self.visit(function.body)
        return result

    def visit_FunctionArgumentNode(self, node: FunctionArgumentNode):
        variable_name = node.name.value
        argument = FunctionArgument(variable_name, node.type.type)
        return argument

    def visit_BreakNode(self, node: BreakNode):
        return str(node)

    def visit_ContinueNode(self, node: ContinueNode):
        return str(node)

    def visit_ReturnNode(self, return_node: ReturnNode):
        value = self.visit(return_node.node) if return_node.node else None
        return ReturnValue(value)

    def visit_not_found(self, node, context):
        raise RunTimeError(node.pos_start, f'Could not find method for node: {type(node).__name__}', context)
