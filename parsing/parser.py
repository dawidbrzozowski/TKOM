from errors.error import InvalidSyntaxError
from lexer.lexer import FileLexer
from lexer.token.token_type import TokenType
from lexer.token.tokens import BaseToken
from parsing.nodes import IntNode, BinaryOperationNode, UnaryOperationNode, VariableAssignmentNode, VarAccessNode, \
    IfNode, WhileNode, FunctionDefinitionNode, CallFunctionNode, StringNode, DoubleNode, ListNode

VARIABLES = (BaseToken(TokenType.T_STRING), BaseToken(TokenType.T_DOUBLE), BaseToken(TokenType.T_INT))

COMPARISONS = (TokenType.T_EQ, TokenType.T_NOT_EQ, TokenType.T_GREATER, TokenType.T_GREATER_OR_EQ, TokenType.T_LESS,
               TokenType.T_LESS_OR_EQ)


class Parser:
    def __init__(self, lexer):
        self.lexer: FileLexer = lexer
        self.current_token = None
        self.next_token()

    def parse(self):
        result = self.statements([TokenType.T_EOT])
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

        # skip new lines at the start
        while self.current_token.type == TokenType.T_SEMICOLON:
            self.next_token()

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
            if_expression = self.perform_method(self.parse_if_expression)
            return if_expression

        elif self.current_token.type == TokenType.T_WHILE:
            while_expression = self.perform_method(self.parse_while_expression)
            return while_expression

        elif self.current_token.type == TokenType.T_FUNCTION:
            function_expression = self.perform_method(self.parse_function_expression)
            return function_expression
        expression = self.parse_expression()
        self.check_token_and_next(TokenType.T_SEMICOLON, ';')
        return expression

    def parse_expression(self):
        if self.current_token in VARIABLES:
            self.next_token()
            if self.current_token.type != TokenType.VT_ID:
                raise InvalidSyntaxError(self.current_token.pos_start.copy(), 'Expected identifier')
            variable_name = self.current_token
            self.next_token()

            if self.current_token.type != TokenType.T_ASSIGN:
                raise InvalidSyntaxError(self.current_token.pos_start.copy(), 'Expected =')

            self.next_token()
            expr = self.perform_method(self.parse_expression)
            return VariableAssignmentNode(variable_name, expr)

        return self.parse_binary_operation(self.parse_comparison_expression, (TokenType.T_AND, TokenType.T_OR))

    def parse_comparison_expression(self):
        if self.current_token.type == TokenType.T_NOT:
            operation = self.current_token
            self.next_token()

            comp_node = self.perform_method(self.parse_comparison_expression)
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
            factor = self.perform_method(self.parse_factor)
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
            return VarAccessNode(token)

        elif token.type == TokenType.T_LPARENT:
            self.next_token()
            expression = self.perform_method(self.parse_expression)

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
            arguments.append(self.current_token)
            self.next_token()

            while self.current_token.type == TokenType.T_COMMA:
                self.next_token()
                if not self.current_token.type == TokenType.VT_ID:
                    raise InvalidSyntaxError(self.current_token.pos_start, 'Expected identifier')
                arguments.append(self.current_token)
                self.next_token()
        self.check_token_and_next(TokenType.T_RPARENT, ')')

        self.check_token_and_next(TokenType.T_ARROW, '->')
        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expressions = self.statements([TokenType.T_RBRACKET])
        self.check_token_and_next(TokenType.T_RBRACKET, '}')
        return FunctionDefinitionNode(function_name, arguments, expressions)

    def parse_call_function(self):
        function_name = self.perform_method(self.parse_factor)
        self.next_token()
        arguments = []
        self.check_token_and_next(TokenType.T_LPARENT, '(')
        if self.current_token.type == TokenType.T_RPARENT:
            self.next_token()
        else:
            arguments.append(self.perform_method(self.parse_expression))
            while self.current_token.type == TokenType.T_COMMA:
                self.next_token()
                arguments.append(self.perform_method(self.parse_expression))
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

        while self.current_token.type == TokenType.T_ELSEIF:
            self.next_token()
            condition = self.get_condition_with_parenthesis()
            self.check_token_and_next(TokenType.T_LBRACKET, '{')
            expressions = self.statements([TokenType.T_RBRACKET])
            if_cases.append((condition, expressions))

        if self.current_token.type == TokenType.T_ELSE:
            self.next_token()
            self.check_token_and_next(TokenType.T_LBRACKET, '{')
            else_case = self.statements([TokenType.T_RBRACKET])
            if_cases.append((condition, else_case))

        self.next_token()

        return IfNode(if_cases, else_case)

    def get_condition_with_parenthesis(self):
        self.check_token_and_next(TokenType.T_LPARENT, '(')
        condition = self.perform_method(self.parse_expression)
        self.check_token_and_next(TokenType.T_RPARENT, ')')
        return condition

    def get_expression_with_brackets(self):
        self.check_token_and_next(TokenType.T_LBRACKET, '{')
        expr = self.perform_method(self.parse_expression)
        self.check_token_and_next(TokenType.T_RBRACKET, '}')
        return expr

    def check_token_and_next(self, expected: TokenType, as_string):
        if not self.current_token.type == expected:
            raise InvalidSyntaxError(self.current_token.pos_start.copy(), f'Expected {as_string}')
        self.next_token()

    def parse_binary_operation(self, parse_method, operations):
        left = self.perform_method(parse_method)

        while self.current_token.type in operations:
            operation = self.current_token
            self.next_token()
            right = self.perform_method(parse_method)
            left = BinaryOperationNode(left, operation, right)
        return left


if __name__ == '__main__':
    file_lexer = FileLexer('test_files/testfile1line.txt')
    parser = Parser(file_lexer)
    ast = parser.parse()
    print(ast)
