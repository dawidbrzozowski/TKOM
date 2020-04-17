from lexer.lexer import Lexer
import unittest

from token.token import Token
from token.token_type import TokenType


class LexerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.lexer = Lexer()

    def test_lex_data_types(self):
        line = "int double char bool string "
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_INT),
                    Token(TokenType.T_DOUBLE),
                    Token(TokenType.T_CHAR),
                    Token(TokenType.T_BOOL),
                    Token(TokenType.T_STRING)]
        self.assertEqual(expected, predicted)

    def test_lex_punctuation_types(self):
        line = ", . : ; { } ( )"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_COMMA),
                    Token(TokenType.T_DOT),
                    Token(TokenType.T_COLON),
                    Token(TokenType.T_SEMICOLON),
                    Token(TokenType.T_LBRACKET),
                    Token(TokenType.T_RBRACKET),
                    Token(TokenType.T_LPARENT),
                    Token(TokenType.T_RPARENT)]
        self.assertEqual(expected, predicted)

    def test_lex_math_operations_types(self):
        line = "+ - * /"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_PLUS),
                    Token(TokenType.T_MINUS),
                    Token(TokenType.T_MUL),
                    Token(TokenType.T_DIV)]
        self.assertEqual(expected, predicted)

    def test_math_order_types(self):
        line = "<= < >= > == !="
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_LESS_OR_EQ),
                    Token(TokenType.T_LESS),
                    Token(TokenType.T_GREATER_OR_EQ),
                    Token(TokenType.T_GREATER),
                    Token(TokenType.T_EQ),
                    Token(TokenType.T_NOT_EQ)]
        self.assertEqual(expected, predicted)

    def test_logical_types(self):
        line = "or and not"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_OR),
                    Token(TokenType.T_AND),
                    Token(TokenType.T_NOT)]
        self.assertEqual(expected, predicted)

    def test_other_types(self):
        line = "if else true false return while = void function"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_IF),
                    Token(TokenType.T_ELSE),
                    Token(TokenType.T_TRUE),
                    Token(TokenType.T_FALSE),
                    Token(TokenType.T_RETURN),
                    Token(TokenType.T_WHILE),
                    Token(TokenType.T_ASSIGN),
                    Token(TokenType.T_VOID),
                    Token(TokenType.T_FUNCTION)]
        self.assertEqual(expected, predicted)

    def test_specific_to_task_types(self):
        line = "unit phys"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.T_UNIT),
                    Token(TokenType.T_PHYS)]
        self.assertEqual(expected, predicted)

    def test_const_values(self):
        line = "'c' \"string\" 5 2.5"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.VT_CHAR, "'c'"),
                    Token(TokenType.VT_STRING, '"string"'),
                    Token(TokenType.VT_INT, "5"),
                    Token(TokenType.VT_DOUBLE, "2.5")]
        self.assertEqual(expected, predicted)

    def test_id(self):
        line = "var_name x y z"
        predicted = self.lexer.get_tokens_from_line(line)
        expected = [Token(TokenType.VT_ID, "var_name"),
                    Token(TokenType.VT_ID, "x"),
                    Token(TokenType.VT_ID, "y"),
                    Token(TokenType.VT_ID, "z")]
        self.assertEqual(expected, predicted)


if __name__ == '__main__':
    unittest.main()
