from errors.error import InvalidSyntaxError
from lexer.lexer import FileLexer, StdInLexer
from lexer.token.token_type import TokenType
from lexer.token.token_type_repr import token_type_repr
from parsing.nodes import *

VARIABLE_TYPES = (TokenType.T_STRING, TokenType.T_DOUBLE, TokenType.T_INT, TokenType.T_PHYS, TokenType.T_UNIT)

COMPARISONS = (TokenType.T_EQ, TokenType.T_NOT_EQ, TokenType.T_GREATER, TokenType.T_GREATER_OR_EQ, TokenType.T_LESS,
               TokenType.T_LESS_OR_EQ)

NUMERICAL_VALUES = [TokenType.VT_INT, TokenType.VT_DOUBLE]


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self._next_token()

    def parse(self):
        result = self._parse_statements(end_token=TokenType.T_EOT)
        return result

    def _parse_statements(self, end_token):
        statements = []
        pos_start = self.current_token.pos_start.copy()

        statement = self._perform_method(self._parse_statement)
        statements.append(statement)

        while self.current_token.type != end_token:
            statement = self._perform_method(self._parse_statement)
            statements.append(statement)
        pos_end = self.current_token.pos_end
        self._check_token_and_next(self.current_token.type)
        return StatementsNode(statements, pos_start, pos_end)

    def _parse_statement(self):
        token = self.current_token
        if token.type == TokenType.T_IF:
            if_expression = self._parse_if_expression()
            return if_expression

        elif token.type == TokenType.T_WHILE:
            while_expression = self._parse_while_expression()
            return while_expression

        elif token.type == TokenType.T_FUNCTION:
            function_expression = self._parse_function_definition()
            return function_expression

        elif token.type == TokenType.T_RETURN:
            return_expression = self._parse_return()
            self._check_token_and_next(TokenType.T_SEMICOLON)
            return return_expression

        elif self._is_current_token_type(TokenType.T_BREAK):
            self._check_token_and_next(TokenType.T_SEMICOLON)
            return BreakNode(token.pos_start, self.current_token.pos_start)

        elif self._is_current_token_type(TokenType.T_CONTINUE):
            self._check_token_and_next(TokenType.T_SEMICOLON)
            return ContinueNode(token.pos_start, self.current_token.pos_start)

        expression = self._parse_expression()
        self._check_token_and_next(TokenType.T_SEMICOLON)
        return expression

    def _parse_if_expression(self):
        if_cases = []
        else_case = None
        self._check_token_and_next(TokenType.T_IF)

        condition = self._get_condition_with_parenthesis()
        self._check_token_and_next(TokenType.T_LBRACKET)
        expressions = self._parse_statements(TokenType.T_RBRACKET)
        if_cases.append((condition, expressions))

        while self._is_current_token_type(TokenType.T_ELSEIF):
            condition = self._get_condition_with_parenthesis()
            self._check_token_and_next(TokenType.T_LBRACKET)
            expressions = self._parse_statements(TokenType.T_RBRACKET)
            if_cases.append((condition, expressions))

        if self._is_current_token_type(TokenType.T_ELSE):
            self._check_token_and_next(TokenType.T_LBRACKET)
            else_case = self._parse_statements(TokenType.T_RBRACKET)

        return IfNode(if_cases, else_case)

    def _parse_while_expression(self):
        self._check_token_and_next(TokenType.T_WHILE)
        condition = self._get_condition_with_parenthesis()
        self._check_token_and_next(TokenType.T_LBRACKET)
        expressions = self._parse_statements(TokenType.T_RBRACKET)
        return WhileNode(condition, expressions)

    def _parse_function_definition(self):
        self._check_token_and_next(TokenType.T_FUNCTION)
        function_name = self._get_token_if_type_and_next(TokenType.VT_ID)
        self._check_token_and_next(TokenType.T_LPARENT)
        arguments = []
        if self.current_token.type == TokenType.VT_ID:
            argument = self._parse_function_argument()
            arguments.append(argument)
            while self._is_current_token_type(TokenType.T_COMMA):
                argument = self._parse_function_argument()
                arguments.append(argument)
        self._check_token_and_next(TokenType.T_RPARENT)
        self._check_token_and_next(TokenType.T_ARROW)

        return_type = self._parse_type(include_void=True)

        self._check_token_and_next(TokenType.T_LBRACKET)
        expressions = self._parse_statements(TokenType.T_RBRACKET)
        return FunctionDefinitionNode(function_name, arguments, expressions, return_type)

    def _parse_function_argument(self):
        argument_name = self._get_token_if_type_and_next(TokenType.VT_ID)
        self._check_token_and_next(TokenType.T_COLON)
        argument_type = self._parse_type()
        return FunctionArgumentNode(argument_name, argument_type)

    def _parse_return(self):
        pos_start = self.current_token.pos_start
        pos_end = self.current_token.pos_end
        self._next_token()
        expression = None
        if self.current_token.type != TokenType.T_SEMICOLON:
            expression = self._parse_expression()
            pos_end = expression.pos_end
        return ReturnNode(expression, pos_start, pos_end)

    def _parse_expression(self):
        if self.current_token.type in VARIABLE_TYPES or (
                self.current_token.type == TokenType.VT_ID and self._show_upcoming_token().type == TokenType.T_ASSIGN):
            return self._parse_assignment()

        return self._parse_binary_operation(self._parse_comparison_expression, (TokenType.T_AND, TokenType.T_OR))

    def _parse_assignment(self):
        var_type = None
        if self.current_token.type in VARIABLE_TYPES:
            var_type = self._parse_type()
        variable_name = self._get_token_if_type_and_next(TokenType.VT_ID)
        self._check_token_and_next(TokenType.T_ASSIGN)
        expression = self._parse_expression()
        return VariableAssignmentNode(var_type, variable_name, expression)

    def _parse_comparison_expression(self):
        if self.current_token.type == TokenType.T_NOT:
            operation = self.current_token
            self._next_token()

            comp_node = self._parse_comparison_expression()
            return UnaryOperationNode(operation, comp_node)

        return self._parse_binary_operation(self._parse_arithmetic_expression, COMPARISONS)

    def _parse_arithmetic_expression(self):
        return self._parse_binary_operation(self._parse_term, (TokenType.T_PLUS, TokenType.T_MINUS))

    def _parse_term(self):
        return self._parse_binary_operation(self._parse_factor, (TokenType.T_MUL, TokenType.T_DIV))

    def _parse_binary_operation(self, parse_method, operations):
        left = parse_method()

        while self.current_token.type in operations:
            operation = self.current_token
            self._next_token()
            right = parse_method()
            left = BinaryOperationNode(left, operation, right)
        return left

    def _parse_factor(self):
        token = self.current_token

        if token.type in (TokenType.T_PLUS, TokenType.T_MINUS):
            self._next_token()
            factor = self._parse_factor()
            return UnaryOperationNode(token, factor)

        return self._parse_atom()

    def _parse_atom(self):
        token = self.current_token

        if token.type == TokenType.VT_ID:
            if self._show_upcoming_token().type == TokenType.T_LPARENT:
                return self._parse_call_function()
            self._next_token()
            return VariableAccessNode(token)

        elif token.type == TokenType.T_LPARENT:
            self._next_token()
            expression = self._parse_expression()
            self._check_token_and_next(TokenType.T_RPARENT)
            return expression

        return self._parse_value()

    def _parse_value(self):
        token = self.current_token

        if token.type == TokenType.VT_STRING:
            self._next_token()
            return StringNode(token)

        elif token.type in NUMERICAL_VALUES or token.type == TokenType.VT_ID:
            if self._show_upcoming_token().type == TokenType.T_AMPERSAND:
                return self._parse_phys_value()

        elif token.type == TokenType.T_VERTICAL_BAR:
            return self._parse_unit_value()

        return self._parse_numerical_value()

    def _parse_numerical_value(self):
        token = self.current_token
        if token.type == TokenType.VT_INT:
            self._next_token()
            return IntNode(token)

        elif token.type == TokenType.VT_DOUBLE:
            self._next_token()
            return DoubleNode(token)

        raise InvalidSyntaxError(self._get_last_token_location(), 'Expected expression.')

    def _parse_phys_value(self):
        value = self.current_token
        self._next_token()
        self._check_token_and_next(TokenType.T_AMPERSAND)
        unit = self._parse_unit_value()
        return PhysNode(value, unit)

    def _parse_unit_value(self):
        pos_start = self.current_token.pos_start
        pos_end = pos_start
        self._check_token_and_next(TokenType.T_VERTICAL_BAR)
        nominator = self._get_nominator()
        if len(nominator):
            pos_end = nominator[-1].pos_end
        denominator = []
        if self._is_current_token_type(TokenType.T_DIV):
            denominator = self._get_denominator()
        if len(denominator):
            pos_end = denominator[-1].pos_end
        self._check_token_and_next(TokenType.T_VERTICAL_BAR)
        return UnitNode(nominator, denominator, pos_start, pos_end)

    def _get_nominator(self):
        nominator = []
        if self.current_token.type == TokenType.VT_ID:
            nominator.append(self.current_token)
            self._next_token()
            while self._is_current_token_type(TokenType.T_MUL):
                identifier = self._get_token_if_type_and_next(TokenType.VT_ID)
                nominator.append(identifier)
        else:
            if not isinstance(self.current_token, ValueToken) and \
                    self.current_token.type == TokenType.VT_INT and self.current_token.value == 1:
                raise InvalidSyntaxError(self._get_last_token_location(), 'Expected identifier or 1')
            self._next_token()
        return nominator

    def _get_denominator(self):
        denominator = []
        identifier = self._get_token_if_type_and_next(TokenType.VT_ID)
        denominator.append(identifier)
        while self._is_current_token_type(TokenType.T_MUL):
            identifier = self._get_token_if_type_and_next(TokenType.VT_ID)
            denominator.append(identifier)
        return denominator

    def _parse_call_function(self):
        function_name = self._get_token_if_type_and_next(TokenType.VT_ID)
        arguments = []
        self._check_token_and_next(TokenType.T_LPARENT)

        if not self._is_current_token_type(TokenType.T_RPARENT):
            arguments.append(self._parse_expression())
            while self._is_current_token_type(TokenType.T_COMMA):
                arguments.append(self._parse_expression())
            self._check_token_and_next(TokenType.T_RPARENT)
        return CallFunctionNode(function_name, arguments)

    def _parse_type(self, include_void=False):
        variable_types = VARIABLE_TYPES or TokenType.T_VOID if include_void else VARIABLE_TYPES
        if self.current_token.type not in variable_types:
            raise InvalidSyntaxError(self._get_last_token_location(), 'Expected type.')
        token = self.current_token
        self._next_token()
        return TypeNode(token)

    def _is_current_token_type(self, token_type):
        result = False
        if self.current_token.type == token_type:
            result = True
            self._next_token()
        return result

    def _get_condition_with_parenthesis(self):
        self._check_token_and_next(TokenType.T_LPARENT)
        condition = self._parse_expression()
        self._check_token_and_next(TokenType.T_RPARENT)
        return condition

    def _check_token_and_next(self, expected: TokenType):
        if not self.current_token.type == expected:
            raise InvalidSyntaxError(self._get_last_token_location(), f'Expected {token_type_repr.get(expected)}')
        self._next_token()

    def _get_token_if_type_and_next(self, expected: TokenType):
        token = self.current_token
        self._check_token_and_next(expected)
        return token

    def _next_token(self):
        self.current_token = self.lexer.get_next_token()
        return self.current_token

    def _show_upcoming_token(self):
        return self.lexer.get_next_token(move_index=False)

    def _get_last_token_location(self):
        return self.lexer.show_prev_token_location()

    def _perform_method(self, method):
        result = None
        try:
            result = method()
        except InvalidSyntaxError as e:
            e.print_error_and_exit()
        return result


if __name__ == '__main__':
    file_lexer = FileLexer('test_files/presentation_test.txt')
    parser = Parser(file_lexer)
    ast = parser.parse()
    print(ast)
