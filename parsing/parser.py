from errors.error import InvalidSyntaxError
from lexer.lexer import FileLexer
from lexer.token.token_type import TokenType
from lexer.token.tokens import BaseToken
from parsing.nodes import NumberNode, BinaryOperationNode, UnaryOperationNode, VariableAssignmentNode, VarAccessNode

VARIABLES = (BaseToken(TokenType.T_STRING), BaseToken(TokenType.T_DOUBLE), BaseToken(TokenType.T_INT))

COMPARISONS = (TokenType.T_EQ, TokenType.T_NOT_EQ, TokenType.T_GREATER, TokenType.T_GREATER_OR_EQ, TokenType.T_LESS,
               TokenType.T_LESS_OR_EQ)


class Parser:
    def __init__(self, lexer):
        self.lexer: FileLexer = lexer
        self.current_token = None
        self.next_token()

    def parse(self):
        result = self.perform_method(self.parse_expression)
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

        elif token.type in (TokenType.VT_INT, TokenType.VT_DOUBLE):
            self.next_token()
            return NumberNode(token)

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
