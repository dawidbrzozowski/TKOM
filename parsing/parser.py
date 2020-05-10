from errors.error import InvalidSyntaxError
from lexer.lexer import FileLexer
from lexer.token.token_type import TokenType
from lexer.token.token_type_repr import token_type_repr
from parsing.nodes import *

VARIABLE_TYPES = (TokenType.T_STRING, TokenType.T_DOUBLE, TokenType.T_INT, TokenType.T_PHYS, TokenType.T_UNIT)

COMPARISONS = (TokenType.T_EQ, TokenType.T_NOT_EQ, TokenType.T_GREATER, TokenType.T_GREATER_OR_EQ, TokenType.T_LESS,
               TokenType.T_LESS_OR_EQ)

NUMERICAL_VALUES = [TokenType.VT_INT, TokenType.VT_DOUBLE]


class Parser:
    def __init__(self, lexer):
        self.lexer: FileLexer = lexer
        self.current_token = None
        self.next_token()

    def parse(self):
        result = self.parse_statements(end_token=TokenType.T_EOT)
        return result

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
        return self.current_token

    def show_upcoming_token(self):
        return self.lexer.get_next_token(move_index=False)

    def perform_method(self, method):
        result = None
        try:
            result = method()
        except InvalidSyntaxError as e:
            e.print_error_and_exit()
        return result

    def parse_statements(self, end_token):
        statements = []
        pos_start = self.current_token.pos_start.copy()

        statement = self.perform_method(self.parse_statement)
        statements.append(statement)

        while self.current_token.type != end_token:
            statement = self.perform_method(self.parse_statement)
            statements.append(statement)
        pos_end = self.current_token.pos_end
        self.check_token_and_next(self.current_token.type)
        return StatementsNode(statements, pos_start, pos_end)

    def parse_statement(self):
        if self.current_token.type == TokenType.T_IF:
            if_expression = self.parse_if_expression()
            return if_expression

        elif self.current_token.type == TokenType.T_WHILE:
            while_expression = self.parse_while_expression()
            return while_expression

        elif self.current_token.type == TokenType.T_FUNCTION:
            function_expression = self.parse_function_expression()
            return function_expression

        elif self.current_token.type == TokenType.T_RETURN:
            return_expression = self.parse_return()
            self.check_token_and_next(TokenType.T_SEMICOLON)
            return return_expression

        expression = self.parse_expression()
        self.check_token_and_next(TokenType.T_SEMICOLON)
        return expression

    def parse_return(self):
        pos_start = self.current_token.pos_start
        pos_end = self.current_token.pos_end
        self.next_token()
        expression = None
        if self.current_token.type != TokenType.T_SEMICOLON:
            expression = self.parse_expression()
            pos_end = expression.pos_end
        return ReturnNode(expression, pos_start, pos_end)

    def parse_expression(self):
        if self.current_token.type in VARIABLE_TYPES or (
                self.current_token.type == TokenType.VT_ID and self.show_upcoming_token().type == TokenType.T_ASSIGN):
            return self.parse_assignment()

        return self.parse_binary_operation(self.parse_comparison_expression, (TokenType.T_AND, TokenType.T_OR))

    def parse_assignment(self):
        var_type = None
        if self.current_token.type in VARIABLE_TYPES:
            var_type = self.parse_type()
        variable_name = self.get_token_if_type_and_next(TokenType.VT_ID)
        self.check_token_and_next(TokenType.T_ASSIGN)
        expression = self.parse_expression()
        return VariableAssignmentNode(var_type, variable_name, expression)

    def parse_comparison_expression(self):
        if self.current_token.type == TokenType.T_NOT:
            operation = self.current_token
            self.next_token()

            comp_node = self.parse_comparison_expression()
            return UnaryOperationNode(operation, comp_node)

        return self.parse_binary_operation(self.parse_arithmetic_expression, COMPARISONS)

    def parse_arithmetic_expression(self):
        return self.parse_binary_operation(self.parse_term, (TokenType.T_PLUS, TokenType.T_MINUS))

    def parse_term(self):
        return self.parse_binary_operation(self.parse_factor, (TokenType.T_MUL, TokenType.T_DIV))

    def parse_factor(self):
        token = self.current_token

        if token.type in (TokenType.T_PLUS, TokenType.T_MINUS):
            self.next_token()
            factor = self.parse_factor()
            return UnaryOperationNode(token, factor)

        return self.parse_atom()

    def parse_atom(self):
        token = self.current_token

        if token.type == TokenType.VT_ID:
            if self.show_upcoming_token().type == TokenType.T_LPARENT:
                return self.parse_call_function()
            self.next_token()
            return VariableAccessNode(token)

        elif token.type == TokenType.T_LPARENT:
            self.next_token()
            expression = self.parse_expression()
            self.check_token_and_next(TokenType.T_RPARENT)
            return expression

        return self.parse_value()

    def parse_value(self):
        token = self.current_token

        if token.type == TokenType.VT_STRING:
            self.next_token()
            return StringNode(token)

        elif token.type in NUMERICAL_VALUES or token.type == TokenType.VT_ID:
            if self.show_upcoming_token().type == TokenType.T_AMPERSAND:
                return self.parse_phys_value()

        elif token.type == TokenType.T_VERTICAL_BAR:
            return self.parse_unit_value()

        return self.parse_numerical_value()

    def parse_unit_value(self):
        pos_start = self.current_token.pos_start
        pos_end = pos_start
        self.check_token_and_next(TokenType.T_VERTICAL_BAR)
        nominator = self.get_nominator()
        if len(nominator):
            pos_end = nominator[-1].pos_end
        denominator = []
        if self.is_current_token_type(TokenType.T_DIV):
            denominator = self.get_denominator()
        if len(denominator):
            pos_end = denominator[-1].pos_end
        self.check_token_and_next(TokenType.T_VERTICAL_BAR)
        return UnitNode(nominator, denominator, pos_start, pos_end)

    def get_nominator(self):
        nominator = []
        if self.current_token.type == TokenType.VT_ID:
            nominator.append(self.current_token)
            self.next_token()
            while self.is_current_token_type(TokenType.T_MUL):
                identifier = self.get_token_if_type_and_next(TokenType.VT_ID)
                nominator.append(identifier)
        else:
            if not isinstance(self.current_token, ValueToken) and \
                    self.current_token.type == TokenType.VT_INT and self.current_token.value == 1:
                raise InvalidSyntaxError(self.current_token.pos_start, 'Expected identifier or 1')
            self.next_token()
        return nominator

    def get_denominator(self):
        denominator = []
        identifier = self.get_token_if_type_and_next(TokenType.VT_ID)
        denominator.append(identifier)
        while self.is_current_token_type(TokenType.T_MUL):
            identifier = self.get_token_if_type_and_next(TokenType.VT_ID)
            denominator.append(identifier)
        return denominator

    def parse_phys_value(self):
        value = self.current_token
        self.next_token()
        self.check_token_and_next(TokenType.T_AMPERSAND)
        unit = self.parse_unit_value()
        return PhysNode(value, unit)

    def parse_numerical_value(self):
        token = self.current_token
        if token.type == TokenType.VT_INT:
            self.next_token()
            return IntNode(token)

        elif token.type == TokenType.VT_DOUBLE:
            self.next_token()
            return DoubleNode(token)

        raise InvalidSyntaxError(token.pos_start.copy(), 'Expected instruction.')

    def parse_function_expression(self):
        self.check_token_and_next(TokenType.T_FUNCTION)
        function_name = self.get_token_if_type_and_next(TokenType.VT_ID)
        self.check_token_and_next(TokenType.T_LPARENT)
        arguments = []
        if self.current_token.type == TokenType.VT_ID:
            argument = self.parse_function_argument()
            arguments.append(argument)
            while self.is_current_token_type(TokenType.T_COMMA):
                argument = self.parse_function_argument()
                arguments.append(argument)
        self.check_token_and_next(TokenType.T_RPARENT)
        self.check_token_and_next(TokenType.T_ARROW)

        return_type = self.parse_type(include_void=True)

        self.check_token_and_next(TokenType.T_LBRACKET)
        expressions = self.parse_statements(TokenType.T_RBRACKET)
        return FunctionDefinitionNode(function_name, arguments, expressions, return_type)

    def parse_function_argument(self):
        argument_name = self.get_token_if_type_and_next(TokenType.VT_ID)
        self.check_token_and_next(TokenType.T_COLON)
        argument_type = self.parse_type()
        return FunctionArgumentNode(argument_name, argument_type)

    def parse_type(self, include_void=False):
        variable_types = VARIABLE_TYPES or TokenType.T_VOID if include_void else VARIABLE_TYPES
        if self.current_token.type not in variable_types:
            raise InvalidSyntaxError(self.current_token.pos_start, 'Expected int, double or string')
        token = self.current_token
        self.next_token()
        return TypeNode(token)

    def is_current_token_type(self, token_type):
        result = False
        if self.current_token.type == token_type:
            result = True
            self.next_token()
        return result

    def parse_call_function(self):
        function_name = self.get_token_if_type_and_next(TokenType.VT_ID)
        arguments = []
        self.check_token_and_next(TokenType.T_LPARENT)

        if not self.is_current_token_type(TokenType.T_RPARENT):
            arguments.append(self.parse_expression())
            while self.is_current_token_type(TokenType.T_COMMA):
                arguments.append(self.parse_expression())
            self.check_token_and_next(TokenType.T_RPARENT)
        return CallFunctionNode(function_name, arguments)

    def parse_while_expression(self):
        self.check_token_and_next(TokenType.T_WHILE)
        condition = self.get_condition_with_parenthesis()
        self.check_token_and_next(TokenType.T_LBRACKET)
        expressions = self.parse_statements(TokenType.T_RBRACKET)
        return WhileNode(condition, expressions)

    def parse_if_expression(self):
        if_cases = []
        else_case = None
        self.check_token_and_next(TokenType.T_IF)

        condition = self.get_condition_with_parenthesis()
        self.check_token_and_next(TokenType.T_LBRACKET)
        expressions = self.parse_statements(TokenType.T_RBRACKET)
        if_cases.append((condition, expressions))

        while self.is_current_token_type(TokenType.T_ELSEIF):
            condition = self.get_condition_with_parenthesis()
            self.check_token_and_next(TokenType.T_LBRACKET)
            expressions = self.parse_statements(TokenType.T_RBRACKET)
            if_cases.append((condition, expressions))

        if self.is_current_token_type(TokenType.T_ELSE):
            self.check_token_and_next(TokenType.T_LBRACKET)
            else_case = self.parse_statements(TokenType.T_RBRACKET)

        return IfNode(if_cases, else_case)

    def get_condition_with_parenthesis(self):
        self.check_token_and_next(TokenType.T_LPARENT)
        condition = self.parse_expression()
        self.check_token_and_next(TokenType.T_RPARENT)
        return condition

    def check_token_and_next(self, expected: TokenType):
        if not self.current_token.type == expected:
            raise InvalidSyntaxError(self.current_token.pos_start.copy(), f'Expected {token_type_repr.get(expected)}')
        self.next_token()

    def get_token_if_type_and_next(self, expected: TokenType):
        token = self.current_token
        self.check_token_and_next(expected)
        return token

    def parse_binary_operation(self, parse_method, operations):
        left = parse_method()

        while self.current_token.type in operations:
            operation = self.current_token
            self.next_token()
            right = parse_method()
            left = BinaryOperationNode(left, operation, right)
        return left


if __name__ == '__main__':
    file_lexer = FileLexer('test_files/testfile1line.txt')
    parser = Parser(file_lexer)
    ast = parser.parse()
    print(ast)
