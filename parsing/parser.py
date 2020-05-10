from errors.error import InvalidSyntaxError
from lexer.lexer import FileLexer
from lexer.token.token_type import TokenType
from parsing.nodes import IntNode, BinaryOperationNode, UnaryOperationNode, VariableAssignmentNode, VariableAccessNode, \
    IfNode, WhileNode, FunctionDefinitionNode, CallFunctionNode, StringNode, DoubleNode, ListNode, ReturnNode, TypeNode, \
    FunctionArgumentNode

VARIABLE_TYPES = (TokenType.T_STRING, TokenType.T_DOUBLE, TokenType.T_INT)

COMPARISONS = (TokenType.T_EQ, TokenType.T_NOT_EQ, TokenType.T_GREATER, TokenType.T_GREATER_OR_EQ, TokenType.T_LESS,
               TokenType.T_LESS_OR_EQ)


class Parser:
    def __init__(self, lexer):
        self.lexer: FileLexer = lexer
        self.current_token = None
        self.next_token()

    def parse(self):
        result = self.statements(end_tokens=[TokenType.T_EOT])
        return result

    def next_token(self):
        self.current_token = self.lexer.get_next_token()
        return self.current_token

    def perform_method(self, method):
        result = None
        try:
            result = method()
        except InvalidSyntaxError as e:
            e.print_error_and_exit()
        return result

    def statements(self, end_tokens):
        statements = []
        pos_start = self.current_token.pos_start.copy()

        # There must be at least 1 statement
        statement = self.perform_method(self.parse_statement)
        statements.append(statement)

        while self.current_token.type not in end_tokens:
            statement = self.perform_method(self.parse_statement)
            statements.append(statement)
        return ListNode(
            statements,
            pos_start,
            self.current_token.pos_end.copy()
        )

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
            self.check_token_and_next(TokenType.T_SEMICOLON, ';')
            return return_expression

        expression = self.parse_expression()
        self.check_token_and_next(TokenType.T_SEMICOLON, ';')
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
        if self.current_token.type in VARIABLE_TYPES:
            self.next_token()
            if self.current_token.type != TokenType.VT_ID:
                raise InvalidSyntaxError(self.current_token.pos_start.copy(), 'Expected identifier')
            variable_name = self.current_token
            self.next_token()

            if self.current_token.type != TokenType.T_ASSIGN:
                raise InvalidSyntaxError(self.current_token.pos_start.copy(), 'Expected =')

            self.next_token()
            expr = self.parse_expression()
            return VariableAssignmentNode(variable_name, expr)

        return self.parse_binary_operation(self.parse_comparison_expression, (TokenType.T_AND, TokenType.T_OR))

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

        elif token.type == TokenType.VT_INT:
            self.next_token()
            return IntNode(token)

        elif token.type == TokenType.VT_DOUBLE:
            self.next_token()
            return DoubleNode(token)

        elif token.type == TokenType.VT_STRING:
            self.next_token()
            return StringNode(token)

        elif token.type == TokenType.VT_ID:
            self.next_token()
            return VariableAccessNode(token)

        elif token.type == TokenType.T_LPARENT:
            self.next_token()
            expression = self.parse_expression()

            if self.current_token.type == TokenType.T_RPARENT:
                self.next_token()
                return expression
            else:
                raise InvalidSyntaxError(self.current_token.pos_start.copy(), "Expected ')'")

        raise InvalidSyntaxError(token.pos_start.copy(), 'Expected int or double.')

    def parse_function_expression(self):
        self.check_token_and_next(TokenType.T_FUNCTION, 'function')
        if not self.current_token.type == TokenType.VT_ID:
            raise InvalidSyntaxError(self.current_token.pos_start, 'Expected identifier')
        function_name = self.current_token
        self.next_token()
        self.check_token_and_next(TokenType.T_LPARENT, '(')
        arguments = []
        if self.current_token.type == TokenType.VT_ID:
            argument = self.parse_function_argument()
            self.next_token()
            arguments.append(argument)
            while self.current_token.type == TokenType.T_COMMA:
                self.next_token()
                if not self.current_token.type == TokenType.VT_ID:
                    raise InvalidSyntaxError(self.current_token.pos_start, 'Expected identifier')
                argument = self.parse_function_argument()
                arguments.append(argument)
                self.next_token()
        self.check_token_and_next(TokenType.T_RPARENT, ')')

        self.check_token_and_next(TokenType.T_ARROW, '->')

        return_type = self.parse_type(include_void=True)
        self.next_token()

        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expressions = self.statements([TokenType.T_RBRACKET])
        self.check_token_and_next(TokenType.T_RBRACKET, '}')
        return FunctionDefinitionNode(function_name, arguments, expressions, return_type)

    def parse_function_argument(self):
        argument_name = self.current_token
        self.next_token()
        self.check_token_and_next(TokenType.T_COLON, ':')
        argument_type = self.parse_type()
        return FunctionArgumentNode(argument_name, argument_type)

    def parse_type(self, include_void=False):
        variable_types = VARIABLE_TYPES or TokenType.T_VOID if include_void else VARIABLE_TYPES
        if self.current_token.type not in variable_types:
            raise InvalidSyntaxError(self.current_token.pos_start, 'Expected int, double or string')
        return TypeNode(self.current_token)

    def parse_call_function(self):
        function_name = self.parse_factor()
        self.next_token()
        arguments = []
        self.check_token_and_next(TokenType.T_LPARENT, '(')
        if self.current_token.type == TokenType.T_RPARENT:
            self.next_token()
        else:
            arguments.append(self.parse_expression())
            while self.current_token.type == TokenType.T_COMMA:
                self.next_token()
                arguments.append(self.parse_expression())
            self.check_token_and_next(TokenType.T_RPARENT, ')')
        return CallFunctionNode(function_name, arguments)

    def parse_while_expression(self):
        self.check_token_and_next(TokenType.T_WHILE, 'while')
        condition = self.get_condition_with_parenthesis()
        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expressions = self.statements([TokenType.T_RBRACKET])
        self.next_token()
        return WhileNode(condition, expressions)

    def parse_if_expression(self):
        if_cases = []
        else_case = None
        self.check_token_and_next(TokenType.T_IF, 'if')

        condition = self.get_condition_with_parenthesis()
        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expressions = self.statements([TokenType.T_RBRACKET])
        if_cases.append((condition, expressions))
        self.next_token()

        while self.current_token.type == TokenType.T_ELSEIF:
            self.next_token()
            condition = self.get_condition_with_parenthesis()
            self.check_token_and_next(TokenType.T_LBRACKET, '{')
            expressions = self.statements([TokenType.T_RBRACKET])
            if_cases.append((condition, expressions))
            self.next_token()

        if self.current_token.type == TokenType.T_ELSE:
            self.next_token()
            self.check_token_and_next(TokenType.T_LBRACKET, '{')
            else_case = self.statements([TokenType.T_RBRACKET])

        self.next_token()

        return IfNode(if_cases, else_case)

    def get_condition_with_parenthesis(self):
        self.check_token_and_next(TokenType.T_LPARENT, '(')
        condition = self.parse_expression()
        self.check_token_and_next(TokenType.T_RPARENT, ')')
        return condition

    def get_expression_with_brackets(self):
        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expr = self.parse_expression()
        self.check_token_and_next(TokenType.T_RBRACKET, '}')
        return expr

    def check_token_and_next(self, expected: TokenType, as_string):
        if not self.current_token.type == expected:
            raise InvalidSyntaxError(self.current_token.pos_start.copy(), f'Expected {as_string}')
        self.next_token()

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
